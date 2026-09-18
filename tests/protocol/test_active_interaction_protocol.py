from __future__ import annotations

import torch

from fediec.baselines.contracts import active_baseline_contracts
from fediec.config import load_config
from fediec.datasets.moniotr_imc_2019.dataset import physical_device_id
from fediec.datasets.representation import constant_feature_indices
from fediec.enums import SemanticAction
from fediec.models.conditional_flow import build_conditional_interaction_flow, encode_intent
from fediec.types import DirectoryName


def test_active_config_has_capture_target_and_intent_only_context() -> None:
    configuration = load_config()
    assert configuration.model.interaction_dimension == 19
    assert configuration.model.context_dimension == 3
    assert configuration.federated.scarcity_budgets == (10, 30, 60)


def test_intent_encoding_is_fixed_three_state_one_hot() -> None:
    encoded = tuple(encode_intent(intent) for intent in SemanticAction)
    assert all(vector.shape == (3,) for vector in encoded)
    assert torch.equal(torch.stack(encoded).sum(dim=0), torch.ones(3))


def test_conditional_flow_accepts_only_19_d_capture_and_3_d_intent() -> None:
    model = build_conditional_interaction_flow()
    captures = torch.zeros((2, 19))
    conditions = torch.stack((encode_intent(SemanticAction.TURN_ON),) * 2)
    assert model.log_probability(captures, conditions).shape == (2,)


def test_baseline_contracts_share_the_active_target_dimension() -> None:
    contracts = active_baseline_contracts()
    assert all(contract.target_dimension == 19 for contract in contracts)
    assert (
        next(
            contract for contract in contracts if contract.condition_dimension is not None
        ).condition_dimension
        == 3
    )


def test_representation_confound_gate_identifies_constant_feature() -> None:
    vectors = ((1.0,) * 19, (2.0,) + (1.0,) * 18)
    assert constant_feature_indices(vectors) == tuple(range(1, 19))


def test_moniotr_physical_identity_keeps_sites_and_collapses_vpn_only() -> None:
    us = physical_device_id(DirectoryName("us"), DirectoryName("tplink-bulb"))
    us_vpn = physical_device_id(DirectoryName("us-vpn"), DirectoryName("tplink-bulb"))
    uk = physical_device_id(DirectoryName("uk"), DirectoryName("tplink-bulb"))
    assert us == us_vpn
    assert us != uk
