# Preprocessing Pipeline (Digital Image Processing)

This document outlines the standard Digital Image Processing (DIP) pipeline applied to all images prior to model inference. It relies heavily on techniques from Gonzalez's "Digital Image Processing."

## 1. Core Principles
The pipeline avoids deep-learning based segmentation (e.g., CRAFT) in favor of computationally efficient, deterministic algorithms. This drastically reduces the overhead needed for preprocessing while standardizing the inputs to simplify the neural network's learning manifold.

## 2. Pipeline Stages
1. **Illumination Correction**: 
   - **Method**: Contrast Limited Adaptive Histogram Equalization (CLAHE).
   - **Purpose**: Counters gradient lighting and uneven illumination commonly found in smartphone photos of handwritten text.

2. **Adaptive Binarization**:
   - **Method**: Adaptive Gaussian Thresholding.
   - **Purpose**: Global thresholding (like Otsu's) fails under varying illumination. This method calculates the threshold for small, localized regions based on a Gaussian-weighted mean, robustly separating ink strokes from the background.

3. **Morphological Noise Reduction**:
   - **Method**: Morphological Opening (Erosion followed by Dilation).
   - **Purpose**: Eliminates isolated "salt-and-pepper" artifacts (e.g., dust, paper imperfections) using a small structured kernel (e.g., 2x2).

4. **Skew Correction**:
   - **Method**: Canny Edge Detection paired with Hough Line Transforms.
   - **Purpose**: Detects the angle of the text baselines and rotates the image to a standardized horizontal orientation.

5. **Paragraph Segmentation**:
   - **Method**: Horizontal Projection Profiles.
   - **Constraint**: Deep learning solutions are explicitly forbidden here due to compute costs.
   - **Logic**: By projecting binary pixel intensities horizontally, text lines appear as peaks and line spacing as valleys. A heuristic threshold is applied to these valleys to crop paragraph images into single lines.

## 3. Implementation Location
The complete pipeline is implemented and executed within `02_Digital_Image_Processing.ipynb`. It includes a unified function that runs the sequence above, and a batch processing loop that reads the raw `.txt` annotations, processes every image, saves the standardized images to a `Processed_Datasets/` directory, and outputs updated annotation files (e.g., `processed_train.txt`) for training.
