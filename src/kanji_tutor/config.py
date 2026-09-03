"""
Configuration constants and physical thresholds for Real-Time Kanji Tutor.
Reference: Gonzalez & Woods, Digital Image Processing, 4th Edition.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class VisionConfig:
    # Target frame rate & budget
    TARGET_FPS: int = 60
    FRAME_BUDGET_MS: float = 16.66  # 1000 ms / 60 FPS

    # Canvas dimensions
    CANVAS_SIZE: int = 128          # 128x128 canonical square
    ROI_WIDTH: int = 600
    ROI_HEIGHT: int = 600

    # Photometric IQA Thresholds (Chapter 3, 6)
    MIN_HSV_V_MEAN: float = 40.0
    MAX_HSV_V_MEAN: float = 235.0
    MIN_LAPLACIAN_VAR: float = 65.0 # Sharpness threshold
    GAUSSIAN_KERNEL_SIZE: int = 3
    GAUSSIAN_SIGMA: float = 0.8

    # Physical Segmentation Thresholds (Chapter 2, 10)
    DIFF_THRESHOLD: int = 18        # Delta_t = max(0, f_{t-1} - f_t) >= 18
    INK_MAX_INTENSITY: int = 85     # Reflectance model threshold (f_t <= 85)
    SOBEL_MIN_GRADIENT: float = 30.0# Edge gradient threshold

    # Morphological & Area Constraints (Chapter 9, 11)
    MIN_INK_AREA: int = 4           # In pixels
    MAX_INK_AREA: int = 150         # In pixels

    # Trajectory & Pen-Up Dynamics (Chapter 11, 12)
    PEN_UP_FRAME_THRESHOLD: int = 10 # Frames without ink (~166 ms at 60 FPS)
    RESAMPLE_POINTS: int = 32        # Equidistant 32-point stroke representation
