from __future__ import annotations

import torch
from torch import Tensor

from fediec.config import load_config


def calibration_threshold(clean_calibration_scores: Tensor) -> Tensor:
    if clean_calibration_scores.ndim != 1 or clean_calibration_scores.shape[0] == 0:
        raise ValueError("threshold calibration requires clean one-dimensional score observations")
    return torch.quantile(clean_calibration_scores, load_config().calibration.threshold_quantile)
