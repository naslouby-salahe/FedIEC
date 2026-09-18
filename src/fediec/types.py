from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
from typing import Annotated, NewType

from pydantic import BaseModel, ConfigDict, Field, model_validator

from fediec.enums import (
    ArtifactAuditFamily,
    CounterfactualFeasibility,
    DatasetEligibility,
    DatasetRole,
    DatasetSource,
    DeviceCategory,
    IntentProvenanceGrade,
    NetworkExecutionFeature,
    NetworkTopology,
    RepresentationConfoundAxis,
    SemanticAction,
    SourceGroupKind,
    SplitFeasibility,
    SplitPartition,
    TransitionClass,
    ViolationFamily,
)

NonNegativeInt = Annotated[int, Field(ge=0)]
PositiveInt = Annotated[int, Field(gt=0)]
SignedInt = int
NonNegativeFloat = Annotated[float, Field(ge=0.0)]
PositiveFloat = Annotated[float, Field(gt=0.0)]
FiniteFloat = Annotated[float, Field(allow_inf_nan=False)]
UnitInterval = Annotated[float, Field(ge=0.0, le=1.0, allow_inf_nan=False)]
OpenUnitInterval = Annotated[float, Field(gt=0.0, lt=1.0, allow_inf_nan=False)]

Seed = NonNegativeInt
PacketCount = NonNegativeInt
ByteCount = NonNegativeInt
RemoteTransportPortCount = NonNegativeInt
SampleCount = NonNegativeInt
RoundCount = PositiveInt
EpochCount = PositiveInt
FeatureIndex = NonNegativeInt
FeatureCount = PositiveInt
FeatureValue = FiniteFloat
FeatureVariance = NonNegativeFloat
Dimension = PositiveInt
BlockCount = PositiveInt
LayerCount = PositiveInt
UnitCount = PositiveInt
BatchSize = PositiveInt
DeviceCount = PositiveInt
ManufacturerCount = PositiveInt
CategoryCount = PositiveInt
WindowCount = PositiveInt
InteractionCount = PositiveInt
SessionCount = PositiveInt
DayCount = PositiveInt
SplitSampleCount = PositiveInt
ReplicateCount = PositiveInt
PassiveMonitoringMinutes = PositiveInt

Probability = UnitInterval
Score = FiniteFloat
Threshold = FiniteFloat
MetricValue = UnitInterval
Duration = NonNegativeFloat
WindowLength = PositiveFloat
Quantile = UnitInterval
ArtifactDetectabilityBound = UnitInterval
Tolerance = OpenUnitInterval
LearningRate = OpenUnitInterval
SignificanceLevel = OpenUnitInterval
WeightDecay = NonNegativeFloat
GradientNormClip = NonNegativeFloat
AdamBeta = UnitInterval
AdamEpsilon = PositiveFloat
PcapTimestampScale = PositiveFloat

MonotonicTimestamp = FiniteFloat
WallClockTimestamp = NewType("WallClockTimestamp", datetime)

DeviceId = NewType("DeviceId", str)
ManufacturerId = NewType("ManufacturerId", str)
SessionId = NewType("SessionId", str)
InteractionId = NewType("InteractionId", str)
CaptureId = NewType("CaptureId", str)
SourceCaptureId = NewType("SourceCaptureId", str)
SourceGroupId = NewType("SourceGroupId", str)
SourceContextId = NewType("SourceContextId", str)
CollectionDay = NewType("CollectionDay", date)
AppPackage = NewType("AppPackage", str)
ConfigHash = NewType("ConfigHash", str)
ArtifactChecksum = NewType("ArtifactChecksum", str)
GitCommit = NewType("GitCommit", str)
SourceDependencyClusterId = NewType("SourceDependencyClusterId", str)
CheckDetail = NewType("CheckDetail", str)
BaselineName = NewType("BaselineName", str)
ConfigText = NewType("ConfigText", str)
DirectoryName = NewType("DirectoryName", str)
TargetDeviceMac = NewType("TargetDeviceMac", str)
NetworkFeatureName = NewType("NetworkFeatureName", str)

RepositoryPath = NewType("RepositoryPath", Path)

FeatureVectors = tuple["InteractionFeatureVector", ...]
InteractionIndex = NewType("InteractionIndex", int)
ModelParameterCount = NonNegativeInt
SerializedByteCount = NonNegativeInt
MemoryByteCount = NonNegativeInt
TrainingStepCount = NonNegativeInt

ZERO_PACKET_COUNT: PacketCount = 0
ZERO_BYTE_COUNT: ByteCount = 0
ZERO_SAMPLE_COUNT: SampleCount = 0
ZERO_FEATURE_VALUE: FeatureValue = 0.0
ONE_FEATURE_VALUE: FeatureValue = 1.0
MEDIAN_QUANTILE: Quantile = 0.5
P95_QUANTILE: Quantile = 0.95
NEAR_CONSTANT_VARIANCE_THRESHOLD: FeatureVariance = 1e-12
TOTAL_PACKET_COUNT_FEATURE_INDEX: FeatureIndex = 0
TOTAL_BYTE_COUNT_FEATURE_INDEX: FeatureIndex = 3
FIRST_PACKET_INDEX: FeatureIndex = 0
SAMPLE_AXIS_INDEX: FeatureIndex = 0
LAST_PACKET_INDEX: SignedInt = -1


