## Description
Brief summary of the changes proposed in this Pull Request.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds CV functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Performance improvement (reducing per-frame latency)

## Computer Vision Stages Modified
- [ ] Stage 0: Calibration & Homography
- [ ] Stage 1: Acquisition & ROI Slicing
- [ ] Stage 2: Photometric IQA & Gaussian Filtering
- [ ] Stage 3: Motion Segmentation & Shadow Rejection
- [ ] Stage 4: Morphology & Connected Components
- [ ] Stage 5: Centroid Tracking & Canvas Rectification
- [ ] Stage 6: Stroke Dynamics & Classification
- [ ] UI / HUD Dashboard

## Checklist
- [ ] My code follows the code style of this project (`ruff check .` passes).
- [ ] I have added tests that prove my fix is effective or that my feature works.
- [ ] All existing and new tests pass locally (`pytest tests/`).
- [ ] I have benchmarked my changes to ensure latency remains within the $16.66\text{ ms}$ budget ($60\text{ FPS}$).
- [ ] I have updated relevant documentation in `docs/` or `README.md`.
