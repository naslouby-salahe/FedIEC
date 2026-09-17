from __future__ import annotations

from functools import lru_cache

import yaml
from pydantic import ConfigDict, Field

from fediec.enums import (
    ActivationFunction,
    AggregationRule,
    ClientWeighting,
    ModelArchitectureKind,
    NetworkExecutionFeature,
    Optimizer,
    RepositoryPathKey,
    TensorDType,
)
from fediec.paths import resolve_path
from fediec.types import (
    ArtifactDetectabilityBound,
    BatchSize,
    BlockCount,
    CategoryCount,
    DayCount,
    DeviceCount,
    DeviceId,
    Dimension,
    DomainRecord,
    Duration,
    EpochCount,
    FeatureCount,
    GradientNormClip,
    InteractionCount,
    LayerCount,
    LearningRate,
    ManufacturerCount,
    PassiveMonitoringMinutes,
    Quantile,
    ReplicateCount,
    RoundCount,
    SampleCount,
    Seed,
    SessionCount,
    SignificanceLevel,
    SplitSampleCount,
    Tolerance,
    UnitCount,
    WeightDecay,
    WindowCount,
)


class ProjectSection(DomainRecord):
    target_device_count: DeviceCount
    minimum_device_count: DeviceCount
    minimum_manufacturer_count: ManufacturerCount
    minimum_category_count: CategoryCount


class NoActionStrataQuota(DomainRecord):
    background_silent: WindowCount
    background_low_activity: WindowCount
    background_active_burst: WindowCount


class CollectionSection(DomainRecord):
    turn_on_interactions_per_device: InteractionCount
    turn_off_interactions_per_device: InteractionCount
    no_action_windows_per_device: WindowCount
    no_action_strata_quota: NoActionStrataQuota
    minimum_sessions_per_device: SessionCount
    minimum_days_per_device: DayCount
    pilot_turn_on_interactions_per_device: InteractionCount
    pilot_turn_off_interactions_per_device: InteractionCount
    pilot_minimum_passive_monitoring_minutes: PassiveMonitoringMinutes
    observation_window_seconds: Duration | None = None
    settling_latency_seconds_per_device: dict[DeviceId, Duration] = Field(
        default_factory=dict[DeviceId, Duration]
    )
    clock_synchronization_tolerance_seconds: Duration | None = None


class SplitSection(DomainRecord):
    training_samples_per_device_context: SplitSampleCount
    calibration_samples_per_device_context: SplitSampleCount
    test_samples_per_device_context: SplitSampleCount


class FeaturesSection(DomainRecord):
    feature_count: FeatureCount
    log1p_magnitude_features: tuple[NetworkExecutionFeature, ...]
    rate_features: tuple[NetworkExecutionFeature, ...]


class CounterfactualsSection(DomainRecord):
    common_support_caliper_quantile: Quantile
    artifact_audit_tolerance: Tolerance
    artifact_audit_max_individual_device_a_star: ArtifactDetectabilityBound
    artifact_audit_max_per_feature_a_star: ArtifactDetectabilityBound


class ModelSection(DomainRecord):
    architecture: ModelArchitectureKind
    execution_dimension: Dimension
    context_dimension: Dimension
    coupling_blocks: BlockCount
    hidden_layers_per_conditioner: LayerCount
    hidden_units_per_layer: UnitCount
    activation: ActivationFunction


class TrainingSection(DomainRecord):
    optimizer: Optimizer
    learning_rate: LearningRate
    batch_size: BatchSize
    weight_decay: WeightDecay
    gradient_norm_clip: GradientNormClip
    dtype: TensorDType
    seeds: tuple[Seed, ...]
    local_epochs_full_data: EpochCount
    centralized_epochs_full_data: EpochCount


class FederatedSection(DomainRecord):
    aggregation: AggregationRule
    weighting: ClientWeighting
    local_epochs: EpochCount
    communication_rounds: RoundCount
    batch_size: BatchSize
    scarcity_budgets: tuple[SampleCount, ...]


class CalibrationSection(DomainRecord):
    threshold_quantile: Quantile


class StatisticsSection(DomainRecord):
    alpha: SignificanceLevel
    bootstrap_replicates: ReplicateCount


class FediecConfig(DomainRecord):
    model_config = ConfigDict(frozen=True, extra="forbid")

    project: ProjectSection
    collection: CollectionSection
    split: SplitSection
    features: FeaturesSection
    counterfactuals: CounterfactualsSection
    model: ModelSection
    training: TrainingSection
    federated: FederatedSection
    calibration: CalibrationSection
    statistics: StatisticsSection


@lru_cache(maxsize=1)
def load_config() -> FediecConfig:
    config_path = resolve_path(RepositoryPathKey.CONFIG_FILE)
    raw_text = config_path.read_text(encoding="utf-8")
    raw_mapping = yaml.safe_load(raw_text)
    return FediecConfig.model_validate(raw_mapping)


__all__ = ["FediecConfig", "load_config"]
