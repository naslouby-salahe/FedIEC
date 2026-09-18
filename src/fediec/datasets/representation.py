from __future__ import annotations

import struct
from itertools import pairwise
from pathlib import Path

from fediec.enums import NetworkExecutionFeature, StructByteOrder
from fediec.types import (
    FIRST_PACKET_INDEX,
    LAST_PACKET_INDEX,
    MEDIAN_QUANTILE,
    NEAR_CONSTANT_VARIANCE_THRESHOLD,
    P95_QUANTILE,
    TOTAL_BYTE_COUNT_FEATURE_INDEX,
    TOTAL_PACKET_COUNT_FEATURE_INDEX,
    ZERO_BYTE_COUNT,
    ZERO_FEATURE_VALUE,
    ZERO_PACKET_COUNT,
    Duration,
    FeatureIndex,
    FeatureValue,
    FeatureVariance,
    FeatureVectors,
    InteractionFeatureVector,
    MonotonicTimestamp,
    NetworkFeatureName,
    PcapTimestampScale,
    PublicSourceInteraction,
    RemoteTransportPortCount,
    RepresentationConfoundAudit,
    TargetDeviceMac,
)

_PCAP_FORMATS: dict[bytes, tuple[StructByteOrder, PcapTimestampScale]] = {
    b"\xd4\xc3\xb2\xa1": (StructByteOrder.LITTLE, 1e-6),
    b"\xa1\xb2\xc3\xd4": (StructByteOrder.BIG, 1e-6),
    b"\x4d\x3c\xb2\xa1": (StructByteOrder.LITTLE, 1e-9),
    b"\xa1\xb2\x3c\x4d": (StructByteOrder.BIG, 1e-9),
}


def _mac_text(value: bytes) -> TargetDeviceMac:
    return TargetDeviceMac(":".join(f"{part:x}" for part in value))


def _mean(values: tuple[FeatureValue, ...]) -> FeatureValue:
    return sum(values) / len(values) if values else ZERO_FEATURE_VALUE


def _standard_deviation(values: tuple[FeatureValue, ...]) -> FeatureValue:
    if len(values) < 2:
        return ZERO_FEATURE_VALUE
    mean = _mean(values)
    return (sum((value - mean) ** 2 for value in values) / len(values)) ** 0.5


def _quantile(values: tuple[FeatureValue, ...], quantile: FeatureValue) -> FeatureValue:
    if not values:
        return ZERO_FEATURE_VALUE
    ordered = sorted(values)
    index = round((len(ordered) - 1) * quantile)
    return ordered[index]


def extract_interaction_features(
    interaction: PublicSourceInteraction,
) -> InteractionFeatureVector:
    if interaction.target_device_mac is None:
        raise ValueError(f"{interaction.interaction_id}: target device MAC is unavailable")
    with Path(interaction.capture_path).open("rb") as handle:
        global_header = handle.read(24)
        if len(global_header) != 24 or global_header[:4] not in _PCAP_FORMATS:
            raise ValueError(f"{interaction.interaction_id}: unsupported classic PCAP")
        byte_order, scale = _PCAP_FORMATS[global_header[:4]]
        timestamps: list[MonotonicTimestamp] = []
        outbound_sizes: list[FeatureValue] = []
        inbound_sizes: list[FeatureValue] = []
        remote_endpoints: set[bytes] = set()
        remote_ports: set[RemoteTransportPortCount] = set()
        tcp_count = ZERO_PACKET_COUNT
        udp_count = ZERO_PACKET_COUNT
        total_bytes = ZERO_BYTE_COUNT
        while record_header := handle.read(16):
            if len(record_header) != 16:
                raise ValueError(f"{interaction.interaction_id}: truncated PCAP record header")
            seconds, fraction, captured_length, _ = struct.unpack(
                f"{byte_order}IIII", record_header
            )
            frame = handle.read(captured_length)
            if len(frame) != captured_length:
                raise ValueError(f"{interaction.interaction_id}: truncated PCAP frame")
            timestamp = seconds + fraction * scale
            if len(frame) < 14:
                continue
            destination, source, ethertype = frame[:6], frame[6:12], frame[12:14]
            target = interaction.target_device_mac
            if _mac_text(source) != target and _mac_text(destination) != target:
                continue
            timestamps.append(timestamp)
            total_bytes += captured_length
            outbound = _mac_text(source) == target
            (outbound_sizes if outbound else inbound_sizes).append(captured_length)
            if ethertype != b"\x08\x00" or len(frame) < 34:
                continue
            ip_start = 14
            ihl = (frame[ip_start] & 0x0F) * 4
            if ihl < 20 or len(frame) < ip_start + ihl:
                continue
            protocol = frame[ip_start + 9]
            source_ip = frame[ip_start + 12 : ip_start + 16]
            destination_ip = frame[ip_start + 16 : ip_start + 20]
            remote_endpoints.add(destination_ip if outbound else source_ip)
            if protocol == 6:
                tcp_count += 1
            if protocol == 17:
                udp_count += 1
            transport_start = ip_start + ihl
            if protocol in {6, 17} and len(frame) >= transport_start + 4:
                source_port, destination_port = struct.unpack(
                    "!HH", frame[transport_start : transport_start + 4]
                )
                remote_ports.add(destination_port if outbound else source_port)
    packet_count = len(timestamps)
    inter_arrival = tuple(later - earlier for earlier, later in pairwise(timestamps))
    duration = (
        timestamps[LAST_PACKET_INDEX] - timestamps[FIRST_PACKET_INDEX]
        if timestamps
        else ZERO_FEATURE_VALUE
    )
    return InteractionFeatureVector(
        values=(
            packet_count,
            len(outbound_sizes),
            len(inbound_sizes),
            total_bytes,
            sum(outbound_sizes),
            sum(inbound_sizes),
            _mean(tuple(outbound_sizes)),
            _standard_deviation(tuple(outbound_sizes)),
            _mean(tuple(inbound_sizes)),
            _standard_deviation(tuple(inbound_sizes)),
            _mean(inter_arrival),
            _standard_deviation(inter_arrival),
            _quantile(inter_arrival, MEDIAN_QUANTILE),
            _quantile(inter_arrival, P95_QUANTILE),
            tcp_count / packet_count if packet_count else ZERO_FEATURE_VALUE,
            udp_count / packet_count if packet_count else ZERO_FEATURE_VALUE,
            len(remote_endpoints),
            len(remote_ports),
            duration,
        )
    )


