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
## Entry 3

### Date:
2026-05-02

### Member:
Yifan Yang (474665)

### Branch:
member2-data-preprocessing

### Task:
Checked the released dataset structure and available fields for all datasets.

### Dataset:
All datasets

### Script / Notebook:
- `scripts/preprocessing/check_data_structure.py`
- `scripts/preprocessing/inspect_dataset_fields.py`

### Environment:
- macOS
- Conda environment `dcee`
- Python 3.8
- Git branch `member2-data-preprocessing`

### Parameters:
N/A

### Result:
The dataset files were inspected for file format, record counts, top-level structure, and available fields. The reports showed that the visible repository data mainly contains metadata fields rather than full text fields needed for topic modelling.

### Error / Issue:
The checked dataset files did not include full article text, Reddit post body, tweet text, title, or cleaned text fields needed for topic modelling.

### Output Files:
- `docs/data_structure_report.md`
- `docs/dataset_fields_report.md`
- `scripts/preprocessing/check_data_structure.py`
- `scripts/preprocessing/inspect_dataset_fields.py`

### Comparison with Paper:
The paper uses full-text data from The Guardian, Reddit, and Twitter. The released repository data does not provide enough full text for direct reproduction.

### Notes:
This step confirmed that the repository data alone is not enough to reproduce the full topic modelling pipeline.


## Entry 4

### Date:
2026-05-02

### Member:
Yifan Yang (474665)

### Branch:
member2-data-preprocessing

### Task:
Documented dataset issues and reproducibility problems.

### Dataset:
All datasets

### Script / Notebook:
- `docs/issues/member2_data_issues.md`
- `docs/preprocessing_summary.md`
- `datasets/README.md`

### Environment:
- macOS
- Conda environment `dcee`
- Git branch `member2-data-preprocessing`

### Parameters:
N/A

### Result:
Documented the main data issues found during inspection. The notes explain that several model scripts use hard-coded absolute paths and expect data files that are different from the visible repository files.

### Error / Issue:
Several scripts point to local absolute paths from the original author's machine. Some expected files, such as `guardian_all_data`, `subreddit_posts_updated.json`, `twitter_junhao.csv`, `dcee_guardian`, `dcee_reddit.json`, and `cleaned_tweets.csv`, are not directly available in the visible repository data.

### Output Files:
- `docs/issues/member2_data_issues.md`
- `docs/preprocessing_summary.md`
- `datasets/README.md`

### Comparison with Paper:
The paper describes full-text datasets from The Guardian, Reddit, and Twitter, but the released repository data mainly contains metadata. This is a major reproducibility gap.

### Notes:
This documentation supports the final reproduction report by recording the data mismatch and path issues.


## Entry 5

### Date:
2026-05-02

### Member:
Yifan Yang (474665)

### Branch:
member2-data-preprocessing

### Task:
Recovered Guardian article text from URL metadata.

### Dataset:
The Guardian

### Script / Notebook:
- `scripts/preprocessing/fetch_guardian_3000.py`

### Environment:
- macOS
- Conda environment `dcee`
- Python 3.8
- Guardian API
- Git branch `member2-data-preprocessing`

### Parameters:
- `TARGET_N=3000`
- `SLEEP_SECONDS=1.2`
- `show-fields=headline,bodyText`

### Result:
The Guardian recovery script successfully used Guardian URLs to recover article titles and body text. The run recovered 1,456 Guardian articles with full body text before the API rate limit stopped the run.

### Error / Issue:
The Guardian API rate limit stopped the run before reaching 3,000 records. The script saved progress after each request, so the run can be continued later.

### Output Files:
- `scripts/preprocessing/fetch_guardian_3000.py`
- `datasets/processed/guardian/guardian_3000_with_text.json`
- `datasets/processed/guardian/guardian_3000_progress.json`

### Comparison with Paper:
The paper used Guardian full-text article data. The recovered Guardian data partially reconstructs the needed full-text input, but it is not guaranteed to match the original paper dataset exactly.

### Notes:
The recovered Guardian data is stored locally and is not committed to GitHub.


