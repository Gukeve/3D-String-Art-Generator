from __future__ import annotations

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401


def plot_2d(target, points, lines, output_path: str | None = None):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(target, cmap="gray")
    ax.scatter(points[:, 0], points[:, 1], s=5, c="red")
    for a, b in lines[:3000]:
        p0, p1 = points[a], points[b]
        ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color="cyan", alpha=0.07)
    ax.set_title("2D Preview")
    if output_path:
        fig.savefig(output_path, dpi=150)
    return fig


def plot_3d(frame_paths, points, lines, zseq):
    fig = plt.figure(figsize=(7, 6))
    ax = fig.add_subplot(111, projection="3d")
    for p in frame_paths[:60]:
        xs, ys, zs = zip(*p)
        ax.plot(xs, ys, zs, c="black", alpha=0.3)
    for i, (a, b) in enumerate(lines[:2500]):
        p0, p1 = points[a], points[b]
        z = zseq[i]
        ax.plot([p0[0], p1[0]], [p0[1], p1[1]], [z, z], c="orange", alpha=0.08)
    ax.set_title("3D Print Path Preview")
    return fig
