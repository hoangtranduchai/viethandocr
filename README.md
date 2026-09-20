# VietHandOCR

VietHandOCR is an end-to-end deep learning pipeline designed for robust Vietnamese handwriting recognition. This project bridges traditional Digital Image Processing (DIP) with state-of-the-art Sequence-to-Sequence neural architectures, culminating in an IEEE-formatted research paper.

## 🚀 Core Architecture & Logic

### 1. Data Ingestion & Splitting
- **Dataset**: Built upon the [UIT-HWDB](https://github.com/nghiangh/UIT-HWDB-dataset) dataset, supporting Word, Line, and Paragraph level annotations.
- **Data Integrity**: The predefined test set is completely isolated and kept as-is.
- **Writer-Independent Split**: To strictly prevent data leakage and evaluate true generalization, a **90% Train / 10% Validation** split is applied exclusively by grouping writer IDs, ensuring the model evaluates on unseen handwriting styles.

### 2. Digital Image Processing (DIP)
Before deep feature extraction, images are standardized using foundational techniques from Rafael Gonzalez's *"Digital Image Processing"*:
- **Illumination Correction**: CLAHE (Contrast Limited Adaptive Histogram Equalization).
- **Binarization & Noise Reduction**: Adaptive Gaussian Thresholding and Morphological Opening.
- **Skew Correction**: Canny Edge Detection coupled with Hough Line Transforms.
- **Paragraph Segmentation**: Computationally efficient Horizontal Projection Profiles to segment dense paragraphs into single text lines without heavy deep learning overhead.

### 3. Deep Learning Model (VietOCR)
- **Architecture**: Employs the `vgg_transformer` architecture from the [VietOCR](https://github.com/pbcquoc/vietocr) repository, leveraging a deep **ResNet50** backbone for spatial feature extraction and a **Transformer** sequence decoder for mapping complex Vietnamese diacritics.
- **Fine-Tuning**: Initiated with pre-trained weights to massively accelerate convergence.
- **Environment**: Optimized for Kaggle Cloud environments utilizing Dual NVIDIA T4 GPUs via Mixed Precision (FP16) training.

### 4. MLOps & Advanced Evaluation
Built to Kaggle Grandmaster standards:
- **Experiment Tracking**: Integrated with **Weights & Biases (W&B)** to log all hyperparameter tweaks and loss curves.
- **Stacking Preparedness**: Automatically saves **Out-of-Fold (OOF)** predictions on validation sets for future meta-ensembling.
- **Inference Optimization**: Includes **ONNX** exporting capabilities to drastically slash inference latency and allow for potential TensorRT / INT8 quantization.
- **Metrics**: Evaluated strictly using Character Error Rate (CER), Word Error Rate (WER), Exact Match Accuracy, and BLEU scores.

## 📁 Repository Structure
The project is decoupled into 5 modular, memory-efficient notebooks:
- `01_Data_Preparation_and_EDA.ipynb`: Data ingestion, memory downcasting, and writer-independent splitting.
- `02_Baseline_Evaluation.ipynb`: Zero-shot baseline evaluation of pre-trained model on raw data.
- `03_Digital_Image_Processing.ipynb`: The standalone DIP preprocessing pipeline.
- `04_VietOCR_Training.ipynb`: Model instantiation, W&B tracking, and the main PyTorch training loop.
- `05_Evaluation_and_Inference.ipynb`: Test set evaluation of fine-tuned model (CER/WER) and ONNX export.

## 📄 Research Paper
The culmination of this pipeline is documented in `VietHandOCR_Research_Paper.md`, drafted in standard two-column IEEE format, detailing the hybridization of classical computer vision with modern Transformers for tonal languages.
