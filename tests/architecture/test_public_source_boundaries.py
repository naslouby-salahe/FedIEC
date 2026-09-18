from __future__ import annotations

import ast
from datetime import UTC, datetime
from pathlib import Path
from typing import get_type_hints

from _pytest.monkeypatch import MonkeyPatch

from fediec.datasets.cic_iot_2022.dataset import enumerate_raw_interactions as cic_interactions
from fediec.datasets.moniotr_imc_2019.dataset import (
    enumerate_raw_interactions as moniotr_interactions,
)
from fediec.datasets.moniotr_imc_2019.dataset import (
    physical_device_id,
)
from fediec.datasets.pingpong.dataset import enumerate_raw_interactions as pingpong_interactions
from fediec.datasets.pingpong.dataset import parse_source_timestamps_file
from fediec.datasets.splits import build_clean_split
from fediec.datasets.tu_wien_philips_hue.dataset import (
    enumerate_raw_interactions as hue_interactions,
)
from fediec.enums import (
    CliCommand,
    DatasetEligibility,
    DatasetRole,
    DatasetSource,
    EnvironmentVariable,
    IntentProvenanceGrade,
    MatchingTier,
    ReplayLateExecutionSubtype,
    RepositoryPathKey,
    SemanticAction,
    SourceGroupKind,
    ViolationFamily,
)
from fediec.paths import resolve_path
from fediec.types import (
    DeviceId,
    DirectoryName,
    InteractionId,
    Probability,
    PublicSourceInteraction,
    RepositoryPath,
    SourceCaptureId,
    SourceContextId,
    SourceGroupId,
    WallClockTimestamp,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = REPO_ROOT / "src" / "fediec"

_FORBIDDEN_SOURCE_MARKERS = (
    "fediec_contracts",
    "android_uiautomator",
    "android_appium",
    "gateway_capture",
    "live_capture",
    "device_scheduler",
    "physical_violation",
    "physical_attack",
)

_REQUIRED_INTERACTION_FIELDS = {
    "dataset_source",
    "interaction_id",
    "device_id",
    "source_capture_id",
    "source_group_id",
    "source_context_id",
    "semantic_action",
    "capture_start_timestamp",
    "trigger_timestamp",
    "intent_provenance_grade",
    "capture_path",
    "source_checksum",
}


def _source_files() -> list[Path]:
    return sorted(SRC_ROOT.rglob("*.py"))


def _nested_function_name(tree: ast.AST, node: ast.AST) -> str | None:
    parents = {
        id(child): parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)
    }
    current = parents.get(id(node))
    while current is not None:
        if isinstance(current, ast.FunctionDef | ast.AsyncFunctionDef):
            return current.name
        current = parents.get(id(current))
    return None


def test_required_public_source_enums_are_exact() -> None:
    assert set(ViolationFamily) == {
        ViolationFamily.OMISSION,
        ViolationFamily.SUBSTITUTION,
        ViolationFamily.UNCOMMANDED_EXECUTION,
        ViolationFamily.EXCESS_EXECUTION,
        ViolationFamily.REPLAY_OR_LATE_EXECUTION,
    }
    assert set(ReplayLateExecutionSubtype) == {
        ReplayLateExecutionSubtype.TEMPORALLY_MISALIGNED_EXECUTION,
        ReplayLateExecutionSubtype.PURE_REPLAY_REPRESENTATION_LIMIT,
    }
    assert set(DatasetEligibility) == {
        DatasetEligibility.FULL_CONTRACT_ELIGIBLE,
        DatasetEligibility.ACTION_CONTRACT_ONLY,
        DatasetEligibility.REPLICATION_ONLY,
        DatasetEligibility.ATTACK_ALIGNMENT_ONLY,
        DatasetEligibility.INELIGIBLE,
    }
    assert set(DatasetRole) == {
        DatasetRole.PRIMARY_INTERACTION_CONTRACT,
        DatasetRole.SPARSE_REPLICATION_PROTOCOL_MODE_CONTRAST,
        DatasetRole.SINGLE_DEVICE_FAMILY_REPLICATION,
        DatasetRole.PROVENANCE_DIAGNOSTIC,
    }
    assert set(IntentProvenanceGrade) == {
        IntentProvenanceGrade.VERIFIED_DIRECT,
        IntentProvenanceGrade.VERIFIED_PROTOCOL,
        IntentProvenanceGrade.PARTIAL,
        IntentProvenanceGrade.INELIGIBLE,
    }
    assert set(MatchingTier) == {
        MatchingTier.TIER_1_SAME_SOURCE_GROUP,
        MatchingTier.TIER_2_NEAREST_DISTINCT_SOURCE_GROUP,
        MatchingTier.TIER_3_OTHER_ELIGIBLE_SOURCE_GROUP,
    }


def test_public_source_interaction_retains_required_provenance_fields() -> None:
    assert set(PublicSourceInteraction.model_fields) >= _REQUIRED_INTERACTION_FIELDS
    for adapter in (
        pingpong_interactions,
        cic_interactions,
        hue_interactions,
        moniotr_interactions,
    ):
        assert get_type_hints(adapter)["return"] == tuple[PublicSourceInteraction, ...]


