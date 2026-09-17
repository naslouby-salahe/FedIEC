from enum import StrEnum


class SemanticAction(StrEnum):
    NO_ACTION = "no_action"
    TURN_ON = "turn_on"
    TURN_OFF = "turn_off"


class TransitionClass(StrEnum):
    OFF_TO_ON = "off_to_on"
    ON_TO_OFF = "on_to_off"
    ON_TO_ON = "on_to_on"
    OFF_TO_OFF = "off_to_off"
    UNKNOWN = "unknown"


class NetworkTopology(StrEnum):
    LOCAL_WLAN = "local_wlan"
    CLOUD_MEDIATED = "cloud_mediated"
    HYBRID_OR_OTHER = "hybrid_or_other"


class DeviceCategory(StrEnum):
    SMART_BULB = "smart_bulb"
    SMART_PLUG = "smart_plug"
    SMART_SWITCH = "smart_switch"
    SMART_POWER_STRIP = "smart_power_strip"
    OTHER_BINARY_ACTUATOR = "other_binary_actuator"


class BackgroundActivityStratum(StrEnum):
    BACKGROUND_SILENT = "background_silent"
    BACKGROUND_LOW_ACTIVITY = "background_low_activity"
    BACKGROUND_ACTIVE_BURST = "background_active_burst"


class ViolationFamily(StrEnum):
    OMISSION = "omission"
    SUBSTITUTION = "substitution"
    UNCOMMANDED_EXECUTION = "uncommanded_execution"
    EXCESS_EXECUTION = "excess_execution"
    REPLAY_OR_LATE_EXECUTION = "replay_or_late_execution"


class ReplayLateExecutionSubtype(StrEnum):
    TEMPORALLY_MISALIGNED_EXECUTION = "temporally_misaligned_execution"
    PURE_REPLAY_REPRESENTATION_LIMIT = "pure_replay_representation_limit"


class ArtifactAuditFamily(StrEnum):
    REPLACEMENT_TRANSLATION = "replacement_translation"
    EXCESS_COMPOSITION = "excess_composition"


class MatchingTier(StrEnum):
    TIER_1_SAME_SOURCE_GROUP = "tier_1_same_source_group"
    TIER_2_NEAREST_DISTINCT_SOURCE_GROUP = "tier_2_nearest_distinct_source_group"
    TIER_3_OTHER_ELIGIBLE_SOURCE_GROUP = "tier_3_other_eligible_source_group"


class InfeasibilityReason(StrEnum):
    NO_VALID_COUNTERFACTUAL = "no_valid_counterfactual"
    COUNTERFACTUAL_INFEASIBLE_TRANSITION = "counterfactual_infeasible_transition"
    COUNTERFACTUAL_INFEASIBLE_BOUNDARY = "counterfactual_infeasible_boundary"
    COUNTERFACTUAL_INFEASIBLE_PHYSICAL_TIMELINE = "counterfactual_infeasible_physical_timeline"
    ARTIFACT_AUDIT_INSUFFICIENT = "artifact_audit_insufficient"


class InteractionExclusionReason(StrEnum):
    INTENT_TIMESTAMP_MISSING = "intent_timestamp_missing"
    INTENT_AMBIGUOUS = "intent_ambiguous"
    TARGET_DEVICE_AMBIGUOUS = "target_device_ambiguous"
    CAPTURE_CORRUPTED = "capture_corrupted"
    CAPTURE_OVERLAPS_ANOTHER_ACTION = "capture_overlaps_another_action"
    DEVICE_DISCONNECTED = "device_disconnected"
    CLOCK_SYNCHRONIZATION_FAILED = "clock_synchronization_failed"
    TRAFFIC_ATTRIBUTION_FAILED = "traffic_attribution_failed"
    ACTION_NOT_LOCKED_SEMANTIC = "action_not_locked_semantic"
    SETTLING_INTEGRITY_VIOLATED = "settling_integrity_violated"


class SplitPartition(StrEnum):
    TRAINING = "training"
    CALIBRATION = "calibration"
    TEST = "test"


class LearningRegime(StrEnum):
    LOCAL = "local"
    CENTRALIZED = "centralized"
    FEDERATED = "federated"


class DatasetSource(StrEnum):
    PINGPONG = "pingpong"
    TU_WIEN_PHILIPS_HUE = "tu_wien_philips_hue"
    CIC_IOT_2022 = "cic_iot_2022"


class DatasetAvailability(StrEnum):
    PRESENT_AND_VALID = "present_and_valid"
    PRESENT_BUT_INCOMPLETE = "present_but_incomplete"
    PRESENT_BUT_SCHEMA_DRIFTED = "present_but_schema_drifted"
    PRESENT_BUT_CORRUPT = "present_but_corrupt"
    MISSING_EXTERNAL = "missing_external"
    ACCESS_RESTRICTED = "access_restricted"