## Entry 6

### Date:
2026-05-02

### Member:
Yifan Yang (474665)

### Branch:
member2-data-preprocessing

### Task:
Converted recovered Guardian data into model-ready format.

### Dataset:
The Guardian

### Script / Notebook:
- `scripts/preprocessing/convert_guardian_for_models.py`

### Environment:
- macOS
- Conda environment `dcee`
- Python 3.8
- Git branch `member2-data-preprocessing`

### Parameters:
- Input: `datasets/processed/guardian/guardian_3000_with_text.json`
- Output: `datasets/processed/guardian/guardian_model_ready.jsonl`

### Result:
Converted 1,456 recovered Guardian records into a model-ready JSONL format. The output includes fields expected by the original Guardian model scripts, including `title` and `content.body`.

### Error / Issue:
None.

### Output Files:
- `scripts/preprocessing/convert_guardian_for_models.py`
- `datasets/processed/guardian/guardian_model_ready.jsonl`

### Comparison with Paper:
The output format is closer to the Guardian input expected by the paper's model scripts, but model results have not been compared with the paper yet.

### Notes:
The JSONL output is local data and is not committed to GitHub.


## Entry 7

### Date:
2026-05-02

### Member:
Yifan Yang (474665)

### Branch:
member2-data-preprocessing

### Task:
Collected public Reddit posts related to sustainability and circular economy using public Reddit JSON access.

### Dataset:
Reddit

### Script / Notebook:
- `scripts/preprocessing/fetch_reddit_public_json.py`

### Environment:
- macOS
- Conda environment `dcee`
- Python 3.8
- Public Reddit JSON access
- Git branch `member2-data-preprocessing`

### Parameters:
- Keywords included `circular economy`, `recycling`, `reuse`, `zero waste`, `waste reduction`, `plastic waste`, and `sustainability`.
- Subreddits included `sustainability` and `ZeroWaste`.
- Target collection size was around 1,000 to 3,000 records.
- No Reddit API credentials were used.

### Result:
Collected 1,400 public Reddit records. The records include fields such as `post_id`, `title`, `selftext`, `subreddit`, `keyword`, `score`, `num_comments`, `created_utc`, `url`, and `permalink`.

### Error / Issue:
Some Reddit posts have empty `selftext` because many Reddit posts are link posts or title-only posts. This is expected for Reddit data. The collection method depends on public Reddit JSON access, so it may be affected by Reddit access restrictions or network limits.

### Output Files:
- `scripts/preprocessing/fetch_reddit_public_json.py`
- `datasets/reddit/data_reddit_public.jsonl`

### Comparison with Paper:
The paper used Reddit post text for topic modelling. This recovered Reddit dataset provides public Reddit text for reproduction testing, but it may not match the original paper dataset exactly.

### Notes:
The recovered Reddit data is stored locally and is not committed to GitHub. This step did not use Reddit API credentials.


## Entry 8

### Date:
2026-05-02

### Member:
Yifan Yang (474665)

### Branch:
member2-data-preprocessing

### Task:
Converted recovered Reddit data into model-ready format.

### Dataset:
Reddit

### Script / Notebook:
- `scripts/preprocessing/convert_reddit_for_models.py`

### Environment:
- macOS
- Conda environment `dcee`
- Python 3.8
- Git branch `member2-data-preprocessing`

### Parameters:
- Input: `datasets/reddit/data_reddit_public.jsonl`
- Output: `datasets/processed/reddit/reddit_model_ready.jsonl`
- Text field: `title + selftext`
- Minimum text length: 30 characters

### Result:
Converted 1,369 Reddit records into a model-ready JSONL format. The main modelling field is `text`, which combines `title` and `selftext`.

### Error / Issue:
31 records were filtered out because the combined text was too short or empty.

### Output Files:
- `scripts/preprocessing/convert_reddit_for_models.py`
- `datasets/processed/reddit/reddit_model_ready.jsonl`

### Comparison with Paper:
The Reddit data is now usable for topic modelling, but topic results have not been compared with the paper yet.