def test_pingpong_timestamp_text_uses_the_original_los_angeles_time_basis(
    tmp_path: Path,
) -> None:
    timestamp_file = tmp_path / "trigger.timestamps"
    timestamp_file.write_text("04/23/2019 04:41:44 PM\n", encoding="utf-8")
    parsed = parse_source_timestamps_file(timestamp_file)
    assert len(parsed) == 1
    assert parsed[0].isoformat() == "2019-04-23T23:41:44+00:00"


def test_clean_split_keeps_a_continuous_capture_in_one_partition(tmp_path: Path) -> None:
    capture_one = SourceGroupId("continuous-capture-one")
    interactions = tuple(
        PublicSourceInteraction(
            dataset_source=DatasetSource.PINGPONG,
            interaction_id=InteractionId(f"interaction-{index}"),
            device_id=DeviceId("device"),
            source_capture_id=SourceCaptureId(source_group_id),
            source_group_id=SourceGroupId(source_group_id),
            source_group_kind=SourceGroupKind.CONTINUOUS_CAPTURE,
            source_context_id=SourceContextId("context"),
            semantic_action=action,
            intent_provenance_grade=IntentProvenanceGrade.VERIFIED_PROTOCOL,
            trigger_timestamp=WallClockTimestamp(datetime(2020, 1, index + 1, tzinfo=UTC)),
            capture_path=RepositoryPath(tmp_path / f"{source_group_id}.pcap"),
        )
        for index, source_group_id, action in (
            (0, capture_one, SemanticAction.TURN_ON),
            (1, capture_one, SemanticAction.TURN_OFF),
            (2, SourceGroupId("continuous-capture-two"), SemanticAction.TURN_ON),
            (3, SourceGroupId("continuous-capture-three"), SemanticAction.TURN_ON),
        )
    )
    split_proportions: tuple[Probability, Probability, Probability] = (0.6, 0.2, 0.2)
    manifest = build_clean_split(
        DatasetSource.PINGPONG,
        interactions,
        split_proportions,
    )
    partitions = {
        assignment.partition
        for assignment in manifest.assignments
        if assignment.source_group_id == capture_one
    }
    assert len(partitions) == 1


def test_moniotr_physical_client_identity_keeps_labs_separate_and_vpn_together() -> None:
    us = DirectoryName("us")
    us_vpn = DirectoryName("us-vpn")
    uk = DirectoryName("uk")
    device = DirectoryName("tplink-plug")
    assert physical_device_id(us, device) == physical_device_id(us_vpn, device)
    assert physical_device_id(us, device) != physical_device_id(uk, device)


def test_production_code_has_no_physical_collection_scaffold() -> None:
    offenders = [
        f"{path.relative_to(SRC_ROOT)}:{marker}"
        for path in _source_files()
        for marker in _FORBIDDEN_SOURCE_MARKERS
        if marker in path.read_text(encoding="utf-8").lower()
    ]
    assert not offenders, offenders


def test_public_source_configuration_and_cli_do_not_restore_collection() -> None:
    config_text = (REPO_ROOT / "config.yaml").read_text(encoding="utf-8")
    assert "collection:" not in config_text
    assert "collect" not in {command.value for command in CliCommand}


def test_production_code_does_not_introspect_its_own_source_path() -> None:
    forbidden_names = {"__file__", "inspect", "ast"}
    offenders = [
        f"{path.relative_to(SRC_ROOT)}:{node.lineno}"
        for path in _source_files()
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"), filename=str(path)))
        if isinstance(node, ast.Name) and node.id in forbidden_names
    ]
    assert not offenders, offenders


def test_repository_root_is_explicitly_configurable(
    monkeypatch: MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv(EnvironmentVariable.REPOSITORY_ROOT, str(REPO_ROOT))
    assert resolve_path(RepositoryPathKey.CONFIG_FILE) == REPO_ROOT / "config.yaml"


def test_enum_value_usage_is_limited_to_exact_external_boundaries() -> None:
    allowed = {
        (SRC_ROOT / "cli.py", None),
        (SRC_ROOT / "paths.py", "resolve_output_run_directory"),
    }
    offenders: list[str] = []
    for path in _source_files():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Attribute) or node.attr != "value":
                continue
            function_name = _nested_function_name(tree, node)
            if (path, None) not in allowed and (path, function_name) not in allowed:
                offenders.append(f"{path.relative_to(SRC_ROOT)}:{node.lineno}")
    assert not offenders, offenders


def test_no_raw_dict_field_crosses_a_domain_record_boundary() -> None:
    offenders: list[str] = []
    for path in _source_files():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for class_node in (node for node in tree.body if isinstance(node, ast.ClassDef)):
            if not any(
                isinstance(base, ast.Name) and base.id == "DomainRecord"
                for base in class_node.bases
            ):
                continue
            for field in (node for node in class_node.body if isinstance(node, ast.AnnAssign)):
                if any(
                    isinstance(name, ast.Name) and name.id in {"dict", "Dict"}
                    for name in ast.walk(field.annotation)
                ):
                    offenders.append(f"{path.relative_to(SRC_ROOT)}:{field.lineno}")
    assert not offenders, offenders
