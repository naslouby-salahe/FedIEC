from __future__ import annotations

from fediec.config import load_config
from fediec.enums import DatasetRole


def test_current_source_roles_are_frozen_in_runtime_configuration() -> None:
    sources = load_config().public_sources
    assert sources.moniotr_imc_2019.role is DatasetRole.PRIMARY_INTERACTION_CONTRACT
    assert (
        sources.cic_iot_2022.role
        is DatasetRole.SPARSE_REPLICATION_PROTOCOL_MODE_CONTRAST
    )
    assert (
        sources.tu_wien_philips_hue.role
        is DatasetRole.SINGLE_DEVICE_FAMILY_REPLICATION
    )
    assert sources.pingpong.role is DatasetRole.PROVENANCE_DIAGNOSTIC