### Notes:
The JSONL output is local data and is not committed to GitHub.


## Entry 9

### Date:
2026-05-02

### Member:
Yifan Yang (474665)

### Branch:
member2-data-preprocessing

### Task:
Recovered Twitter/X text from tweet URLs using oEmbed.

### Dataset:
Twitter

### Script / Notebook:
- `scripts/preprocessing/recover_twitter_text_from_urls.py`

### Environment:
- macOS
- Conda environment `dcee`
- Python 3.8
- Twitter/X oEmbed access
- Git branch `member2-data-preprocessing`

### Parameters:
- Recovery method: oEmbed
- Input source: Twitter URL metadata from repository files
- Output target size: around 1,500 records
- No Twitter/X API credentials were used.

### Result:
Recovered 1,500 Twitter/X model-ready records. The output records include `source`, `tweet_id`, `url`, `text`, and `recovery_method`.

### Error / Issue:
Twitter/X full API access was not used. The recovered text is based on available tweet URLs and oEmbed recovery, not the original full Twitter dataset. This means the recovered Twitter/X data may not fully match the paper's original Twitter data.

### Output Files:
- `scripts/preprocessing/recover_twitter_text_from_urls.py`
- `datasets/twitter/twitter_for_models.jsonl`

### Comparison with Paper:
The paper used full tweet text. The recovered Twitter/X data provides usable text for reproduction testing, but it may not fully match the original paper dataset.

### Notes:
The recovered Twitter data is stored locally. The data file was removed from Git tracking so that only scripts and documentation remain in the PR. This step did not use Twitter/X API credentials.


## Entry 10

### Date:
2026-05-02

### Member:
Yifan Yang (474665)

### Branch:
member2-data-preprocessing

### Task:
Updated Git ignore rules to avoid committing recovered data files.

### Dataset:
All datasets

### Script / Notebook:
- `.gitignore`

### Environment:
- macOS
- Git branch `member2-data-preprocessing`

### Parameters:
N/A

### Result:
Updated `.gitignore` so that local recovered data files and model-ready JSONL files are not committed to GitHub. The recovered data remains local and can be shared separately with group members.

### Error / Issue:
A Twitter model-ready data file was previously committed, then removed from Git tracking with documentation updated.

### Output Files:
- `.gitignore`

### Comparison with Paper:
N/A

### Notes:
This keeps the repository focused on scripts, documentation, and reproducibility instructions, not large recovered data files.


## Entry 11

### Date:
2026-05-02

### Member:
Yifan Yang (474665)

### Branch:
member2-data-preprocessing

### Task:
Updated preprocessing documentation and pushed data recovery work to the PR.

### Dataset:
All datasets

### Script / Notebook:
- `docs/preprocessing_summary.md`
- `docs/issues/member2_data_issues.md`
- `datasets/README.md`

### Environment:
- macOS
- Conda environment `dcee`
- Git branch `member2-data-preprocessing`
- GitHub PR workflow

### Parameters:
N/A

### Result:
The PR was updated with data inspection scripts, recovery scripts, conversion scripts, documentation, and reproducibility notes. The latest Git status was clean after commits and push.

### Error / Issue:
None.

### Output Files:
- `docs/preprocessing_summary.md`
- `docs/issues/member2_data_issues.md`
- `datasets/README.md`

### Comparison with Paper:
The documentation explains the mismatch between the paper's full-text data requirements and the repository's metadata-only files. It also documents partial recovery for Guardian, Reddit, and Twitter/X.

### Notes:
Recovered local model-ready data files can be shared separately with group members in a zip file, but they are not included in the PR. The three data sources were recovered with different methods: Guardian API for The Guardian, public Reddit JSON access for Reddit, and oEmbed recovery from tweet URLs for Twitter/X.
---
## Entry 12

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
## Entry 13

### Date:
2026-05-10

### Member:
Lei Hu

### Branch:
member1-modeling

### Task:
Implemented and improved a simplified BERTopic reproduction pipeline for Guardian article topic modelling.

### Dataset:
Guardian processed dataset (`guardian_model_ready.jsonl`)

