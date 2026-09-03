"""
Smoke tests for real-time-kanji-tutor repository.
Verifies package imports, default configuration, and test asset availability.
"""

import os

import cv2
import pytest

from kanji_tutor import __version__
from kanji_tutor.config import VisionConfig


def test_package_metadata():
    """Verify package version and metadata."""
    assert __version__ == "0.1.0"

def test_vision_config_defaults():
    """Verify default computer vision parameters conform to 60 FPS real-time specifications."""
    config = VisionConfig()
    assert config.TARGET_FPS == 60
    assert config.FRAME_BUDGET_MS == pytest.approx(16.66, 0.01)
    assert config.CANVAS_SIZE == 128
    assert config.INK_MAX_INTENSITY == 85
    assert config.MIN_LAPLACIAN_VAR == 65.0

def test_asset_kanji_input_readable():
    """Verify experimental sample image is available in assets/ and decodable by OpenCV."""
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    asset_path = os.path.join(root_dir, "assets", "kanji_input.jpg")
    assert os.path.exists(asset_path), f"Asset file missing: {asset_path}"

    img = cv2.imread(asset_path, cv2.IMREAD_GRAYSCALE)
    assert img is not None, "Failed to decode kanji_input.jpg"
    assert img.shape[0] > 0 and img.shape[1] > 0, "Invalid image dimensions"
