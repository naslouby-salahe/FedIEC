from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

from fediec.enums import DatasetSource, SemanticAction, SplitFeasibility, SplitPartition
from fediec.types import (
    ZERO_SAMPLE_COUNT,
    CleanSplitAssignment,
    CleanSplitContextSummary,
    CleanSplitManifest,
    DeviceId,
    Probability,
    PublicSourceInteraction,
    SampleCount,
    SourceContextId,
    SourceGroupId,
    SplitBalancingError,
    WallClockTimestamp,
)

_SINGLE_GROUP_BEING_ASSIGNED: SampleCount = 1

_Context = tuple[DeviceId, SourceContextId, SemanticAction]
_Group = tuple[PublicSourceInteraction, ...]
_PartitionProportion = tuple[SplitPartition, Probability]
_ContextCounts = tuple[tuple[_Context, SampleCount], ...]
_ContextGroups = tuple[tuple[_Context, tuple[_Group, ...]], ...]
_GroupContextCounts = tuple[tuple[SourceGroupId, _ContextCounts], ...]
_Proportions = tuple[_PartitionProportion, ...]


def _source_ordering_timestamp(interaction: PublicSourceInteraction) -> WallClockTimestamp:
    if interaction.trigger_timestamp is not None:
        return interaction.trigger_timestamp
    if interaction.capture_start_timestamp is not None:
        return interaction.capture_start_timestamp
    raise ValueError(
        f"{interaction.interaction_id}: source interaction has no usable ordering timestamp"
    )


def _earliest_timestamp(group: _Group) -> WallClockTimestamp:
    return min(_source_ordering_timestamp(item) for item in group)


def _context_of(item: PublicSourceInteraction) -> _Context:
    return (item.device_id, item.source_context_id, item.semantic_action)


def _group_by_source_group(
    interactions: tuple[PublicSourceInteraction, ...],
) -> tuple[_Group, ...]:
    grouped: defaultdict[SourceGroupId, list[PublicSourceInteraction]] = defaultdict(list)
    for interaction in interactions:
        grouped[interaction.source_group_id].append(interaction)
    return tuple(tuple(items) for items in grouped.values())


def _group_by_context(groups: tuple[_Group, ...]) -> _ContextGroups:
    contexts: defaultdict[_Context, list[_Group]] = defaultdict(list)
    for group in groups:
        for context in {_context_of(item) for item in group}:
            contexts[context].append(
                tuple(item for item in group if _context_of(item) == context)
            )
    return tuple((context, tuple(sub_groups)) for context, sub_groups in contexts.items())


def _group_context_counts(ordered_groups: tuple[_Group, ...]) -> _GroupContextCounts:
    result: list[tuple[SourceGroupId, _ContextCounts]] = []
    for group in ordered_groups:
        present_contexts = {_context_of(item) for item in group}
        counts = tuple(
            (context, sum(_context_of(item) == context for item in group))
            for context in present_contexts
        )
        result.append((group[0].source_group_id, counts))
    return tuple(result)


@dataclass
class _BalancingState:
    remaining_group_counts: dict[_Context, SampleCount]
    context_counts: dict[_Context, dict[SplitPartition, SampleCount]]
    context_totals: dict[_Context, SampleCount]


def _build_balancing_state(contexts: _ContextGroups, proportions: _Proportions) -> _BalancingState:
    return _BalancingState(
        remaining_group_counts={context: len(groups) for context, groups in contexts},
        context_counts={
            context: dict.fromkeys((partition for partition, _ in proportions), ZERO_SAMPLE_COUNT)
            for context, _ in contexts
        },
        context_totals={
            context: sum(len(group) for group in groups) for context, groups in contexts
        },
    )


def _empty_partitions_for(
    state: _BalancingState, context: _Context, proportions: _Proportions
) -> set[SplitPartition]:
    return {
        partition for partition, _ in proportions if not state.context_counts[context][partition]
    }


def _required_empty_partitions(
    state: _BalancingState, affected_contexts: _ContextCounts, proportions: _Proportions
) -> set[SplitPartition] | None:
    required: set[SplitPartition] | None = None
    for context, _ in affected_contexts:
        state.remaining_group_counts[context] -= 1
        empty_partitions = _empty_partitions_for(state, context, proportions)
        if state.remaining_group_counts[context] + _SINGLE_GROUP_BEING_ASSIGNED != len(
            empty_partitions
        ):
            continue
        required = empty_partitions if required is None else required & empty_partitions
    return required


