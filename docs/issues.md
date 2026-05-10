# Issues and Fixes

## Purpose
This file tracks technical, data, and reproducibility issues encountered during the project.

---

## Issue Template

##  Issue Title:
### Date:
### Reported by:
### Related file / script:
### Description:
### Possible cause:
### Attempted fix:
### Status:
- [ ] Open
- [ ] In progress
- [ ] Resolved

### Notes:

---
##  Issue Title:
Missing full-text data required for topic modelling

### Date:
2026-04-06

### Reported by:
Lei Hu

### Related file / script:
datasets/theguardian/data_guardian.json
scripts/bertopic/bert_grid_guardian.py

### Description:
The original repository only provided metadata files containing URLs, dates, and sections, but did not include the full article text required for BERTopic modeling.

However, the modeling scripts expected fields such as:
- title
- content.body
- selftext
- cleaned text

This caused the original scripts to fail during data loading and preprocessing.

### Possible cause:
The authors likely used locally stored recovered datasets that were not included in the public repository.

### Attempted fix:
Recovered Guardian article text using the Guardian API and converted the recovered records into a model-ready JSONL format.

### Status:
- [x] Resolved

### Notes:
This issue became one of the main reproducibility challenges in the project.

---
##  Issue Title:
Hard-coded absolute file paths prevented reproduction

### Date:
2026-04-06

### Reported by:
Lei Hu

### Related file / script:
scripts/bertopic/bert_grid_guardian.py

### Description:
Several scripts used Linux-specific absolute paths such as:

/home/yy2046/Workspace/DCEE2023/...

These paths did not exist on other systems and caused immediate file loading failures.

### Possible cause:
The original experiments were developed on a local machine without converting paths into portable relative paths before publication.

### Attempted fix:
Replaced all absolute paths with relative project paths using pathlib.

### Status:
- [x] Resolved

### Notes:
Using relative paths significantly improved cross-platform reproducibility.

---
##  Issue Title:
BERTopic topic quality instability across preprocessing configurations

### Date:
2026-05-10

### Reported by:
Hulei

### Related file / script:
scripts/modeling/simple_bertopic_guardian_v2.py

### Description:
Small preprocessing and clustering parameter changes produced substantially different topic structures.

Early reproduction attempts generated only two overly broad topics with weak semantic separation.

### Possible cause:
BERTopic is highly sensitive to:
- preprocessing quality
- stopword filtering
- clustering hyperparameters
- dimensionality reduction settings
- corpus size and document quality

### Attempted fix:
Introduced:
- custom stopword filtering
- lemmatization
- reproducible UMAP settings
- smaller topic size thresholds
- improved preprocessing workflow

### Status:
- [x] Resolved

### Notes:
Although topic quality improved substantially, the reproduced topics still differed from those described in the original paper.