def interaction_feature_order() -> tuple[NetworkExecutionFeature, ...]:
    return tuple(NetworkExecutionFeature)


def constant_feature_indices(vectors: FeatureVectors) -> tuple[FeatureIndex, ...]:
    if not vectors:
        raise ValueError("representation-confound audit requires at least one interaction vector")
    return tuple(
        index
        for index in range(len(NetworkExecutionFeature))
        if len({vector.values[index] for vector in vectors}) == 1
    )


def require_nonconstant_representation(vectors: FeatureVectors) -> None:
    if constant_indices := constant_feature_indices(vectors):
        features = tuple(NetworkExecutionFeature)
        names = tuple(NetworkFeatureName(features[index]) for index in constant_indices)
        raise ValueError(f"representation-confound gate failed: constant features {names}")


def _variance(values: tuple[FeatureValue, ...]) -> FeatureVariance:
    if len(values) < 2:
        return ZERO_FEATURE_VALUE
    mean = _mean(values)
    return sum((value - mean) ** 2 for value in values) / len(values)


def _capture_duration_seconds(interaction: PublicSourceInteraction) -> Duration:
    with Path(interaction.capture_path).open("rb") as handle:
        global_header = handle.read(24)
        if len(global_header) != 24 or global_header[:4] not in _PCAP_FORMATS:
            raise ValueError(f"{interaction.interaction_id}: unsupported classic PCAP")
        byte_order, scale = _PCAP_FORMATS[global_header[:4]]
        first_timestamp: MonotonicTimestamp | None = None
        last_timestamp: MonotonicTimestamp | None = None
        while record_header := handle.read(16):
            if len(record_header) != 16:
                raise ValueError(f"{interaction.interaction_id}: truncated PCAP record header")
            seconds, fraction, captured_length, _ = struct.unpack(
                f"{byte_order}IIII", record_header
            )
            if len(handle.read(captured_length)) != captured_length:
                raise ValueError(f"{interaction.interaction_id}: truncated PCAP frame")
            timestamp = seconds + fraction * scale
            first_timestamp = timestamp if first_timestamp is None else first_timestamp
            last_timestamp = timestamp
    return (
        last_timestamp - first_timestamp
        if first_timestamp is not None and last_timestamp
        else ZERO_FEATURE_VALUE
    )


def audit_representation(
    interactions: tuple[PublicSourceInteraction, ...],
    vectors: FeatureVectors,
) -> RepresentationConfoundAudit:
    if not interactions or len(interactions) != len(vectors):
        raise ValueError("representation-confound audit requires matched interactions and vectors")
    feature_order = interaction_feature_order()
    variances = tuple(
        _variance(tuple(vector.values[index] for vector in vectors))
        for index in range(len(NetworkExecutionFeature))
    )
    constant = tuple(
        NetworkFeatureName(feature_order[index])
        for index, variance in enumerate(variances)
        if variance == ZERO_FEATURE_VALUE
    )
    near_constant = tuple(
        NetworkFeatureName(feature_order[index])
        for index, variance in enumerate(variances)
        if ZERO_FEATURE_VALUE < variance <= NEAR_CONSTANT_VARIANCE_THRESHOLD
    )
    capture_durations = tuple(_capture_duration_seconds(item) for item in interactions)
    timestamps = tuple(item.capture_start_timestamp for item in interactions)
    contexts = tuple(sorted({item.source_context_id for item in interactions}))
    sources = tuple(sorted({item.dataset_source for item in interactions}))
    actions = tuple(item.semantic_action for item in interactions)
    return RepresentationConfoundAudit(
        dataset_source=interactions[0].dataset_source,
        feature_order=tuple(NetworkFeatureName(item) for item in feature_order),
        feature_variances=variances,
        constant_features=constant,
        near_constant_features=near_constant,
        packet_count_range=(
            min(vector.values[TOTAL_PACKET_COUNT_FEATURE_INDEX] for vector in vectors),
            max(vector.values[TOTAL_PACKET_COUNT_FEATURE_INDEX] for vector in vectors),
        ),
        byte_count_range=(
            min(vector.values[TOTAL_BYTE_COUNT_FEATURE_INDEX] for vector in vectors),
            max(vector.values[TOTAL_BYTE_COUNT_FEATURE_INDEX] for vector in vectors),
        ),
        capture_duration_range=(min(capture_durations), max(capture_durations)),
        chronology_available=all(timestamp is not None for timestamp in timestamps),
        site_or_lab_identities=contexts,
        network_conditions=contexts,
        action_collection_ordering_available=len(set(actions)) > 1,
        source_identities=sources,
        passed=not constant and not near_constant,
    )


def require_representation_audit_pass(audit: RepresentationConfoundAudit) -> None:
    if not audit.passed:
        raise ValueError(
            "representation-confound gate failed: "
            f"constant={audit.constant_features}; near_constant={audit.near_constant_features}"
        )
