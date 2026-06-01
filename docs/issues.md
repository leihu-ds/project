
# Reproducibility Issues

## Summary Table

| Issue                          | Description                                                                                                                  | Impact                                                                                         | Action Taken                                                                               | Status             |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ | ------------------ |
| Missing full-text data         | The released repository data mainly contained metadata such as URLs, IDs, dates, and sections.                               | The original topic modelling scripts could not run directly.                                   | The team recovered usable text data and documented the limitation.                         | Partially resolved |
| Metadata-only records          | The initial record counts were much larger than the final modelling datasets because most records did not contain full text. | Dataset size could be misleading if metadata records were confused with model-ready documents. | The team documented the difference between metadata records and final model-ready records. | Documented         |
| Hard-coded file paths          | Some scripts expected local absolute paths from the original author's machine.                                               | Scripts failed on other machines.                                                              | Paths were documented and replaced or avoided in the local workflow.                       | Partially resolved |
| Dependency conflicts           | Some package versions were difficult to install consistently.                                                                | Environment setup was unstable.                                                                | Python 3.8 and key package fixes were documented.                                          | Documented         |
| Missing preprocessing details  | The original cleaning pipeline was not fully documented.                                                                     | Exact reproduction of the original corpus was not possible.                                    | A transparent local cleaning workflow was added.                                           | Partially resolved |
| Non-identical recovered corpus | The recovered data may not match the original paper dataset.                                                                 | Results are comparable but not identical.                                                      | The project reports partial reproduction rather than full replication.                     | Limitation         |
| Twitter/X short-text noise     | Twitter/X posts were short, sparse, and hashtag-heavy.                                                                       | C_NPMI remained low even after filtering.                                                      | Additional filtering and qualitative interpretation were used.                             | Limitation         |

## Main Conclusion

The main reproducibility problem was not the topic modelling algorithm itself, but the gap between the released metadata files and the full cleaned text corpus required for topic modelling. Because of this, the project should be described as a partial reproduction rather than an exact replication.

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
