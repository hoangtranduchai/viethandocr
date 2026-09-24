# Model Architecture & Training Strategy

This document outlines the core deep learning architecture and MLOps strategies used to recognize Vietnamese handwriting.

## 1. Core Architecture (VietOCR)
The project leverages the **VietOCR** repository's sequence-to-sequence implementation.
- **Base Architecture**: `vgg_transformer` (VGG19 encoder with Transformer decoder).
- **Encoder**: A VGG19 backbone provides convolutional feature extraction for the visual encoder.
- **Decoder**: A **Transformer** module replaces legacy RNNs/LSTMs. Multi-head self-attention allows the model to globally context-match base characters and complex stacked diacritics simultaneously, which is critical for tonal languages like Vietnamese.

## 2. Fine-Tuning Strategy
- **Pre-trained Weights**: The model is initialized with pre-trained weights from the official VietOCR repository. This is framed as a domain-adaptation task (from printed/clean text to unconstrained handwriting), massively accelerating convergence.
- **Constraint**: Do not modify the core VGG19+Transformer architecture without explicit approval.

## 3. Training & Hardware Environment
- **Platform**: Optimized for **Kaggle Cloud Environments**.
- **Compute**: Targets **Dual NVIDIA T4 GPUs** (16GB VRAM each).
- **Optimization**: Uses Mixed Precision Training (FP16) to maximize batch sizes.
- **Memory Management**: Aggressive garbage collection (`gc.collect()`) is implemented to stay within standard Kaggle CPU/RAM limits.

## 4. MLOps & Experiment Tracking
- **Weights & Biases (W&B)**: Used exclusively for tracking hyperparameter configurations, loss curves, and system metrics during the training loop.
- **Holdout Predictions**: The training script automatically generates and saves Holdout Validation predictions on the validation set for future stacking and meta-ensembling strategies.
- **ONNX Export**: Post-training, the model weights are exported to the ONNX format to slash inference latency and prepare for potential TensorRT / INT8 quantization.


## 5. Baseline Evaluation Strategy
Before training begins, a zero-shot baseline is computed using the pre-trained `vgg_transformer` weights. This evaluation is strictly executed on all granular levels (all, word, line, paragraph) of BOTH the `test_data` split (for final reporting) and the `val_data` split (to establish an Epoch 0 anchor). The `train_data` split is excluded from baseline evaluation to save compute.

## 6. Implementation Location
Model instantiation, W&B tracking, and the primary training loop are located in `04_VietOCR_Training.ipynb`. ONNX export and inference optimization are handled in `05_Evaluation_and_Inference.ipynb`.
