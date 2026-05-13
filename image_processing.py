from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance, ImageOps


@dataclass
class ImageSettings:
    brightness: float = 1.0
    contrast: float = 1.0
    invert: bool = False
    opacity_simulation: float = 1.0


class ImageProcessor:
    SUPPORTED = {".png", ".jpg", ".jpeg"}

    @staticmethod
    def load_image(path: str | Path) -> Image.Image:
        p = Path(path)
        if p.suffix.lower() not in ImageProcessor.SUPPORTED:
            raise ValueError(f"Unsupported format: {p.suffix}")
        return Image.open(p).convert("RGB")

    @staticmethod
    def preprocess(image: Image.Image, settings: ImageSettings, target_size: int = 512) -> np.ndarray:
        img = image.convert("L")
        img = ImageEnhance.Brightness(img).enhance(settings.brightness)
        img = ImageEnhance.Contrast(img).enhance(settings.contrast)
        if settings.invert:
            img = ImageOps.invert(img)
        img = img.resize((target_size, target_size), Image.Resampling.LANCZOS)
        arr = np.asarray(img, dtype=np.float32) / 255.0
        arr = np.clip(arr * settings.opacity_simulation, 0.0, 1.0)
        return arr
