# Reproduction Log

## Purpose
This file records all reproduction attempts, configurations, outputs, and observed differences from the original paper.

---

## Entry Template

### Date:
### Member:
### Branch:
### Task:
### Dataset:
### Script / Notebook:
### Environment:
### Parameters:
### Result:
### Error / Issue:
### Output Files:
### Comparison with Paper:
### Notes:

---
## Entry 3

### Date:
2026-05-05

### Member:
Lei Hu

### Branch:
member2-data-preprocessing

### Task:
Implemented and executed a reproducible data preprocessing pipeline to standardize data preparation. 
This was necessary because the preprocessing scripts provided by Member 2 did not form a clear or unified workflow, which makes it a bit difficult to understand and reproduce the data processing steps.

### Dataset:
Guardian (processed dataset)

### Script / Notebook:
scripts/preprocessing/run_pipeline.py

### Environment:
Local machine (macOS), Conda environment (dcee), Python 3.8

### Parameters:
Default pipeline configuration (no external API calls executed)

### Result:
- Successfully inspected dataset structure
- Converted Guardian dataset into model-ready JSONL format
- Verified existence of Reddit and Twitter processed datasets
- Pipeline executed without errors

### Error / Issue:
- Original datasets only contained metadata (URLs), not usable text
- Required use of recovered text data from team member

### Output Files:
datasets/processed/guardian/guardian_model_ready.jsonl

### Comparison with Paper:
The original paper assumes access to full-text data, which was not provided. Our pipeline reconstructs the missing preprocessing step.

### Notes:
The pipeline improves reproducibility by removing hard-coded paths and standardizing data processing steps.

---
## Entry 2

### Date:
2026-04-29

### Member:
Fan Zhao

### Branch:
member4

### Task:
Created the documentation structure for tracking the reproduction process.

### Dataset:
N/A

### Script / Notebook:
N/A

### Environment:
GitHub web interface

### Parameters:
N/A

### Result:
Created the `docs` folder and added the following files:
- `reproduction_log.md`
- `issues.md`
- `results_comparison.md`
- `final_report_outline.md`

### Error / Issue:
At first, nested `docs` folders were created by mistake. The structure was then corrected so that all documentation files are now stored in one `docs` folder.

### Output Files:
- `docs/reproduction_log.md`
- `docs/issues.md`
- `docs/results_comparison.md`
- `docs/final_report_outline.md`

### Comparison with Paper:
N/A

### Notes:
The documentation structure is ready for recording reproduction attempts, issues, and comparisons with the original paper.

---
## Entry 1

### Date:
2026-04-06

### Member:
Lei Hu

### Branch:
main

### Task:
Initial environment setup, repository cloning, and dependency installation.

### Dataset:
Guardian / Reddit / Twitter (metadata only)

### Script / Notebook:
N/A

### Environment:
macOS (Apple Silicon)  
Conda environment: dcee  
Python 3.8  

### Parameters:
N/A

### Result:
- Successfully cloned the repository and created the conda environment.  
- Installed dependencies from requirements.txt.  
- Resolved compatibility issues by manually installing numpy==1.23.5 and spacy==3.5.0. Environment setup completed successfully.

### Error / Issue:
- spacy installation failed due to numpy version conflict.  
- Some packages required Python >= 3.9 while the environment used Python 3.8.  
- Initial scripts failed due to missing full-text data and incorrect file paths.

### Output Files:
N/A

### Comparison with Paper:
N/A

### Notes:
- The dataset only contains metadata (URLs, IDs) and lacks full-text data required for topic modelling.  
- Some scripts contain hard-coded absolute paths, which need to be modified for reproducibility.  
- This step prepares the environment for further preprocessing and modelling.
---