class DatasetEligibility(StrEnum):
    FULL_CONTRACT_ELIGIBLE = "full_contract_eligible"
    ACTION_CONTRACT_ONLY = "action_contract_only"
    REPLICATION_ONLY = "replication_only"
    ATTACK_ALIGNMENT_ONLY = "attack_alignment_only"
    INELIGIBLE = "ineligible"


class DatasetRole(StrEnum):
    PRIMARY_CANDIDATE = "primary_candidate"
    SECONDARY_CANDIDATE = "secondary_candidate"
    MECHANISM_REPLICATION = "mechanism_replication"
    OPTIONAL_ALIGNED_SOURCE = "optional_aligned_source"


class IntentProvenanceGrade(StrEnum):
    VERIFIED_DIRECT = "verified_direct"
    VERIFIED_PROTOCOL = "verified_protocol"
    SOURCE_DOCUMENTED_PATH = "source_documented_path"
    INSUFFICIENT = "insufficient"


class CheckStatus(StrEnum):
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"


class RunStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class ExperimentName(StrEnum):
    INTENT_VALUE = "intent-value"
    PRE_CONTEXT_VALUE = "pre-context-value"
    FEDERATED_COLLABORATION = "federated-collaboration"
    DATA_SCARCITY = "data-scarcity"
    CENTRALIZED_COMPARISON = "centralized-comparison"
    HETEROGENEITY = "heterogeneity"
    TRANSFER = "transfer"
    PROVENANCE_ROBUSTNESS = "provenance-robustness"
    OBSERVED_CONTROL_FAILURES = "observed-control-failures"
    EXTERNAL_VALIDATION = "external-validation"


class ModelArchitectureKind(StrEnum):
    CONDITIONAL_NORMALIZING_FLOW = "conditional_normalizing_flow"


class Optimizer(StrEnum):
    ADAM = "adam"


class ActivationFunction(StrEnum):
    RELU = "relu"


class TensorDType(StrEnum):
    FLOAT32 = "float32"


class AggregationRule(StrEnum):
    FEDAVG = "fedavg"


class ClientWeighting(StrEnum):
    LOCAL_SAMPLE_COUNT = "local_sample_count"


class RepositoryPathKey(StrEnum):
    REPO_ROOT = "repo_root"
    DOCS_ROOT = "docs_root"
    DOCS_IMPLEMENTATION_ROOT = "docs_implementation_root"
    DATA_ROOT = "data_root"
    DATA_RAW_ROOT = "data_raw_root"
    DATA_RAW_PINGPONG = "data_raw_pingpong"
    DATA_RAW_TU_WIEN_PHILIPS_HUE = "data_raw_tu_wien_philips_hue"
    DATA_RAW_CIC_IOT_2022 = "data_raw_cic_iot_2022"
    OUTPUTS_ROOT = "outputs_root"
    OUTPUTS_PROCESSED_ROOT = "outputs_processed_root"
    OUTPUTS_BENCHMARK_ROOT = "outputs_benchmark_root"
    OUTPUTS_RUNS_ROOT = "outputs_runs_root"
    OUTPUTS_ANALYSES_ROOT = "outputs_analyses_root"
    OUTPUTS_REPORTS_ROOT = "outputs_reports_root"
    RESULTS_ROOT = "results_root"
    RESULTS_BENCHMARK_ROOT = "results_benchmark_root"
    RESULTS_EXPERIMENTS_ROOT = "results_experiments_root"
    RESULTS_STATISTICS_ROOT = "results_statistics_root"
    RESULTS_TABLES_ROOT = "results_tables_root"
    RESULTS_FIGURES_ROOT = "results_figures_root"
    CONFIG_FILE = "config_file"


class EnvironmentVariable(StrEnum):
    REPOSITORY_ROOT = "FEDIEC_REPOSITORY_ROOT"


class CliCommand(StrEnum):

    DOCTOR = "doctor"
    PREPROCESS = "preprocess"
    PREPARE = "prepare"
    PLAN = "plan"
    SMOKE = "smoke"
    RUN = "run"
    STATUS = "status"
    REPORT = "report"


class LogEvent(StrEnum):

    DOCTOR_START = "cli.doctor.start"
    DOCTOR_DONE = "cli.doctor.done"
    PREPROCESS_START = "cli.preprocess.start"
    PREPARE_START = "cli.prepare.start"
    PLAN_START = "cli.plan.start"
    PLAN_DONE = "cli.plan.done"
    SMOKE_START = "cli.smoke.start"
    RUN_START = "cli.run.start"
    STATUS_START = "cli.status.start"
    STATUS_DONE = "cli.status.done"
    REPORT_START = "cli.report.start"


class TableColumn(StrEnum):

    CHECK = "check"
    STATUS = "status"
    DETAIL = "detail"
    EXPERIMENT = "experiment"
    SEED = "seed"


