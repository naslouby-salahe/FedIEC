from __future__ import annotations

import re
from pathlib import Path

from fediec.datasets.cic_iot_2022.dataset import read_pcap_first_packet_timestamp
from fediec.enums import (
    DatasetAvailability,
    DatasetSource,
    IntentProvenanceGrade,
    MoniotrPolarityToken,
    RawCaptureFileSuffix,
    SemanticAction,
    SourceGroupKind,
)
from fediec.paths import (
    resolve_dataset_raw_root,
    resolve_moniotr_idle_root,
    resolve_moniotr_interactions_root,
)
from fediec.types import (
    DeviceId,
    DirectoryName,
    InteractionId,
    PublicSourceInteraction,
    RepositoryPath,
    SourceCaptureId,
    SourceContextId,
    SourceGroupId,
    TargetDeviceMac,
)

_OFFICIAL_TARGET_MACS = {
    "uk": {
        "allure-speaker": "b0:f1:ec:d4:26:ae",
        "appletv": "50:32:37:b8:c7:f",
        "blink-camera": "f4:b8:5e:68:8f:35",
        "blink-security-hub": "0:3:7f:96:d8:ec",
        "bosiwo-camera-wifi": "0:c:43:3:51:be",
        "bosiwo-camera-wired": "ae:ca:6:e:ec:89",
        "charger-camera": "fc:ee:e6:2e:23:a3",
        "dlink-camera": "b0:c5:54:12:33:40",
        "echodot": "cc:f7:35:49:f4:5",
        "echoplus": "0:fc:8b:84:22:10",
        "echospot": "5c:41:5a:29:ad:97",
        "firetv": "cc:f7:35:25:af:4d",
        "google-home": "54:60:9:6f:32:84",
        "google-home-mini": "20:df:b9:13:e5:2e",
        "honeywell-thermostat": "b8:2c:a0:28:3e:6b",
        "insteon-hub": "0:e:f3:2c:d4:4",
        "iphone": "c8:d0:83:21:3d:4b",
        "lightify-hub": "84:18:26:7c:1a:56",
        "magichome-strip": "dc:4f:22:89:fc:e7",
        "nest-tstat": "64:16:66:2a:98:62",
        "netatmo-weather-station": "70:ee:50:36:98:da",
        "nexus5x3": "64:bc:c:80:7e:1f",
        "ring-doorbell": "f0:45:da:36:e6:23",
        "roku-tv": "c8:3a:6b:fa:1c:0",
        "samsungtv-wifi": "64:1c:ae:50:57:2a",
        "samsungtv-wired": "fc:3:9f:93:22:62",
        "sengled-hub": "b0:ce:18:20:43:bf",
        "smarter-coffee-mach": "c:2a:69:11:1:ba",
        "smartthings-hub": "d0:52:a8:a4:e6:46",
        "sousvide": "68:c6:3a:ba:c2:6b",
        "t-philips-hub": "ec:b5:fa:0:98:da",
        "t-wemo-plug": "58:ef:68:99:7d:ed",
        "tplink-bulb": "50:c7:bf:ca:3f:9d",
        "tplink-plug": "50:c7:bf:b1:d2:78",
        "tplink-plug2": "b0:be:76:be:f2:aa",
        "wansview-cam-wifi": "14:6b:9c:c6:ec:a6",
        "wansview-cam-wired": "78:a5:dd:28:a1:b7",
        "xiaomi-cam1": "78:11:dc:76:a7:8",
        "xiaomi-cam2": "78:11:dc:76:69:b0",
        "xiaomi-cleaner": "78:11:dc:ec:a3:ab",
        "xiaomi-hub": "7c:49:eb:88:da:82",
        "xiaomi-plug": "7c:49:eb:22:30:9c",
        "yi-camera": "c:8c:24:b:be:fb",
    },
    "us": {
        "amcrest-cam-wifi": "9c:8e:cd:a:33:5f",
        "amcrest-cam-wired": "9c:8e:cd:a:33:1b",
        "appletv": "8:66:98:a2:21:9e",
        "blink-camera": "f4:b8:5e:31:73:db",
        "blink-security-hub": "0:3:7f:4f:c6:b5",
        "brewer": "20:f8:5e:cc:18:1f",
        "bulb1": "ec:fa:bc:82:20:bb",
        "cloudcam": "b0:fc:d:c9:0:4c",
        "dishwasher": "b4:e6:2a:27:34:b7",
        "dlink-mov": "6c:72:20:c5:a:3f",
        "dryer": "c0:97:27:73:aa:38",
        "echodot": "18:74:2e:41:4d:35",
        "echoplus": "fc:a1:83:38:e0:2d",
        "echospot": "0:71:47:c0:91:93",
        "firetv": "6c:56:97:35:39:f4",
        "fridge": "70:2c:1f:3b:36:53",
        "galaxytab-a": "d4:e6:b7:43:d5:e7",
        "google-home-mini": "20:df:b9:5f:41:7e",
        "google-home-mini2": "44:7:b:50:4d:df",
        "ikettle": "c:2a:69:e:91:16",
        "insteon-hub": "0:e:f3:3b:85:e5",
        "invoke": "d8:f7:10:c3:34:e4",
        "ipad": "e4:e0:a6:3c:3b:d1",
        "iphone": "f0:db:e2:f2:79:2e",
        "iphone-daniel": "84:8e:c:71:8:70",
        "iphone7-gray": "88:6b:6e:4c:12:9b",
        "iphone7-pink": "d4:61:9d:ed:fb:c3",
        "labelprinter": "f8:da:c:7b:a:8f",
        "lefun-cam-wifi": "0:c:43:27:4f:c1",
        "lefun-cam-wired": "ae:ca:6:8:d3:e6",
        "lgtv-wifi": "b4:e6:2a:8c:a2:c2",
        "lgtv-wired": "38:8c:50:68:d7:5c",
        "lightify-hub": "84:18:26:7d:cf:a2",
        "luohe-spycam": "0:c:43:20:32:bb",
        "magichome-strip": "dc:4f:22:c1:58:5",
        "microseven-camera": "0:fc:5c:e0:81:86",
        "microwave": "d8:28:c9:10:b5:60",
        "nest-tstat": "18:b4:30:c8:d8:28",
        "nexus5x1": "64:bc:c:2c:5a:54",
        "nexus5x2": "64:bc:c:2c:5a:af",
        "nexus5x3": "64:bc:c:2c:5a:42",
        "nexus5x4": "64:bc:c:6a:81:f3",
        "nexus5x5": "64:bc:c:2c:59:b9",
        "nexus5x6": "64:bc:c:66:23:5f",
        "nexus6": "f8:cf:c5:c9:38:f0",
        "nexus6p2": "bc:75:74:39:96:9e",
        "philips-bulb": "34:ce:0:99:9b:83",
        "ring-doorbell": "98:84:e3:e4:35:bd",
        "roku-tv": "88:de:a9:8:3:b9",
        "samsungtv-wifi": "68:27:37:52:31:6",
        "samsungtv-wired": "84:c0:ef:2f:42:cc",
        "sengled-hub": "b0:ce:18:27:9f:e4",
        "sengled-hub-spoofed": "b0:ce:18:27:9f:e5",
        "smartthings-hub": "24:fd:5b:4:1b:75",
        "sousvide": "dc:4f:22:28:b6:5b",
        "t-echodot": "fc:65:de:5f:15:a",
        "t-philips-hub": "0:17:88:68:5f:61",
        "t-smartthings-hub": "24:fd:5b:2:1d:3a",
        "t-wemo-plug": "14:91:82:b4:4b:5f",
        "tplink-bulb": "50:c7:bf:a0:f3:76",
        "tplink-plug": "50:c7:bf:5a:2e:a0",
        "wansview-cam-wifi": "ec:3d:fd:34:b4:1b",
        "wansview-cam-wired": "78:a5:dd:1a:15:19",
        "washer": "c0:97:27:81:67:99",
        "washer-old": "c0:97:27:6c:ae:42",
        "wink-hub2": "0:21:cc:4d:ce:8c",
        "wink-hub2-wifi": "dc:ef:ca:22:b8:ff",
        "xiaomi-cam1": "34:ce:0:d6:91:e2",
        "xiaomi-cam2": "34:ce:0:d6:8f:c1",
        "xiaomi-cleaner": "f0:b4:29:41:ec:d7",
        "xiaomi-hub": "34:ce:0:83:99:35",
        "xiaomi-movingcam1": "34:ce:0:b1:2c:5e",
        "xiaomi-movingcam2": "34:ce:0:b0:1f:fb",
        "xiaomi-ricecooker": "7c:49:eb:35:7a:49",
        "xiaomi-strip": "34:ce:0:8b:22:74",
        "yi-camera": "b0:d5:9d:b9:f0:b4",
        "zmodo-doorbell": "7c:c7:9:56:6e:48",
    },
}

