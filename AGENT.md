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
The pipeline strictly enforces a **Writer-Independent split** on training data to prevent leakage. Raw images then pass through a deterministic **DIP Pipeline** (illumination correction, binarization, skew correction, and horizontal projection profiles) to normalize the input manifold. These standardized images are fed into a fine-tuned **ResNet50 + Transformer** architecture (via VietOCR). The final outputs, alongside rigorous evaluation metrics, are documented in an **IEEE Paper generation** process.

## 5. Key Constraints
- Do not modify the original UIT-HWDB zip files directly.
- Keep the predefined `test_data` set exactly as is for evaluation; only apply the 90/10 Writer-Independent split to the `train_data`.
- Writer-Independent splitting is mandatory; do not use random splitting.
- Do not change the core ResNet50+Transformer architecture without explicit approval.
- Paragraph segmentation must use traditional DIP (Projection Profiles), not deep learning.
- Code must adhere to Kaggle resource limits (Dual T4, memory management via `gc.collect()`).
- **Branch Management**: Before adding any features or fixing bugs, always work on a new git branch. Never commit directly on main. Bug branches must follow naming convention `bug/[desc]`, feature branches follow naming convention `feature/[desc]`

## 6. Additional Documentation
For deep technical details, refer to the progressive disclosure documentation located in the `.agent/docs/` directory:
- [Data Ingestion & Splitting](.agent/docs/data_ingestion.md)
- [Preprocessing Pipeline (DIP)](.agent/docs/preprocessing_pipeline.md)
- [Model Architecture](.agent/docs/model_architecture.md)
- [Research Paper Structure](.agent/docs/paper_structure.md)

## 7. Project Guidelines & AI Context (Human-in-the-Loop)
To maintain the highest standard of quality and strict adherence to the project owner's requirements, all AI agents must follow these guidelines:
- **Strict PR Workflow:** Every distinct feature or bug fix must reside in its own isolated branch and be submitted via a Pull Request. Do not mix unrelated changes.
- **Explicit Approval:** Do not modify code without first presenting a detailed Implementation Plan to the user. Execution can only begin after the user explicitly approves ("Duyệt").
- **No Hallucination:** Never fabricate information, speculate, or introduce external data not present in the project. If instructions or data are missing, stop and ask the user for clarification.
- **Relative Pathing:** All notebooks and scripts must use relative paths dynamically (e.g., via `os.walk` or `glob` inside `../input/`) to support both Kaggle and local environments seamlessly, except for `01_Data_Preparation_and_EDA.ipynb` which may use predefined paths.
- **Exhaustive Output & Detailed Logging:** All data processing notebooks must log their execution exhaustively from A to Z (from input scanning, intermediate counts, to exact output paths). Output artifacts must cover all use cases (e.g., exporting both combined and level-specific data splits) to prevent downstream manual parsing.
- **Data Split Rules:** Test data must be left 100% untouched. Train data must be strictly split into 90% Training and 10% Validation.

- **Baseline Evaluation Rule:** Baseline (Zero-shot) evaluation in `02_Baseline_Evaluation.ipynb` must be performed on BOTH the Test sets (`test_*.txt`) for official scientific reporting AND the Validation sets (`val_*.txt`) to establish an 'Epoch 0' performance anchor prior to fine-tuning. Evaluation on `train` splits is omitted to conserve Kaggle compute time.