class TerminalColor(StrEnum):

    GREEN = "green"
    YELLOW = "yellow"
    RED = "red"
    BLUE = "blue"


class CheckKind(StrEnum):

    CONFIGURATION = "configuration"
    DATASET_PINGPONG = "dataset:pingpong"
    DATASET_TU_WIEN_PHILIPS_HUE = "dataset:tu_wien_philips_hue"
    DATASET_CIC_IOT_2022 = "dataset:cic_iot_2022"


class CicTriggerMethod(StrEnum):

    LOCAL = "LOCAL_"
    LAN = "LAN_"
    WAN = "WAN_"
    ALEXA = "ALEXA_"
    GOOGLE = "GOOGLE_"


class CicPolarityToken(StrEnum):

    ON = "ON"
    OFF = "OFF"


class TuWienPolarityToken(StrEnum):

    ON = "On"
    OFF = "Off"


class DatasetRawDirectoryName(StrEnum):

    PINGPONG = "PingPong"
    TU_WIEN_PHILIPS_HUE = "TU Wien Philips Hue"
    CIC_IOT_2022 = "cic-iot-2022"


class PingPongEligibleDevice(StrEnum):

    AMAZON_PLUG = "amazon-plug"
    DLINK_PLUG = "dlink-plug"
    ST_PLUG = "st-plug"
    TPLINK_PLUG = "tplink-plug"
    TPLINK_POWER_STRIP = "tplink-power-strip"
    TPLINK_TWO_OUTLET_PLUG = "tplink-two-outlet-plug"
    WEMO_INSIGHT_PLUG = "wemo-insight-plug"
    WEMO_PLUG = "wemo-plug"


class PingPongEvaluationSubtree(StrEnum):
    LOCAL_PHONE = "local-phone"
    SAME_VENDOR = "same-vendor"
    REMOTE_PHONE = "remote-phone"
    IFTTT = "ifttt"
    PUBLIC_DATASET = "public-dataset"


class NetworkCaptureSubdirectory(StrEnum):

    TIMESTAMPS = "timestamps"
    WLAN1 = "wlan1"
    WLAN = "wlan"
    ETH0 = "eth0"
    ETH1 = "eth1"
    VPN = "vpn"
    EVENT = "event"


class RawCaptureFileSuffix(StrEnum):

    PCAP = ".pcap"
    TIMESTAMPS = ".timestamps"


class StructByteOrder(StrEnum):
    LITTLE = "<"
    BIG = ">"


class RepositoryPathSegment(StrEnum):
    DOCS = "docs"
    IMPLEMENTATION = "implementation"
    DATA = "data"
    RAW = "raw"
    OUTPUTS = "outputs"
    PROCESSED = "processed"
    BENCHMARK = "benchmark"
    RUNS = "runs"
    ANALYSES = "analyses"
    REPORTS = "reports"
    RESULTS = "results"
    EXPERIMENTS = "experiments"
    STATISTICS = "statistics"
    TABLES = "tables"
    FIGURES = "figures"
    CONFIG_FILE = "config.yaml"
    RUN_MANIFEST_FILE = "manifest.json"


class NetworkExecutionFeature(StrEnum):

    TOTAL_PACKET_COUNT = "total_packet_count"
    OUTBOUND_PACKET_COUNT = "outbound_packet_count"
    INBOUND_PACKET_COUNT = "inbound_packet_count"
    TOTAL_BYTES = "total_bytes"
    OUTBOUND_BYTES = "outbound_bytes"
    INBOUND_BYTES = "inbound_bytes"
    MEAN_OUTBOUND_PACKET_SIZE = "mean_outbound_packet_size"
    STD_OUTBOUND_PACKET_SIZE = "std_outbound_packet_size"
    MEAN_INBOUND_PACKET_SIZE = "mean_inbound_packet_size"
    STD_INBOUND_PACKET_SIZE = "std_inbound_packet_size"
    MEAN_INTER_ARRIVAL_TIME = "mean_inter_arrival_time"
    STD_INTER_ARRIVAL_TIME = "std_inter_arrival_time"
    MEDIAN_INTER_ARRIVAL_TIME = "median_inter_arrival_time"
    P95_INTER_ARRIVAL_TIME = "p95_inter_arrival_time"
    UNIQUE_REMOTE_ENDPOINTS = "unique_remote_endpoints"
    UNIQUE_REMOTE_PORTS = "unique_remote_ports"
    FIRST_PACKET_LATENCY = "first_packet_latency"
    ACTIVE_SPAN = "active_span"
    TCP_FRACTION = "tcp_fraction"
    UDP_FRACTION = "udp_fraction"


class DatasetRawSubpath(StrEnum):
    CIC_IOT_2022_INTERACTIONS = "3-Interactions"
    PINGPONG_EVALUATION_DATASETS = "evaluation-datasets"