class DomainRecord(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")


class InteractionFeatureVector(DomainRecord):
    values: tuple[FeatureValue, ...]

    @model_validator(mode="after")
    def require_active_schema_width(self) -> InteractionFeatureVector:
        if len(self.values) != len(NetworkExecutionFeature):
            raise ValueError("interaction feature vector must contain the active 19-feature schema")
        return self


class PublicSourceInteraction(DomainRecord):
    dataset_source: DatasetSource
    interaction_id: InteractionId
    device_id: DeviceId
    source_capture_id: SourceCaptureId
    source_group_id: SourceGroupId
    source_group_kind: SourceGroupKind
    source_context_id: SourceContextId
    semantic_action: SemanticAction
    intent_provenance_grade: IntentProvenanceGrade
    capture_start_timestamp: WallClockTimestamp | None = None
    trigger_timestamp: WallClockTimestamp | None = None
    capture_path: RepositoryPath
    target_device_mac: TargetDeviceMac | None = None
    source_checksum: ArtifactChecksum | None = None
    manufacturer_id: ManufacturerId | None = None
    device_category: DeviceCategory | None = None
    network_topology: NetworkTopology | None = None
    transition_class: TransitionClass | None = None


class CleanSplitAssignment(DomainRecord):
    interaction_id: InteractionId
    device_id: DeviceId
    source_context_id: SourceContextId
    semantic_action: SemanticAction
    source_group_id: SourceGroupId
    partition: SplitPartition | None = None


class CleanSplitContextSummary(DomainRecord):
    device_id: DeviceId
    source_context_id: SourceContextId
    semantic_action: SemanticAction
    interaction_count: SampleCount
    independent_source_group_count: SampleCount
    source_group_sizes: tuple[SampleCount, ...]
    training_count: SampleCount
    calibration_count: SampleCount
    test_count: SampleCount
    feasibility: SplitFeasibility


class CleanSplitManifest(DomainRecord):
    dataset_source: DatasetSource
    assignments: tuple[CleanSplitAssignment, ...]
    contexts: tuple[CleanSplitContextSummary, ...]


class RepresentationConfoundAudit(DomainRecord):
    dataset_source: DatasetSource
    feature_order: tuple[NetworkFeatureName, ...]
    feature_variances: tuple[FeatureVariance, ...]
    constant_features: tuple[NetworkFeatureName, ...]
    near_constant_features: tuple[NetworkFeatureName, ...]
    packet_count_range: tuple[FeatureValue, FeatureValue]
    byte_count_range: tuple[FeatureValue, FeatureValue]
    capture_duration_range: tuple[Duration, Duration]
    chronology_available: bool
    site_or_lab_identities: tuple[SourceContextId, ...]
    network_conditions: tuple[SourceContextId, ...]
    action_collection_ordering_available: bool
    source_identities: tuple[DatasetSource, ...]
    stratified_variation: tuple[RepresentationStratifiedVariation, ...]
    passed: bool


class RepresentationStratifiedVariation(DomainRecord):
    axis: RepresentationConfoundAxis
    stratum_count: SampleCount
    strata_with_constant_features: SampleCount
    universally_constant_features: tuple[NetworkFeatureName, ...]


class FrozenClientActionCount(DomainRecord):
    device_id: DeviceId
    semantic_action: SemanticAction
    training_count: SampleCount
    calibration_count: SampleCount
    test_count: SampleCount


class CounterfactualFeasibilityRecord(DomainRecord):
    violation_family: ViolationFamily
    feasibility: CounterfactualFeasibility
    reason: CheckDetail


class ArtifactControlRecord(DomainRecord):
    artifact_audit_family: ArtifactAuditFamily
    feasibility: CounterfactualFeasibility
    pass_rule: CheckDetail
    reason: CheckDetail


class ProtocolFreezeManifest(DomainRecord):
    dataset_source: DatasetSource
    role: DatasetRole
    eligible_capture_count: SampleCount
    eligible_physical_client_count: DeviceCount
    client_action_counts: tuple[FrozenClientActionCount, ...]
    source_group_count: SampleCount
    source_group_overlap_free: bool
    network_condition_treatment: CheckDetail
    feature_order: tuple[NetworkExecutionFeature, ...]
    context_dimension: Dimension
    supported_scarcity_budgets: tuple[SampleCount, ...]
    scarcity_eligible_client_count: DeviceCount
    full_eligible_client_count: DeviceCount
    holdout_definition: CheckDetail
    normalization_protocol: CheckDetail
    model_interface: CheckDetail
    baseline_interfaces: tuple[CheckDetail, ...]
    supported_violation_families: tuple[ViolationFamily, ...]
    counterfactual_feasibility: tuple[CounterfactualFeasibilityRecord, ...]
    artifact_control_plan: tuple[ArtifactControlRecord, ...]
    unavailable_analysis_reasons: tuple[CheckDetail, ...]
    seeds: tuple[Seed, ...]
    statistical_protocol: CheckDetail
    representation_confound_audit_passed: bool


class DatasetAssessment(DomainRecord):
    dataset_source: DatasetSource
    role: DatasetRole
    eligibility: DatasetEligibility
    intent_provenance_grade: IntentProvenanceGrade