_ANDROID_ONOFF_DIRECTORY = re.compile(r"^android_(?P<transport>lan|wan)_(?P<polarity>on|off)$")

_POLARITY_TOKEN_TO_ACTION: dict[MoniotrPolarityToken, SemanticAction] = {
    MoniotrPolarityToken.ON: SemanticAction.TURN_ON,
    MoniotrPolarityToken.OFF: SemanticAction.TURN_OFF,
}


def physical_device_id(region_name: DirectoryName, device_name: DirectoryName) -> DeviceId:
    return DeviceId(f"{region_name.removesuffix('-vpn')}_{device_name}")


def official_target_mac(
    region_name: DirectoryName, device_name: DirectoryName
) -> TargetDeviceMac | None:
    physical_region = DirectoryName(region_name.removesuffix("-vpn"))
    devices = _OFFICIAL_TARGET_MACS.get(physical_region)
    value = devices.get(device_name) if devices is not None else None
    return TargetDeviceMac(value) if value is not None else None


def describe_raw_availability() -> DatasetAvailability:
    root = resolve_dataset_raw_root(DatasetSource.MONIOTR_IMC_2019)
    required_roots = (resolve_moniotr_interactions_root(), resolve_moniotr_idle_root())
    if not root.exists():
        return DatasetAvailability.MISSING_EXTERNAL
    if not all(Path(path).exists() for path in required_roots):
        return DatasetAvailability.PRESENT_BUT_INCOMPLETE
    return DatasetAvailability.PRESENT_AND_VALID


