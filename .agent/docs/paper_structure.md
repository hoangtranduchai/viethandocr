# Research Paper Structure

This document outlines the final deliverable of the project: a two-column IEEE-formatted research paper detailing the hybrid DIP + Deep Learning methodology.

## 1. Overview
The paper serves as a comprehensive analysis of the project's novel approach to Vietnamese Handwritten Text Recognition (HTR). It argues that traditional Digital Image Processing (DIP) heuristics remain highly relevant for standardizing unconstrained inputs, reducing the computational burden on modern Transformer networks.

## 2. Core Sections
1. **Abstract**: High-level summary of the challenges (diacritics, noise), the proposed hybrid pipeline (CLAHE, Projection Profiles + ResNet50/Transformer), and the writer-independent evaluation strategy.
2. **Introduction**: Details the difficulty of tonal Vietnamese handwriting and contrasts heavy deep-learning segmentation (CRAFT) with the proposed lightweight DIP approach.
3. **Related Work**: Reviews prior VGG+LSTM efforts, the shift towards Transformer-based OCR, and classical DIP methodologies.
4. **Methodology**: 
   - Strict Writer-Independent data splitting.
   - DIP Pipeline (CLAHE, Adaptive Thresholding, Morphological Operations).
   - Paragraph Segmentation via Horizontal Projection Profiles.
   - The VietOCR architecture (ResNet50 Encoder + Transformer Decoder) and domain-adaptation fine-tuning.
5. **Experiments and Setup**: Describes the Kaggle Dual-T4 GPU environment, AdamW optimizer, and Mixed Precision (FP16) training.
6. **Results and Discussion**: Focuses on rigorous evaluation metrics, including Character Error Rate (CER), Word Error Rate (WER), Exact Match accuracy, and BLEU scores. Error analysis explores edge cases in heavily cursive text.
7. **Conclusion**: Summarizes the reproducible pipeline and outlines future avenues like non-linear deskewing and language model integration.

## 3. Implementation Location
The full research paper draft is maintained in `VietHandOCR_Research_Paper.md`.
