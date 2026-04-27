# Member 2 Data Issues

## Issue 1: Hard-coded paths

Some scripts use absolute paths from the original author's computer.

Example:

```python
pd.read_json('/home/yy2046/Workspace/DCEE2023/datasets/theguardian/all_keywords_data/guardian_all_data', lines=True)
```

This path does not work on my computer after cloning the repository.

Affected folders:

- `scripts/bertopic/`
- `scripts/lda/`
- `scripts/corex/`

This is a reproducibility issue because users need to edit file paths manually.

## Issue 2: Metadata-only data files

I checked the dataset files in the repository. Several JSON files appear to contain only metadata fields rather than the full text/content needed for analysis.

| File | Records | Fields |
|---|---:|---|
| `datasets/theguardian/data_guardian.json` | 17,484 | `date`, `section`, `url` |
| `datasets/reddit/data_reddit.json` | 680 | `source`, `type`, `url`, `created_utc`, `post_id` |
| `datasets/twitter/data_twitter.json` | 5,298 | `id`, `user_id`, `url` |
| `datasets/twitter/data_twitter_external_links.json` | 41,575 | `urls`, `user_id` |
| `datasets/twitter/data_twitter_related_ids.json` | 12,458 | `user_id` |

This is a data completeness issue because these files mostly provide identifiers, URLs, dates, or other metadata, but not the actual article/post/tweet text. This may prevent users from reproducing the original analysis unless the missing content is downloaded or provided separately.

I did not find full text fields like article text, Reddit post body, tweet text, title, or cleaned text.

This matters because topic modelling needs text data.

## Issue 3: Expected data files are different

The model scripts expect files such as:

- `guardian_all_data`
- `subreddit_posts_updated.json`
- `twitter_junhao.csv`
- `dcee_guardian`
- `dcee_reddit.json`
- `cleaned_tweets.csv`

These are different from the visible metadata files in the repository.

This is a reproducibility issue because the scripts cannot be run directly using only the dataset files currently visible in the repository.

## Summary

The repository contains scripts for topic modelling, but some scripts depend on local file paths and data files that are not directly available in the repository.

To improve reproducibility, the project should:

- Replace absolute local paths with relative paths.
- Provide the expected input data files or explain how to obtain them.
- Clarify which files are metadata-only and which files contain full text.
- Add instructions for preparing the data before running the model scripts.
