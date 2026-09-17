from __future__ import annotations

from functools import lru_cache

import yaml
from pydantic import ConfigDict, Field

from fediec.enums import (
    ActivationFunction,
    AggregationRule,
    ClientWeighting,
    ModelArchitectureKind,
    Optimizer,
    RepositoryPathKey,
    TensorDType,
)
from fediec.paths import resolve_path
from fediec.types import (
    DeviceId,
    DomainRecord,
    Duration,
    NonNegativeFloat,
    OpenUnitInterval,
    PositiveInt,
    SampleCount,
    Seed,
    UnitInterval,
)


class ProjectSection(DomainRecord):
    target_device_count: PositiveInt
    minimum_device_count: PositiveInt
    minimum_manufacturer_count: PositiveInt
    minimum_category_count: PositiveInt


class NoActionStrataQuota(DomainRecord):
    background_silent: PositiveInt
    background_low_activity: PositiveInt
    background_active_burst: PositiveInt


class CollectionSection(DomainRecord):
    turn_on_interactions_per_device: PositiveInt
    turn_off_interactions_per_device: PositiveInt
    no_action_windows_per_device: PositiveInt
    no_action_strata_quota: NoActionStrataQuota
    minimum_sessions_per_device: PositiveInt
    minimum_days_per_device: PositiveInt
    pilot_turn_on_interactions_per_device: PositiveInt
    pilot_turn_off_interactions_per_device: PositiveInt
    pilot_minimum_passive_monitoring_minutes: PositiveInt
    observation_window_seconds: Duration | None = None
    settling_latency_seconds_per_device: dict[DeviceId, Duration] = Field(
        default_factory=dict[DeviceId, Duration]
    )
    clock_synchronization_tolerance_seconds: Duration | None = None


class SplitSection(DomainRecord):
    training_samples_per_device_context: PositiveInt
    calibration_samples_per_device_context: PositiveInt
    test_samples_per_device_context: PositiveInt


class FeaturesSection(DomainRecord):
    feature_count: PositiveInt
    log1p_magnitude_features: tuple[str, ...]
    rate_features: tuple[str, ...]


class CounterfactualsSection(DomainRecord):
    common_support_caliper_quantile: UnitInterval
    artifact_audit_tolerance: OpenUnitInterval
    artifact_audit_max_individual_device_a_star: UnitInterval
    artifact_audit_max_per_feature_a_star: UnitInterval


class ModelSection(DomainRecord):
    architecture: ModelArchitectureKind
    execution_dimension: PositiveInt
    context_dimension: PositiveInt
    coupling_blocks: PositiveInt
    hidden_layers_per_conditioner: PositiveInt
    hidden_units_per_layer: PositiveInt
    activation: ActivationFunction


class TrainingSection(DomainRecord):
    optimizer: Optimizer
    learning_rate: OpenUnitInterval
    batch_size: PositiveInt
    weight_decay: NonNegativeFloat
    gradient_norm_clip: NonNegativeFloat
    dtype: TensorDType
    seeds: tuple[Seed, ...]
    local_epochs_full_data: PositiveInt
    centralized_epochs_full_data: PositiveInt


class FederatedSection(DomainRecord):
    aggregation: AggregationRule
    weighting: ClientWeighting
    local_epochs: PositiveInt
    communication_rounds: PositiveInt
    batch_size: PositiveInt
    scarcity_budgets: tuple[SampleCount, ...]


class CalibrationSection(DomainRecord):
    threshold_quantile: UnitInterval


class StatisticsSection(DomainRecord):
    alpha: OpenUnitInterval
    bootstrap_replicates: PositiveInt


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
