from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
from typing import Annotated, NewType

from pydantic import BaseModel, ConfigDict, Field

from fediec.enums import (
    DatasetEligibility,
    DatasetRole,
    DatasetSource,
    DeviceCategory,
    IntentProvenanceGrade,
    NetworkTopology,
    SemanticAction,
    TransitionClass,
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
SampleCount = NonNegativeInt
RoundCount = PositiveInt
EpochCount = PositiveInt
FeatureIndex = NonNegativeInt
FeatureCount = PositiveInt
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
Duration = NonNegativeFloat
WindowLength = PositiveFloat
Quantile = UnitInterval
ArtifactDetectabilityBound = UnitInterval
Tolerance = OpenUnitInterval
LearningRate = OpenUnitInterval
SignificanceLevel = OpenUnitInterval
WeightDecay = NonNegativeFloat
GradientNormClip = NonNegativeFloat
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
CollectionDay = NewType("CollectionDay", date)
AppPackage = NewType("AppPackage", str)
ConfigHash = NewType("ConfigHash", str)
ArtifactChecksum = NewType("ArtifactChecksum", str)
GitCommit = NewType("GitCommit", str)
SourceDependencyClusterId = NewType("SourceDependencyClusterId", str)
CheckDetail = NewType("CheckDetail", str)
ConfigText = NewType("ConfigText", str)
DirectoryName = NewType("DirectoryName", str)

RepositoryPath = NewType("RepositoryPath", Path)


class DomainRecord(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")


class PublicSourceInteraction(DomainRecord):
    dataset_source: DatasetSource
    interaction_id: InteractionId
    device_id: DeviceId
    source_capture_id: SourceCaptureId
    source_group_id: SourceGroupId
    semantic_action: SemanticAction
    trigger_timestamp: WallClockTimestamp
    intent_provenance_grade: IntentProvenanceGrade
    capture_path: RepositoryPath
    source_checksum: ArtifactChecksum | None = None
    manufacturer_id: ManufacturerId | None = None
    device_category: DeviceCategory | None = None
    network_topology: NetworkTopology | None = None
    transition_class: TransitionClass | None = None


class DatasetAssessment(DomainRecord):
    dataset_source: DatasetSource
    role: DatasetRole
    eligibility: DatasetEligibility
    intent_provenance_grade: IntentProvenanceGrade
