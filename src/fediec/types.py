from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
from typing import Annotated, NewType

from pydantic import BaseModel, ConfigDict, Field

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

Probability = UnitInterval
Score = FiniteFloat
Threshold = FiniteFloat
Duration = NonNegativeFloat
WindowLength = PositiveFloat

MonotonicTimestamp = FiniteFloat
WallClockTimestamp = NewType("WallClockTimestamp", datetime)

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
CheckLabel = NewType("CheckLabel", str)
CheckDetail = NewType("CheckDetail", str)
ConfigText = NewType("ConfigText", str)

RepositoryPath = NewType("RepositoryPath", Path)


class DomainRecord(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")


class DatasetFileInventoryEntry(DomainRecord):
    relative_path: RepositoryPath
    size_bytes: NonNegativeInt
    checksum: ArtifactChecksum | None = None
