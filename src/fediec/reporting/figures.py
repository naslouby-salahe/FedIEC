from __future__ import annotations

from pathlib import Path

from fediec.types import EffectSize, PairedEffectEstimate, RepositoryPath, SvgMarkup

_WIDTH = 320
_HEIGHT = 200
_MARGIN = 30


def _bar_svg(values: tuple[EffectSize, ...]) -> SvgMarkup:
    if not values:
        return SvgMarkup("")
    plot_width = _WIDTH - 2 * _MARGIN
    plot_height = _HEIGHT - 2 * _MARGIN
    magnitude = max(abs(value) for value in values) or 1.0
    bar_width = plot_width / len(values)
    zero_y = _MARGIN + plot_height / 2
    bars: list[SvgMarkup] = []
    for index, value in enumerate(values):
        bar_height = abs(value) / magnitude * (plot_height / 2)
        x = _MARGIN + index * bar_width + bar_width * 0.1
        y = zero_y if value >= 0 else zero_y - bar_height
        bars.append(
            SvgMarkup(
                f'<rect x="{x:.2f}" y="{y:.2f}" width="{bar_width * 0.8:.2f}" '
                f'height="{bar_height:.2f}" fill="#3366cc"/>'
            )
        )
    return SvgMarkup("".join(bars))


def write_paired_effect_by_seed_figure(
    estimate: PairedEffectEstimate, path: RepositoryPath
) -> None:
    zero_y = _MARGIN + (_HEIGHT - 2 * _MARGIN) / 2
    title = f"{estimate.left_method} vs {estimate.right_method}"
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{_WIDTH}" height="{_HEIGHT}" '
        f'viewBox="0 0 {_WIDTH} {_HEIGHT}">'
        f'<text x="{_MARGIN}" y="16" font-size="10">{title}</text>'
        f'<line x1="{_MARGIN}" y1="{zero_y:.2f}" x2="{_WIDTH - _MARGIN}" y2="{zero_y:.2f}" '
        f'stroke="black" stroke-width="0.5"/>'
        f"{_bar_svg(estimate.seed_effects)}"
        "</svg>"
    )
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(svg, encoding="utf-8")
