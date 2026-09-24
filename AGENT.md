# VietHandOCR Agent Guide

## 1. Project Overview
VietHandOCR is an end-to-end deep learning pipeline designed for robust Vietnamese handwriting recognition. It employs a hybrid methodology that bridges traditional Digital Image Processing (DIP) heuristics for computationally efficient standardization with a state-of-the-art Sequence-to-Sequence neural architecture, culminating in an IEEE-formatted research paper.

## 2. Tech Stack
- **Language/Frameworks**: Python, PyTorch
- **Core Models/Libraries**: VietOCR, OpenCV
- **MLOps**: Weights & Biases (W&B)
- **Environment**: Kaggle Notebooks (Dual NVIDIA T4 GPUs)
- **Publishing**: LaTeX (via Markdown drafts)

## 3. Dev Commands
This project relies on a Kaggle Notebook environment rather than local CLI scripts.
- **Setup Dependencies**: The environment assumes standard Kaggle packages. Install project-specific dependencies directly within the notebook cells using: `pip install -q vietocr wandb onnx`
- **Execution Pipeline**: Developers should upload the project notebooks to Kaggle and execute them sequentially by clicking "Run All":
  1. Run `01_Data_Preparation_and_EDA.ipynb`
  2. Run `02_Baseline_Evaluation.ipynb` (Zero-shot baseline)
  3. Run `03_Digital_Image_Processing.ipynb` (DIP Preprocessing)
  4. Run `04_VietOCR_Training.ipynb` (Training loop with W&B tracking)
  5. Run `05_Evaluation_and_Inference.ipynb` (Evaluation and ONNX export)

## 4. Core Logic Summary
The pipeline strictly enforces a **Writer-Independent split** on training data to prevent leakage. Raw images then pass through a deterministic **DIP Pipeline** (illumination correction, binarization, skew correction, and horizontal projection profiles) to normalize the input manifold. These standardized images are fed into a fine-tuned **VGG19 + Transformer** architecture (via VietOCR). The final outputs, alongside rigorous evaluation metrics, are documented in an **IEEE Paper generation** process.

## 5. Key Constraints
- Do not modify the original UIT-HWDB zip files directly.
- Keep the predefined `test_data` set exactly as is for evaluation; only apply the 90/10 Writer-Independent split to the `train_data`.
- Writer-Independent splitting is mandatory; do not use random splitting.
- Do not change the core VGG19+Transformer architecture without explicit approval.
- Paragraph segmentation must use traditional DIP (Projection Profiles), not deep learning.
- Code must adhere to Kaggle resource limits (Dual T4, memory management via `gc.collect()`).
- **Branch Management**: Before adding any features or fixing bugs, always work on a new git branch. Never commit directly on main. Bug branches must follow naming convention `bug/[desc]`, feature branches follow naming convention `feature/[desc]`

## 6. Additional Documentation
For deep technical details, refer to the progressive disclosure documentation located in the `.agent/docs/` directory:
- [Data Ingestion & Splitting](.agent/docs/data_ingestion.md)
- [Preprocessing Pipeline (DIP)](.agent/docs/preprocessing_pipeline.md)
- [Model Architecture](.agent/docs/model_architecture.md)
- [Research Paper Structure](.agent/docs/paper_structure.md)
- [AI Guidelines & Human-in-the-Loop Context](.agent/docs/ai_guidelines.md)
