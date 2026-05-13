from __future__ import annotations

import json
import sys
from dataclasses import asdict

from PyQt6.QtWidgets import (
    QApplication, QFileDialog, QHBoxLayout, QLabel, QMainWindow, QPushButton,
    QSpinBox, QDoubleSpinBox, QComboBox, QTextEdit, QVBoxLayout, QWidget
)

from frame_generator import FrameParams, generate_frame_paths
from gcode_generator import PrintParams, generate_z_sequence, gcode_for_paths
from image_processing import ImageProcessor, ImageSettings
from preview import plot_2d
from string_generator import StringArtParams, greedy_string_art


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D String Art Generator")
        self.image = None
        self.target = None
        self.points = None
        self.lines = []

        root = QWidget(); self.setCentralWidget(root)
        layout = QHBoxLayout(root)

        left = QVBoxLayout(); center = QVBoxLayout(); right = QVBoxLayout()
        layout.addLayout(left, 2); layout.addLayout(center, 3); layout.addLayout(right, 2)

        self.shape = QComboBox(); self.shape.addItems(["circle", "square", "hexagon"])
        self.points_n = QSpinBox(); self.points_n.setRange(50, 1000); self.points_n.setValue(300)
        self.lines_n = QSpinBox(); self.lines_n.setRange(100, 10000); self.lines_n.setValue(2000)
        self.size = QDoubleSpinBox(); self.size.setRange(50, 500); self.size.setValue(200)

        b_load = QPushButton("Load Image")
        b_gen = QPushButton("Generate")
        b_export = QPushButton("Export G-code/JSON/PNG")

        for w in [QLabel("Shape"), self.shape, QLabel("Points"), self.points_n, QLabel("Lines"), self.lines_n,
                  QLabel("Frame size (mm)"), self.size, b_load, b_gen, b_export]:
            left.addWidget(w)

        self.stats = QTextEdit(); self.stats.setReadOnly(True)
        right.addWidget(QLabel("Statistics")); right.addWidget(self.stats)
        center.addWidget(QLabel("Preview saved as preview.png after Generate"))

        b_load.clicked.connect(self.load_image)
        b_gen.clicked.connect(self.generate)
        b_export.clicked.connect(self.export_all)

    def load_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open", "", "Images (*.png *.jpg *.jpeg)")
        if not path:
            return
        self.image = ImageProcessor.load_image(path)
        self.target = ImageProcessor.preprocess(self.image, ImageSettings())
        self.stats.append(f"Loaded: {path}")

    def generate(self):
        if self.target is None:
            self.stats.append("Load image first")
            return
        sp = StringArtParams(shape=self.shape.currentText(), point_count=self.points_n.value(), line_count=self.lines_n.value())
        self.points, self.lines, _ = greedy_string_art(self.target, sp)
        plot_2d(self.target, self.points, self.lines, output_path="preview.png")
        max_bridge = max((((self.points[a]-self.points[b])**2).sum() ** 0.5 for a, b in self.lines), default=0)
        est_sec = len(self.lines) * 1.2
        self.stats.append(f"Total lines: {len(self.lines)}\nEstimated print time: {est_sec/60:.1f} min\nMax bridge length: {max_bridge:.1f} mm")

    def export_all(self):
        if self.points is None:
            self.stats.append("Generate first")
            return
        fp = FrameParams(shape=self.shape.currentText(), width_mm=self.size.value(), height_mm=self.size.value())
        pp = PrintParams()
        frame_paths = generate_frame_paths(fp)
        gcode = gcode_for_paths(frame_paths, self.points, self.lines, pp)
        with open("output.gcode", "w", encoding="utf-8") as f:
            f.write(gcode)
        proj = {
            "frame": asdict(fp),
            "print": asdict(pp),
            "line_count": len(self.lines),
            "points": self.points.tolist(),
            "lines": self.lines,
            "z_sequence": generate_z_sequence(len(self.lines), pp),
        }
        with open("project.json", "w", encoding="utf-8") as f:
            json.dump(proj, f, indent=2)
        self.stats.append("Exported: output.gcode, project.json, preview.png")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow(); w.resize(1300, 750); w.show()
    sys.exit(app.exec())
