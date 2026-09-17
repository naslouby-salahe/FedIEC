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
    TEMPORALLY_MISALIGNED_EXECUTION = "temporally_misaligned_execution"
    PURE_REPLAY_REPRESENTATION_LIMIT = "pure_replay_representation_limit"


class ArtifactAuditFamily(StrEnum):
    REPLACEMENT_TRANSLATION = "replacement_translation"
    EXCESS_COMPOSITION = "excess_composition"


class MatchingTier(StrEnum):
    TIER_1_SAME_SESSION = "tier_1_same_session"
    TIER_2_SAME_DAY = "tier_2_same_day"
    TIER_3_ADJACENT_DAY = "tier_3_adjacent_day"


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
    FEDIEC_CONTRACTS = "fediec_contracts"
    PINGPONG = "pingpong"
    TU_WIEN_PHILIPS_HUE = "tu_wien_philips_hue"
    CIC_IOT_2022 = "cic_iot_2022"


class DatasetAvailability(StrEnum):
    PRESENT_AND_VALID = "present_and_valid"
    PRESENT_BUT_INCOMPLETE = "present_but_incomplete"
    PRESENT_BUT_SCHEMA_DRIFTED = "present_but_schema_drifted"
    PRESENT_BUT_CORRUPT = "present_but_corrupt"
    MISSING_EXTERNAL = "missing_external"
    MISSING_CONTROLLED_BENCHMARK = "missing_controlled_benchmark"


class AutomationSource(StrEnum):
    ANDROID_UIAUTOMATOR = "android_uiautomator"
    ANDROID_APPIUM = "android_appium"
    MANUAL_LOGGED = "manual_logged"


class PhysicalViolationMechanism(StrEnum):
    COMMAND_DELIVERY_INTERRUPTION = "command_delivery_interruption"
    SECONDARY_CONTROLLER_COMMAND = "secondary_controller_command"
    UNCOMMANDED_STATE_CHANGE = "uncommanded_state_change"
    DELAYED_COMMAND_EXECUTION = "delayed_command_execution"
    RAPID_CONTRADICTORY_COMMAND = "rapid_contradictory_command"
    TEMPORARY_NETWORK_INTERRUPTION = "temporary_network_interruption"


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
    PHYSICAL_VIOLATIONS = "physical-violations"
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
    DATA_RAW_FEDIEC_CONTRACTS = "data_raw_fediec_contracts"
    DATA_RAW_PINGPONG = "data_raw_pingpong"
    DATA_RAW_TU_WIEN_PHILIPS_HUE = "data_raw_tu_wien_philips_hue"
    DATA_RAW_CIC_IOT_2022 = "data_raw_cic_iot_2022"
    DATA_RAW_FEDIEC_CONTRACTS_CAPTURES = "data_raw_fediec_contracts_captures"
    DATA_RAW_FEDIEC_CONTRACTS_INTENT_LOGS = "data_raw_fediec_contracts_intent_logs"
    DATA_RAW_FEDIEC_CONTRACTS_SESSION_MANIFESTS = "data_raw_fediec_contracts_session_manifests"
    DATA_RAW_FEDIEC_CONTRACTS_DEVICE_METADATA = "data_raw_fediec_contracts_device_metadata"
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


class CliCommand(StrEnum):

    DOCTOR = "doctor"
    COLLECT = "collect"
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
    COLLECT_START = "cli.collect.start"
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
    DATASET_FEDIEC_CONTRACTS = "dataset:fediec_contracts"
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

    FEDIEC_CONTRACTS = "FedIEC-Contracts"
    PINGPONG = "PingPong"
    TU_WIEN_PHILIPS_HUE = "TU Wien Philips Hue"
    # Real on-disk name in the shared data pool differs from the dataset's
    # documented prose spelling ("CIC IoT 2022") — verified, not assumed.
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
    """LOCAL_PHONE and SAME_VENDOR are wired into the adapter today.
    REMOTE_PHONE/IFTTT/PUBLIC_DATASET exist on disk but are not yet
    included — see decisions-and-blockers.md."""

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
    """struct module format-string byte-order codes."""

    LITTLE = "<"
    BIG = ">"
