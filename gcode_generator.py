from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass
class PrintParams:
    nozzle_diameter: float = 0.4
    layer_height: float = 0.2
    print_speed: float = 40.0
    travel_speed: float = 250.0
    nozzle_temperature: int = 215
    bed_temperature: int = 60
    fan_speed: int = 100
    extrusion_per_line: float = 0.01
    start_z_above_frame: float = 10.2
    max_z: float = 12.0
    z_step: float = 0.05
    max_line_length: float = 260.0


def generate_z_sequence(line_count: int, p: PrintParams):
    z_vals = np.arange(p.start_z_above_frame, p.max_z + 1e-9, p.z_step)
    zig = np.concatenate([z_vals, z_vals[::-1]])
    return [float(zig[i % len(zig)]) for i in range(line_count)]


def gcode_for_paths(frame_paths, points, lines, pp: PrintParams) -> str:
    out = [
        "; 3D String Art Generator",
        "G21",
        "G90",
        "M82",
        f"M104 S{pp.nozzle_temperature}",
        f"M140 S{pp.bed_temperature}",
        f"M106 S{int(255*pp.fan_speed/100)}",
        "G28",
        "G92 E0",
    ]
    e = 0.0
    for path in frame_paths:
        if not path:
            continue
        x, y, z = path[0]
        out.append(f"G0 X{x:.3f} Y{y:.3f} Z{z:.3f} F{pp.travel_speed*60:.0f}")
        for x, y, z in path[1:]:
            e += pp.extrusion_per_line
            out.append(f"G1 X{x:.3f} Y{y:.3f} Z{z:.3f} E{e:.5f} F{pp.print_speed*60:.0f}")

    zseq = generate_z_sequence(len(lines), pp)
    for i, (a, b) in enumerate(lines):
        p0, p1 = points[a], points[b]
        dist = float(np.linalg.norm(p1 - p0))
        if dist > pp.max_line_length:
            out.append(f"; skipped line {a}->{b} too long: {dist:.2f}")
            continue
        z = zseq[i]
        out.append(f"G0 X{p0[0]:.3f} Y{p0[1]:.3f} Z{z:.3f} F{pp.travel_speed*60:.0f}")
        e += pp.extrusion_per_line
        out.append(f"G1 X{p1[0]:.3f} Y{p1[1]:.3f} Z{z:.3f} E{e:.5f} F{pp.print_speed*60:.0f}")

    out += ["M104 S0", "M140 S0", "M107", "G28 X0", "M84"]
    return "\n".join(out) + "\n"
