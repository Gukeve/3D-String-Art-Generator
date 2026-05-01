from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np

ShapeType = Literal["circle", "square", "hexagon"]


@dataclass
class StringArtParams:
    shape: ShapeType = "circle"
    point_count: int = 300
    line_count: int = 1500
    min_jump: int = 10


def generate_perimeter_points(shape: ShapeType, count: int, size_mm: tuple[float, float]) -> np.ndarray:
    w, h = size_mm
    cx, cy = w / 2.0, h / 2.0
    if shape == "circle":
        r = min(w, h) * 0.5
        a = np.linspace(0, 2 * np.pi, count, endpoint=False)
        return np.column_stack([cx + r * np.cos(a), cy + r * np.sin(a)])

    if shape == "square":
        pts = []
        for i in range(count):
            t = i / count * 4
            s = t % 1
            edge = int(t)
            if edge == 0:
                pts.append((s * w, 0))
            elif edge == 1:
                pts.append((w, s * h))
            elif edge == 2:
                pts.append((w * (1 - s), h))
            else:
                pts.append((0, h * (1 - s)))
        return np.array(pts)

    angles = np.linspace(0, 2 * np.pi, 7)[:-1]
    r = min(w, h) * 0.5
    verts = np.column_stack([cx + r * np.cos(angles), cy + r * np.sin(angles)])
    pts = []
    for i in range(count):
        t = i / count * 6
        e = int(t)
        s = t % 1
        p0, p1 = verts[e], verts[(e + 1) % 6]
        pts.append(p0 * (1 - s) + p1 * s)
    return np.array(pts)


def _draw_line(mask: np.ndarray, p0: np.ndarray, p1: np.ndarray, value: float = 0.05) -> None:
    n = int(np.linalg.norm(p1 - p0) * 2) + 1
    xs = np.linspace(p0[0], p1[0], n).astype(int)
    ys = np.linspace(p0[1], p1[1], n).astype(int)
    valid = (xs >= 0) & (ys >= 0) & (xs < mask.shape[1]) & (ys < mask.shape[0])
    mask[ys[valid], xs[valid]] = np.clip(mask[ys[valid], xs[valid]] + value, 0.0, 1.0)


def greedy_string_art(target: np.ndarray, params: StringArtParams):
    points_img = generate_perimeter_points(params.shape, params.point_count, (target.shape[1] - 1, target.shape[0] - 1))
    canvas = np.zeros_like(target, dtype=np.float32)
    lines: list[tuple[int, int]] = []
    current = 0
    for _ in range(params.line_count):
        best_idx = None
        best_err = 1e9
        for nxt in range(params.point_count):
            if nxt == current or abs(nxt - current) < params.min_jump:
                continue
            test = canvas.copy()
            _draw_line(test, points_img[current], points_img[nxt])
            err = np.mean((target - test) ** 2)
            if err < best_err:
                best_err = err
                best_idx = nxt
        if best_idx is None:
            continue
        _draw_line(canvas, points_img[current], points_img[best_idx])
        lines.append((current, best_idx))
        current = best_idx
    return points_img, lines, canvas
