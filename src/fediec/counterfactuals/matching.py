from __future__ import annotations

from fediec.enums import MatchingTier
from fediec.types import (
    Distance,
    DonorCandidate,
    MatchingCaliper,
    Quantile,
    SemanticAction,
    TierRank,
)


def compute_caliper(
    training_context_distances: tuple[Distance, ...],
    semantic_action: SemanticAction,
    quantile: Quantile,
) -> MatchingCaliper:
    if not training_context_distances:
        raise ValueError("a matching caliper requires at least one training context distance")
    ordered = sorted(training_context_distances)
    index = round((len(ordered) - 1) * quantile)
    return MatchingCaliper(
        semantic_action=semantic_action,
        caliper_quantile=quantile,
        caliper_value=ordered[index],
    )


_TIER_ORDER: dict[MatchingTier, TierRank] = {
    MatchingTier.TIER_1_SAME_SOURCE_GROUP: 0,
    MatchingTier.TIER_2_NEAREST_DISTINCT_SOURCE_GROUP: 1,
    MatchingTier.TIER_3_OTHER_ELIGIBLE_SOURCE_GROUP: 2,
}


def rank_donor_candidates(candidates: tuple[DonorCandidate, ...]) -> tuple[DonorCandidate, ...]:
    def sort_key(candidate: DonorCandidate) -> tuple[TierRank, Distance]:
        return (_TIER_ORDER[candidate.matching_tier], candidate.context_distance)

    return tuple(sorted(candidates, key=sort_key))


def within_caliper(caliper: MatchingCaliper, candidate: DonorCandidate) -> bool:
    return candidate.context_distance <= caliper.caliper_value