### Script / Notebook:
scripts/modeling/simple_bertopic_guardian_v2.py

### Environment:
macOS (Apple Silicon)
Python 3.8
Conda environment: dcee

### Parameters:
- BERTopic
- all-MiniLM-L6-v2 embedding model
- UMAP dimensionality reduction
- min_topic_size = 4
- n_neighbors = 5
- custom stopword filtering
- spaCy preprocessing with lemmatization

### Result:
An initial simplified BERTopic pipeline (v1) was first implemented to verify whether the recovered Guardian full-text dataset could successfully run through the modeling workflow.

The v1 model completed successfully but generated low-quality and overly broad topics with limited interpretability.

A second version (v2) was then developed with improved preprocessing, custom stopword filtering, reproducible UMAP settings, and better clustering parameters.

The updated v2 pipeline generated more than 40 interpretable topics related to climate policy, renewable energy, pollution, fossil fuels, sustainability, and environmental politics.

### Error / Issue:
Initial reproduction attempts generated only two overly broad topics.

The original repository also lacked a clear preprocessing workflow and relied on incomplete metadata rather than full-text content.

Several parameter settings caused unstable clustering behaviour and BERTopic vectorizer errors.

### Output Files:
results/guardian/guardian_topic_info_v2.csv
results/guardian/guardian_topics_v2.json

### Comparison with Paper:
The reproduced results do not exactly match the original paper due to missing original datasets and preprocessing differences.

However, the simplified reproduction successfully generated semantically meaningful environmental and climate-related topics.

### Notes:
### Notes:
The iterative transition from v1 to v2 became an important part of the reproduction process.

The original repository did not provide a fully reproducible preprocessing pipeline. Important preprocessing operations, including lemmatization, document splitting, filtering procedures, and final modeling datasets, were either incomplete or undocumented.

Although preprocessing improvements increased pipeline reproducibility and reduced lexical noise, the resulting topics remained weakly separated.

This suggests that topic quality is highly dependent on the original cleaned corpus used by the authors.

The project therefore focused not only on reproducing outputs, but also on documenting the practical challenges of reproducing the original research pipeline.
## Entry 14

### Date:
2026-05-02

### Member:
Yifan Yang (474665)

### Branch:
member2-data-preprocessing

### Task:
Added a light text cleaning step for all recovered model-ready datasets.

### Dataset:
All datasets

### Script / Notebook:
- `scripts/preprocessing/clean_model_ready_text.py`

### Environment:
- macOS
- Conda environment `dcee`
- Python 3.8
- Git branch `member2-data-preprocessing`

### Parameters:
- Input files:
  - `datasets/processed/guardian/guardian_model_ready.jsonl`
  - `datasets/processed/reddit/reddit_model_ready.jsonl`
  - `datasets/twitter/twitter_for_models.jsonl`
- Output directory: `datasets/processed/cleaned/`
- Minimum cleaned text length: 30 characters

### Result:
Added a unified light text cleaning workflow for The Guardian, Reddit, and Twitter/X. The script creates a `clean_text` field and a `clean_text_length` field for each record. The cleaned outputs contain 1,456 Guardian records, 1,368 Reddit records, and 1,500 Twitter/X records.

### Error / Issue:
One Reddit record was filtered out after cleaning because the cleaned text was shorter than 30 characters.

### Output Files:
- `scripts/preprocessing/clean_model_ready_text.py`
- `datasets/processed/cleaned/guardian_cleaned.jsonl`
- `datasets/processed/cleaned/reddit_cleaned.jsonl`
- `datasets/processed/cleaned/twitter_cleaned.jsonl`

### Comparison with Paper:
The paper uses cleaned text for topic modelling, but the exact original cleaning pipeline is not fully reproducible from the released repository. This step adds a transparent and reproducible light cleaning process for the recovered text data.

### Notes:
The cleaning is intentionally light. It removes URLs, `pic.twitter.com` links, HTML tags, HTML entities, and extra whitespace, but does not apply stemming, lemmatization, or stopword removal. The cleaned data files are stored locally and are not committed to GitHub.
