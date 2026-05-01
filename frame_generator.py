from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np

ShapeType = Literal["circle", "square", "hexagon"]


@dataclass
class FrameParams:
    shape: ShapeType = "circle"
    width_mm: float = 200
    height_mm: float = 200
    frame_height_mm: float = 10
    thickness_mm: float = 10
    layer_height: float = 0.2


def generate_frame_paths(params: FrameParams) -> list[list[tuple[float, float, float]]]:
    layers = max(1, int(params.frame_height_mm / params.layer_height))
    paths: list[list[tuple[float, float, float]]] = []
    for li in range(layers):
        z = (li + 1) * params.layer_height
        if params.shape == "circle":
            r_outer = min(params.width_mm, params.height_mm) / 2
            r_inner = max(1.0, r_outer - params.thickness_mm)
            for r in np.linspace(r_outer, r_inner, 6):
                a = np.linspace(0, 2 * np.pi, 120, endpoint=True)
                paths.append([(params.width_mm / 2 + r * np.cos(t), params.height_mm / 2 + r * np.sin(t), z) for t in a])
        else:
            w, h = params.width_mm, params.height_mm
            inset_vals = np.linspace(0, params.thickness_mm, 6)
            for inset in inset_vals:
                if params.shape == "square":
                    p = [(inset, inset, z), (w - inset, inset, z), (w - inset, h - inset, z), (inset, h - inset, z), (inset, inset, z)]
                else:
                    r = min(w, h) / 2 - inset
                    a = np.linspace(0, 2 * np.pi, 7, endpoint=True)
                    p = [(w / 2 + r * np.cos(t), h / 2 + r * np.sin(t), z) for t in a]
                paths.append(p)
    return paths
