from __future__ import annotations

from functools import lru_cache

import yaml
from pydantic import ConfigDict

from fediec.enums import (
    ActivationFunction,
    AggregationRule,
    ClientWeighting,
    DatasetEligibility,
    DatasetRole,
    IntentProvenanceGrade,
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
    DeviceCount,
    Dimension,
    DomainRecord,
    EpochCount,
    FeatureCount,
    GradientNormClip,
    LayerCount,
    LearningRate,
    Probability,
    Quantile,
    ReplicateCount,
    RoundCount,
    SampleCount,
    Seed,
    SignificanceLevel,
    Tolerance,
    UnitCount,
    WeightDecay,
)


class ProjectSection(DomainRecord):
    minimum_eligible_device_clients_for_main_federated_claim: DeviceCount


class PublicSourceSection(DomainRecord):
    role: DatasetRole
    eligibility: DatasetEligibility
    intent_provenance: IntentProvenanceGrade


class PublicSourcesSection(DomainRecord):
    pingpong: PublicSourceSection
    cic_iot_2022: PublicSourceSection
    tu_wien_philips_hue: PublicSourceSection
    moniotr_imc_2019: PublicSourceSection


class SplitSection(DomainRecord):
    training_proportion: Probability
    calibration_proportion: Probability
    test_proportion: Probability


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
    interaction_dimension: Dimension
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
    public_sources: PublicSourcesSection
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