def _interaction_record(
    capture_path: Path,
    root: Path,
    device_id: DeviceId,
    context_id: SourceContextId,
    action: SemanticAction,
    target_device_mac: TargetDeviceMac | None,
) -> PublicSourceInteraction | None:
    if target_device_mac is None:
        return None
    relative_capture = capture_path.relative_to(root).as_posix()
    typed_capture = RepositoryPath(capture_path)
    try:
        capture_start_timestamp = read_pcap_first_packet_timestamp(typed_capture)
    except ValueError:
        return None
    return PublicSourceInteraction(
        dataset_source=DatasetSource.MONIOTR_IMC_2019,
        interaction_id=InteractionId(relative_capture),
        device_id=device_id,
        source_capture_id=SourceCaptureId(relative_capture),
        source_group_id=SourceGroupId(relative_capture),
        source_group_kind=SourceGroupKind.INDIVIDUAL_CAPTURE,
        source_context_id=context_id,
        semantic_action=action,
        intent_provenance_grade=IntentProvenanceGrade.VERIFIED_PROTOCOL,
        capture_start_timestamp=capture_start_timestamp,
        trigger_timestamp=None,
        capture_path=typed_capture,
        target_device_mac=target_device_mac,
    )


def _iter_child_directories(directory: Path) -> tuple[Path, ...]:
    return tuple(sorted(path for path in directory.iterdir() if path.is_dir()))


def _iter_action_directories(
    interactions_root: Path,
) -> tuple[tuple[Path, Path, Path], ...]:
    return tuple(
        (region_directory, device_directory, action_directory)
        for region_directory in _iter_child_directories(interactions_root)
        for device_directory in _iter_child_directories(region_directory)
        for action_directory in _iter_child_directories(device_directory)
    )


def _resolve_action_context(
    region_directory: Path, action_directory: Path
) -> tuple[SemanticAction, SourceContextId] | None:
    match = _ANDROID_ONOFF_DIRECTORY.fullmatch(action_directory.name)
    if match is None:
        return None
    try:
        polarity_token = MoniotrPolarityToken(match["polarity"])
    except ValueError:
        return None
    context = SourceContextId(f"{region_directory.name}_{match['transport']}")
    return _POLARITY_TOKEN_TO_ACTION[polarity_token], context


def _records_for_action_directory(
    interactions_root: Path, region_directory: Path, device_directory: Path, action_directory: Path
) -> tuple[PublicSourceInteraction, ...]:
    resolved = _resolve_action_context(region_directory, action_directory)
    if resolved is None:
        return ()
    action, context = resolved
    region_name = DirectoryName(region_directory.name)
    device_name = DirectoryName(device_directory.name)
    device_id = physical_device_id(region_name, device_name)
    target_device_mac = official_target_mac(region_name, device_name)
    records = (
        _interaction_record(
            capture_path, interactions_root, device_id, context, action, target_device_mac
        )
        for capture_path in sorted(action_directory.glob(f"*{RawCaptureFileSuffix.PCAP}"))
    )
    return tuple(record for record in records if record is not None)


def enumerate_raw_interactions() -> tuple[PublicSourceInteraction, ...]:
    interactions_root = Path(resolve_moniotr_interactions_root())
    if not interactions_root.exists():
        return ()
    return tuple(
        record
        for region_directory, device_directory, action_directory in _iter_action_directories(
            interactions_root
        )
        for record in _records_for_action_directory(
            interactions_root, region_directory, device_directory, action_directory
        )
    )
