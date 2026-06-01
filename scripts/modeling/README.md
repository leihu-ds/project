


# Member 3 — BERTopic Reproduction Workflow

# Overview

This folder contains the BERTopic modeling scripts used during the reproduction process.

The goal was not only to rerun the original paper’s topic models, but also to investigate how preprocessing choices and parameter settings affect topic quality and reproducibility.

During the project we found that the original repository did not provide a fully reproducible modeling pipeline. Sme preprocessing details, filtering steps, and cleaned datasets used in the paper were missing or undocumented. Because of this, several versions of the BERTopic workflow were created:

- baseline reproductions using the paper parameters
- improved versions with additional cleaning
- a unified reproducible pipeline for all datasets
- experiments with topic quality improvements

The scripts below reflect the progression of that work.

---

# Folder Structure

```text
├── scripts/modeling/
│   ├── run_bertopic_guardian_cleaned.py
│   ├── run_bertopic_guardian_cleaned_v2.py
│   ├── run_bertopic_reddit_cleaned.py
│   ├── run_bertopic_twitter_cleaned.py
│   ├── run_bertopic_twitter_cleaned_v2.py
│   └── run_bertopic_repro_improved.py
│
├── outputs/member3/
│   ├── *_topic_info.csv
│   ├── *_topic_words.csv
│   ├── *_document_topics.csv
│   └── *_metrics.csv
```

---

# 1. Guardian Baseline

## `run_bertopic_guardian_cleaned.py`

This was the first Guardian BERTopic reproduction attempt.

The goal of this version was simply to verify that the original modeling workflow could run successfully on the cleaned Guardian dataset using the parameter settings reported in the paper.

### Features

- uses cleaned Guardian data
- follows the BERTopic parameter settings reported in the original paper
- minimal preprocessing
- runs BERTopic directly on cleaned text

### Main settings

- n-gram: 2
- clusters: 2
- components: 5
- neighbors: 20

### Outputs

- `guardian_bertopic_topic_info.csv`
- `guardian_bertopic_topic_words.csv`
- `guardian_bertopic_document_topics.csv`

### Result

The baseline reproduction worked successfully, but the generated topics still contained a large amount of lexical noise and overlapping keywords.

Many high-frequency news terms appeared repeatedly across topics, making interpretation difficult.

---

# 2. Guardian Improved Version

## `run_bertopic_guardian_cleaned_v2.py`

This version extended the original Guardian workflow with additional preprocessing and filtering steps.

The main goal was to reduce generic news vocabulary and improve topic interpretability.

### Additional preprocessing

- custom stopword filtering
- regex cleaning
- URL removal
- generic news word filtering
- minimum document frequency filtering
- stronger text normalization

### Examples of removed words

- said
- new
- time
- people

### Outputs

- `guardian_bertopic_v2_topic_info.csv`
- `guardian_bertopic_v2_topic_words.csv`
- `guardian_bertopic_v2_document_topics.csv`

### Result

Compared to the baseline version, this workflow generally produced cleaner topic keywords and more interpretable topic clusters.

However, some topic overlap still remained, especially for broad climate and policy-related articles. This suggests that preprocessing alone was not sufficient to fully reproduce the original topic structure reported in the paper.

---

# 3. Reddit Baseline

## `run_bertopic_reddit_cleaned.py`

This script applied the parameter settings reported in the paper directly to cleaned Reddit posts.

### Features

- cleaned Reddit posts
- parameter settings reported in the paper
- BERTopic with KMeans clustering

### Main settings

- n-gram: 3
- clusters: 15
- components: 15
- neighbors: 15

### Outputs

- `reddit_bertopic_topic_info.csv`
- `reddit_bertopic_topic_words.csv`
- `reddit_bertopic_document_topics.csv`

### Result

This version produced several noisy or overlapping topics. The Reddit dataset showed strong variation in writing style, post quality, and topic focus, which made stable topic modeling more difficult than on the Guardian dataset.

---

# 4. Twitter Baseline

## `run_bertopic_twitter_cleaned.py`

This script implements a basic BERTopic reproduction workflow for Twitter data, which used recovered tweet text together with the parameter settings reported in the paper.

### Features

- recovered tweet text
- parameter settings reported in the paper
- BERTopic with KMeans clustering

### Main settings

- n-gram: 2
- clusters: 10
- components: 10
- neighbors: 10

### Outputs

- `twitter_bertopic_topic_info.csv`
- `twitter_bertopic_topic_words.csv`
- `twitter_bertopic_document_topics.csv`

### Result

This version was highly sensitive to noisy tweets, spam-like content, multilingual fragments, hashtags, and repeated usernames.

Several generated topics were dominated by non-informative tokens instead of meaningful semantic themes.

---

# 5. Twitter Improved Version

## `run_bertopic_twitter_cleaned_v2.py`

This version introduced Twitter-specific preprocessing designed to reduce common sources of noise in recovered tweet data.

### Additional preprocessing

- Twitter-specific stopword filtering
- hashtag removal
- URL removal
- multilingual token filtering
- regex cleaning
- minimum document frequency filtering

### Main goals

- reduce spam topics
- reduce repeated usernames
- reduce event-promotion noise
- improve topic stability
- improve topic interpretability

### Outputs

- `twitter_bertopic_v2_topic_info.csv`
- `twitter_bertopic_v2_topic_words.csv`
- `twitter_bertopic_v2_document_topics.csv`

### Result

This version generally produced more stable and interpretable Twitter topics.

Although some noise still remained, the overall topic quality improved noticeably compared to the baseline version.

---

# 6. Final Unified Pipeline

## `run_bertopic_repro_improved.py`

This is the final and most complete BERTopic reproduction pipeline developed during the project.

The script combines preprocessing, filtering, modeling, and evaluation into a single reproducible workflow.

### Supports

- `paper-soo`
- `paper-moo`
- `improved`
- `grid-search`

### Can run on

- Guardian
- Reddit
- Twitter
- all datasets together

### Main improvements

- duplicate removal
- platform-specific stopwords
- Twitter spam filtering
- Guardian section filtering
- CE keyword filtering
- local C_NPMI evaluation
- topic diversity evaluation

---

### Outputs

The script automatically generates output files based on:

- dataset name
- experiment mode

Example output files:

- `guardian_bertopic_improved_topic_info.csv`
- `guardian_bertopic_improved_topic_words.csv`
- `guardian_bertopic_improved_document_topics.csv`
- `guardian_bertopic_improved_metrics.csv`

- `reddit_bertopic_paper_soo_topic_info.csv`
- `twitter_bertopic_paper_moo_metrics.csv`

Generated outputs include:

- topic information
- topic keywords
- document-topic assignments
- evaluation metrics

### Result

This eventually became the main BERTopic pipeline used in the project. Compared to the earlier versions, it produced more stable results and made experiments much easier to compare across datasets, preprocessing methods, and parameter settings.

---

# Notes

Some datasets used in these experiments were recovered locally and are not uploaded to GitHub because of API restrictions, platform policies, and file size limitations.

As a result, fully reproducing all experiments may require regenerating some datasets locally.

This repository therefore focuses on:

- reproducible preprocessing
- reproducible modeling
- transparent parameter settings
- reproducible evaluation workflows

The emphasis is on documenting transparent and reproducible workflows rather than redistributing platform-restricted raw data.

# Recommended Entry Point

For most reproduction experiments, the recommended script is:

`run_bertopic_repro_improved.py`

The earlier scripts are preserved to document the incremental development process and intermediate reproduction attempts.

---