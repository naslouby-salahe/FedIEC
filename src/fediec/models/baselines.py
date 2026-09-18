from __future__ import annotations

from dataclasses import dataclass

import numpy
from sklearn.covariance import LedoitWolf
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LogisticRegression
from sklearn.svm import OneClassSVM
from torch import Tensor

from fediec.enums import SemanticAction


@dataclass(frozen=True)
class FittedBaselines:
    action_agnostic: IsolationForest
    action_classifier: LogisticRegression
    per_action_one_class: dict[SemanticAction, OneClassSVM]
    per_action_covariance: dict[SemanticAction, LedoitWolf]


def fit_baselines(features: Tensor, actions: tuple[SemanticAction, ...]) -> FittedBaselines:
    rows = features.detach().cpu().numpy()
    labels = numpy.asarray(tuple(tuple(SemanticAction).index(action) for action in actions))
    action_agnostic = IsolationForest(random_state=0).fit(rows)
    classifier = LogisticRegression(max_iter=1000, random_state=0).fit(rows, labels)
    one_class: dict[SemanticAction, OneClassSVM] = {}
    covariance: dict[SemanticAction, LedoitWolf] = {}
    for action in (SemanticAction.TURN_ON, SemanticAction.TURN_OFF):
        action_rows = rows[labels == tuple(SemanticAction).index(action)]
        one_class[action] = OneClassSVM(gamma="scale").fit(action_rows)
        covariance[action] = LedoitWolf().fit(action_rows)
    return FittedBaselines(action_agnostic, classifier, one_class, covariance)


def action_agnostic_scores(model: FittedBaselines, features: Tensor) -> Tensor:
    return Tensor(-model.action_agnostic.score_samples(features.detach().cpu().numpy()))


def direct_action_scores(
    model: FittedBaselines, features: Tensor, actions: tuple[SemanticAction, ...]
) -> Tensor:
    probabilities = model.action_classifier.predict_proba(features.detach().cpu().numpy())
    probability_columns = tuple(
        tuple(model.action_classifier.classes_).index(tuple(SemanticAction).index(action))
        for action in actions
    )
    return Tensor(
        -numpy.log(probabilities[numpy.arange(len(probability_columns)), probability_columns])
    )


def per_action_one_class_scores(
    model: FittedBaselines, features: Tensor, actions: tuple[SemanticAction, ...]
) -> Tensor:
    rows = features.detach().cpu().numpy()
    scores = tuple(
        -model.per_action_one_class[action].score_samples(row[None, :])[0]
        for row, action in zip(rows, actions, strict=True)
    )
    return Tensor(scores)


def mahalanobis_scores(
    model: FittedBaselines, features: Tensor, actions: tuple[SemanticAction, ...]
) -> Tensor:
    rows = features.detach().cpu().numpy()
    scores = tuple(
        (row - model.per_action_covariance[action].location_)
        @ model.per_action_covariance[action].precision_
        @ (row - model.per_action_covariance[action].location_)
        for row, action in zip(rows, actions, strict=True)
    )
    return Tensor(scores)
