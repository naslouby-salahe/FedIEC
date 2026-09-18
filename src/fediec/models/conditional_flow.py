from __future__ import annotations

import torch
from torch import Tensor, nn

from fediec.config import load_config
from fediec.enums import SemanticAction

_INTENT_DIMENSION = 3


def encode_intent(intent: SemanticAction) -> Tensor:
    index = tuple(SemanticAction).index(intent)
    return torch.nn.functional.one_hot(torch.tensor(index), num_classes=_INTENT_DIMENSION).float()


class ConditionalInteractionFlow(nn.Module):
    def __init__(self, target_dimension: int, coupling_blocks: int, hidden_units: int) -> None:
        super().__init__()
        if target_dimension < 1:
            raise ValueError("conditional flow target dimension must be positive")
        self.target_dimension = target_dimension
        self.context_dimension = _INTENT_DIMENSION
        self.blocks = nn.ModuleList(
            _AffineCouplingBlock(
                target_dimension=self.target_dimension,
                context_dimension=self.context_dimension,
                hidden_units=hidden_units,
                invert_mask=block_index % 2 == 1,
            )
            for block_index in range(coupling_blocks)
        )

    def log_probability(self, interaction: Tensor, intent_condition: Tensor) -> Tensor:
        if interaction.ndim != 2 or interaction.shape[1] != self.target_dimension:
            raise ValueError(f"interaction target must have shape [batch, {self.target_dimension}]")
        if intent_condition.ndim != 2 or intent_condition.shape[1] != self.context_dimension:
            raise ValueError("intent condition must have shape [batch, 3]")
        transformed = interaction
        log_determinant = torch.zeros(interaction.shape[0], device=interaction.device)
        for block in self.blocks:
            transformed, block_log_determinant = block(transformed, intent_condition)
            log_determinant += block_log_determinant
        normalizer = torch.log(torch.tensor(2.0 * torch.pi, device=interaction.device))
        return -0.5 * (transformed.square() + normalizer).sum(dim=1) + log_determinant

    def anomaly_score(self, interaction: Tensor, intent_condition: Tensor) -> Tensor:
        return -self.log_probability(interaction, intent_condition)


def build_conditional_interaction_flow() -> ConditionalInteractionFlow:
    configuration = load_config().model
    if configuration.context_dimension != _INTENT_DIMENSION:
        raise ValueError("active conditional flow requires a 3-dimensional intent context")
    return ConditionalInteractionFlow(
        target_dimension=int(configuration.interaction_dimension),
        coupling_blocks=int(configuration.coupling_blocks),
        hidden_units=int(configuration.hidden_units_per_layer),
    )


class _AffineCouplingBlock(nn.Module):
    _mask: Tensor

    def __init__(
        self,
        target_dimension: int,
        context_dimension: int,
        hidden_units: int,
        invert_mask: bool,
    ) -> None:
        super().__init__()
        base_mask = torch.tensor(
            [float(index % 2) for index in range(target_dimension)], dtype=torch.float32
        )
        self.register_buffer("_mask", 1.0 - base_mask if invert_mask else base_mask)
        self.conditioner = nn.Sequential(
            nn.Linear(target_dimension + context_dimension, hidden_units),
            nn.ReLU(),
            nn.Linear(hidden_units, hidden_units),
            nn.ReLU(),
            nn.Linear(hidden_units, target_dimension * 2),
        )

    def forward(self, interaction: Tensor, intent_condition: Tensor) -> tuple[Tensor, Tensor]:
        masked = interaction * self._mask
        raw_scale, translation = self.conditioner(
            torch.cat((masked, intent_condition), dim=1)
        ).chunk(2, dim=1)
        bounded_log_scale = torch.tanh(raw_scale) * (1.0 - self._mask)
        transformed = masked + (1.0 - self._mask) * (
            interaction * torch.exp(bounded_log_scale) + translation
        )
        return transformed, bounded_log_scale.sum(dim=1)
