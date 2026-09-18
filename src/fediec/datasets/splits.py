from __future__ import annotations

from collections import defaultdict

from fediec.enums import DatasetSource, SemanticAction, SplitFeasibility, SplitPartition
from fediec.types import (
    CleanSplitAssignment,
    CleanSplitContextSummary,
    CleanSplitManifest,
    DeviceId,
    Probability,
    PublicSourceInteraction,
    SourceContextId,
    SourceGroupId,
    WallClockTimestamp,
)

_CURRENT_SOURCE_GROUP_COUNT = len((SplitPartition.TRAINING,))


def _source_ordering_timestamp(interaction: PublicSourceInteraction) -> WallClockTimestamp:
    if interaction.trigger_timestamp is not None:
        return interaction.trigger_timestamp
    if interaction.capture_start_timestamp is not None:
        return interaction.capture_start_timestamp
    raise ValueError(
        f"{interaction.interaction_id}: source interaction has no usable ordering timestamp"
    )


def build_clean_split(
    dataset_source: DatasetSource,
    interactions: tuple[PublicSourceInteraction, ...],
    split_proportions: tuple[Probability, Probability, Probability],
) -> CleanSplitManifest:
    grouped: defaultdict[SourceGroupId, list[PublicSourceInteraction]] = defaultdict(list)
    for interaction in interactions:
        grouped[interaction.source_group_id].append(interaction)
    contexts: defaultdict[
        tuple[DeviceId, SourceContextId, SemanticAction], list[list[PublicSourceInteraction]]
    ] = defaultdict(list)
    for group in grouped.values():
        for context in {
            (item.device_id, item.source_context_id, item.semantic_action) for item in group
        }:
            contexts[context].append(
                [
                    item
                    for item in group
                    if (item.device_id, item.source_context_id, item.semantic_action) == context
                ]
            )
    proportions = (
        (SplitPartition.TRAINING, split_proportions[0]),
        (SplitPartition.CALIBRATION, split_proportions[1]),
        (SplitPartition.TEST, split_proportions[2]),
    )
    ordered_groups = sorted(
        grouped.values(),
        key=lambda group: min(_source_ordering_timestamp(item) for item in group),
    )
    group_context_counts = {
        next(iter(group)).source_group_id: {
            context: len(items)
            for context in {
                (item.device_id, item.source_context_id, item.semantic_action) for item in group
            }
            for items in (
                [
                    item
                    for item in group
                    if (item.device_id, item.source_context_id, item.semantic_action) == context
                ],
            )
        }
        for group in ordered_groups
    }
    remaining_group_counts = {context: len(groups) for context, groups in contexts.items()}
    context_counts = {
        context: {partition: len(()) for partition, _ in proportions} for context in contexts
    }
    context_totals = {
        context: sum(len(group) for group in groups) for context, groups in contexts.items()
    }
    partition_by_group: dict[SourceGroupId, SplitPartition] = {}
    for group in ordered_groups:
        group_id = next(iter(group)).source_group_id
        affected_contexts = group_context_counts[group_id]
        required_empty_partitions: set[SplitPartition] | None = None
        for context in affected_contexts:
            remaining_group_counts[context] -= 1
            empty_partitions = {
                partition for partition, _ in proportions if not context_counts[context][partition]
            }
            if remaining_group_counts[context] + _CURRENT_SOURCE_GROUP_COUNT != len(
                empty_partitions
            ):
                continue
            required_empty_partitions = (
                empty_partitions
                if required_empty_partitions is None
                else required_empty_partitions & empty_partitions
            )
        candidates = (
            tuple(required_empty_partitions)
            if required_empty_partitions
            else tuple(partition for partition, _ in proportions)
        )
        partition = min(
            candidates,
            key=lambda candidate: sum(
                (
                    (
                        context_counts[context][selected_partition]
                        + (count if selected_partition == candidate else len(()))
                    )
                    / context_totals[context]
                    - proportion
                )
                ** 2
                for context, count in affected_contexts.items()
                for selected_partition, proportion in proportions
            ),
        )
        partition_by_group[group_id] = partition
        for context, count in affected_contexts.items():
            context_counts[context][partition] += count
    assignments = [
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
    ]
    summaries: list[CleanSplitContextSummary] = []
    for context, groups in sorted(contexts.items(), key=lambda item: item[0]):
        ordered = sorted(
            groups,
            key=lambda group: min(_source_ordering_timestamp(item) for item in group),
        )
        counts = context_counts[context]
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
    return CleanSplitManifest(
        dataset_source=dataset_source, assignments=tuple(assignments), contexts=tuple(summaries)
    )
