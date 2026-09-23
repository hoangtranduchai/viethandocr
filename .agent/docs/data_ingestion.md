# Data Ingestion & Splitting Strategy

This document details the first stage of the VietHandOCR pipeline, focusing on data extraction, optimization, and validation splits.

## 1. Dataset Characteristics (UIT-HWDB)
- The pipeline utilizes the **UIT-HWDB dataset**.
- Data spans three levels of granularity: **Word, Line, and Paragraph**.
- **Data Integrity Rule**: The predefined `test_data` split provided in the original dataset is kept completely untouched. This is strictly for final model evaluation and must not be used during training or hyperparameter tuning.

## 2. Writer-Independent Splitting
To prevent data leakage and evaluate the model's ability to generalize to unseen handwriting styles, a strict **Writer-Independent Split** is applied exclusively to the `train_data`.
- **Ratio**: 90% Training / 10% Validation.
- **Mechanism**: The split groups samples by `writer_id`. A random shuffle of the unique writer IDs partitions the dataset such that the 10% of writers appearing in the validation set have *no* samples in the training set.
- **Constraint**: Standard random splitting (e.g., `train_test_split` without grouping) is forbidden, as it allows the model to memorize writer-specific quirks, leading to artificially inflated validation metrics.

## 3. Memory Optimization
Given the constraints of standard Kaggle environments (e.g., 16GB CPU RAM), aggressive memory downcasting is applied to the metadata DataFrames:
- Integer columns are downcasted to `int8`, `int16`, or `int32` where appropriate.
- Float columns are downcasted to `float16` or `float32`.
- Object/string columns with low cardinality are converted to the `category` datatype.
- Garbage collection (`gc.collect()`) is used routinely to clear unreferenced variables.

## 4. Implementation Location
This logic is fully implemented and executed within `01_Data_Preparation_and_EDA.ipynb`. The final splits are saved as **12 highly granular `.txt` annotation files** formatted as `image_path	label` for native VietOCR compatibility. Specifically:
- **Combined Level (All Data)**: `train_all.txt`, `val_all.txt`, `test_all.txt`
- **Word Level**: `train_word.txt`, `val_word.txt`, `test_word.txt`
- **Line Level**: `train_line.txt`, `val_line.txt`, `test_line.txt`
- **Paragraph Level**: `train_paragraph.txt`, `val_paragraph.txt`, `test_paragraph.txt`