def _balancing_error(
    state: _BalancingState,
    affected_contexts: _ContextCounts,
    candidate: SplitPartition,
    proportions: _Proportions,
) -> SplitBalancingError:
    return sum(
        (
            (
                state.context_counts[context][selected_partition]
                + (count if selected_partition == candidate else ZERO_SAMPLE_COUNT)
            )
            / state.context_totals[context]
            - proportion
        )
        ** 2
        for context, count in affected_contexts
        for selected_partition, proportion in proportions
    )


def _select_balancing_partition(
    state: _BalancingState, affected_contexts: _ContextCounts, proportions: _Proportions
) -> SplitPartition:
    required = _required_empty_partitions(state, affected_contexts, proportions)
    candidates = tuple(required) if required else tuple(partition for partition, _ in proportions)
    return min(
        candidates,
        key=lambda candidate: _balancing_error(state, affected_contexts, candidate, proportions),
    )


def _assign_partitions(
    ordered_groups: tuple[_Group, ...],
    group_context_counts: _GroupContextCounts,
    contexts: _ContextGroups,
    proportions: _Proportions,
) -> tuple[tuple[SourceGroupId, SplitPartition], ...]:
    affected_by_group = dict(group_context_counts)
    state = _build_balancing_state(contexts, proportions)
    partition_by_group: list[tuple[SourceGroupId, SplitPartition]] = []
    for group in ordered_groups:
        group_id = group[0].source_group_id
        affected_contexts = affected_by_group[group_id]
        partition = _select_balancing_partition(state, affected_contexts, proportions)
        partition_by_group.append((group_id, partition))
        for context, count in affected_contexts:
            state.context_counts[context][partition] += count
    return tuple(partition_by_group)


def _build_context_summaries(
    contexts: _ContextGroups,
    partition_by_group: tuple[tuple[SourceGroupId, SplitPartition], ...],
    proportions: _Proportions,
) -> tuple[CleanSplitContextSummary, ...]:
    partition_lookup = dict(partition_by_group)
    summaries: list[CleanSplitContextSummary] = []
    for context, groups in sorted(contexts, key=lambda item: item[0]):
        ordered = sorted(groups, key=_earliest_timestamp)
        counts: dict[SplitPartition, SampleCount] = dict.fromkeys(
            (partition for partition, _ in proportions), ZERO_SAMPLE_COUNT
        )
        for group in ordered:
            counts[partition_lookup[group[0].source_group_id]] += len(group)
        feasible = len(ordered) >= len(proportions) and all(
            counts[partition] > 0 for partition, _ in proportions
        )
        summaries.append(
            CleanSplitContextSummary(
                device_id=context[0],
                source_context_id=context[1],
                semantic_action=context[2],
                interaction_count=sum(len(group) for group in ordered),
                independent_source_group_count=len(ordered),
                source_group_sizes=tuple(len(group) for group in ordered),
                training_count=counts[SplitPartition.TRAINING],
                calibration_count=counts[SplitPartition.CALIBRATION],
                test_count=counts[SplitPartition.TEST],
                feasibility=(
                    SplitFeasibility.ALL_PARTITIONS_AVAILABLE
                    if feasible
                    else SplitFeasibility.INSUFFICIENT_INDEPENDENT_GROUPS
                ),
            )
        )
    return tuple(summaries)


def build_clean_split(
    dataset_source: DatasetSource,
    interactions: tuple[PublicSourceInteraction, ...],
    split_proportions: tuple[Probability, Probability, Probability],
) -> CleanSplitManifest:
    groups = _group_by_source_group(interactions)
    contexts = _group_by_context(groups)
    proportions = (
        (SplitPartition.TRAINING, split_proportions[0]),
        (SplitPartition.CALIBRATION, split_proportions[1]),
        (SplitPartition.TEST, split_proportions[2]),
    )
    ordered_groups = tuple(sorted(groups, key=_earliest_timestamp))
    group_context_counts = _group_context_counts(ordered_groups)
    partition_assignments = _assign_partitions(
        ordered_groups, group_context_counts, contexts, proportions
    )
    partition_by_group = dict(partition_assignments)
    assignments = tuple(
        CleanSplitAssignment(
            interaction_id=item.interaction_id,
            device_id=item.device_id,
            source_context_id=item.source_context_id,
            semantic_action=item.semantic_action,
            source_group_id=item.source_group_id,
            partition=partition_by_group[item.source_group_id],
        )
        for group in ordered_groups
        for item in group
    )
    summaries = _build_context_summaries(contexts, partition_assignments, proportions)
    return CleanSplitManifest(
        dataset_source=dataset_source, assignments=assignments, contexts=summaries
    )
