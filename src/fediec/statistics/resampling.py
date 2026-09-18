from __future__ import annotations

from collections import Counter, defaultdict

from numpy.random import Generator

from fediec.types import DeviceId, InteractionId, PermutationSign, PredictionRecord, SourceGroupId


def _device_hierarchy(
    predictions: tuple[PredictionRecord, ...],
) -> tuple[tuple[DeviceId, tuple[tuple[SourceGroupId, tuple[InteractionId, ...]], ...]], ...]:
    hierarchy: dict[DeviceId, dict[SourceGroupId, list[InteractionId]]] = defaultdict(
        lambda: defaultdict(list)
    )
    seen: set[tuple[DeviceId, SourceGroupId, InteractionId]] = set()
    for record in predictions:
        key = (record.device_id, record.source_group_id, record.interaction_id)
        if key in seen:
            continue
        seen.add(key)
        hierarchy[record.device_id][record.source_group_id].append(record.interaction_id)
    return tuple(
        (device, tuple((group, tuple(interactions)) for group, interactions in groups.items()))
        for device, groups in hierarchy.items()
    )


def resample_interaction_weights(
    predictions: tuple[PredictionRecord, ...], rng: Generator
) -> Counter[InteractionId]:
    hierarchy = dict(_device_hierarchy(predictions))
    devices = tuple(hierarchy)
    if not devices:
        raise ValueError("hierarchical bootstrap requires at least one physical device")
    weights: Counter[InteractionId] = Counter()
    sampled_devices = rng.choice(devices, size=len(devices), replace=True)
    for device in sampled_devices:
        groups = dict(hierarchy[device])
        group_ids = tuple(groups)
        sampled_groups = rng.choice(group_ids, size=len(group_ids), replace=True)
        for group in sampled_groups:
            interactions = groups[group]
            sampled_interactions = rng.choice(interactions, size=len(interactions), replace=True)
            weights.update(sampled_interactions)
    return weights


def device_sign_flip(
    devices: tuple[DeviceId, ...], rng: Generator
) -> tuple[tuple[DeviceId, PermutationSign], ...]:
    signs = rng.choice((-1, 1), size=len(devices))
    return tuple(zip(devices, (int(sign) for sign in signs), strict=True))
