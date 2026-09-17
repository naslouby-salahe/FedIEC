from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
from typing import Annotated, NewType

from pydantic import BaseModel, ConfigDict, Field

# --- Constrained scalar primitives -----------------------------------------
#
# These eight names exist only to build the semantic aliases below. They
# must never be referenced by name anywhere outside this module — every
# other module uses one of the semantic aliases instead, even when two
# aliases happen to share the same underlying constraint.

NonNegativeInt = Annotated[int, Field(ge=0)]
PositiveInt = Annotated[int, Field(gt=0)]
SignedInt = int
NonNegativeFloat = Annotated[float, Field(ge=0.0)]
PositiveFloat = Annotated[float, Field(gt=0.0)]
FiniteFloat = Annotated[float, Field(allow_inf_nan=False)]
UnitInterval = Annotated[float, Field(ge=0.0, le=1.0, allow_inf_nan=False)]
OpenUnitInterval = Annotated[float, Field(gt=0.0, lt=1.0, allow_inf_nan=False)]

# --- Semantic scalar aliases ------------------------------------------------

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

# --- Identifiers and other nominal string/bytes-based types ----------------

DeviceId = NewType("DeviceId", str)
ManufacturerId = NewType("ManufacturerId", str)
SessionId = NewType("SessionId", str)
InteractionId = NewType("InteractionId", str)
CaptureId = NewType("CaptureId", str)
CollectionDay = NewType("CollectionDay", date)
AppPackage = NewType("AppPackage", str)
ConfigHash = NewType("ConfigHash", str)
ArtifactChecksum = NewType("ArtifactChecksum", str)
GitCommit = NewType("GitCommit", str)
SourceDependencyClusterId = NewType("SourceDependencyClusterId", str)
CheckDetail = NewType("CheckDetail", str)
ConfigText = NewType("ConfigText", str)
FeatureName = NewType("FeatureName", str)
DirectoryName = NewType("DirectoryName", str)
FileName = NewType("FileName", str)

RepositoryPath = NewType("RepositoryPath", Path)


class DomainRecord(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
