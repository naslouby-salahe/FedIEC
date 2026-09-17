from __future__ import annotations

import ast

from fediec.types import (
    DeviceId,
    FiniteFloat,
    NonNegativeFloat,
    NonNegativeInt,
    OpenUnitInterval,
    PositiveFloat,
    PositiveInt,
    SignedInt,
    UnitInterval,
)


def primitive_input(value: int) -> None:
    del value


def primitive_output() -> str:
    return "primitive"


def primitive_multiple_inputs(device_id: DeviceId, score: float) -> None:
    del device_id, score


async def primitive_async_input(value: int) -> float:
    return float(value)


def nested_primitive_input(values: tuple[int, ...]) -> None:
    del values


def nested_primitive_output() -> list[str]:
    return []


def generic_alias_input(value: NonNegativeInt) -> None:
    del value


def generic_alias_inputs(
    finite: FiniteFloat,
    non_negative_float: NonNegativeFloat,
    open_interval: OpenUnitInterval,
    positive_float: PositiveFloat,
    positive_int: PositiveInt,
    signed: SignedInt,
    interval: UnitInterval,
) -> None:
    del (
        finite,
        non_negative_float,
        open_interval,
        positive_float,
        positive_int,
        signed,
        interval,
    )


PHYSICAL_COLLECTION_MARKER = "gateway_capture"


def stale_gateway_capture() -> None:  # type: ignore
    ast.parse("pass")
