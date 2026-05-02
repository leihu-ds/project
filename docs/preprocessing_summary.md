# Preprocessing Summary

## What I checked

I checked the dataset files, data fields, record counts, data loading paths, Guardian full-text recovery, and Reddit text recovery.

## Scripts added

```text
scripts/preprocessing/check_data_structure.py
scripts/preprocessing/inspect_dataset_fields.py
scripts/preprocessing/fetch_guardian_3000.py
scripts/preprocessing/convert_guardian_for_models.py
scripts/preprocessing/fetch_reddit_public_json.py
scripts/preprocessing/convert_reddit_for_models.py
scripts/preprocessing/recover_twitter_text_from_urls.py
```

## Reports generated

```text
docs/data_structure_report.md
docs/dataset_fields_report.md
```

## Dataset summary

| Platform | File | Records | Fields |
|---|---|---:|---|
| Guardian | `datasets/theguardian/data_guardian.json` | 17,484 | `date`, `section`, `url` |
| Reddit | `datasets/reddit/data_reddit.json` | 680 | `source`, `type`, `url`, `created_utc`, `post_id` |
| Twitter | `datasets/twitter/data_twitter.json` | 5,298 | `id`, `user_id`, `url` |
| Twitter | `datasets/twitter/data_twitter_external_links.json` | 41,575 | `urls`, `user_id` |
| Twitter | `datasets/twitter/data_twitter_related_ids.json` | 12,458 | `user_id` |

## Data loading check

I checked the Python scripts and found that several model scripts use local absolute paths.

The scripts also expect files such as:

- `guardian_all_data`
- `subreddit_posts_updated.json`
- `twitter_junhao.csv`
- `dcee_guardian`
- `dcee_reddit.json`
- `cleaned_tweets.csv`

These are different from the visible metadata files in the repository.

## Main finding

The visible data files mostly contain metadata.

I did not find full text fields needed for topic modelling, such as article text, Reddit post body, tweet text, title, or cleaned text.

Several model scripts also use hard-coded absolute paths.

## Guardian full-text recovery

The original Guardian metadata file only contains fields such as `date`, `section`, and `url`.

To make the data usable for topic modelling, I used the Guardian API to recover article titles and body text from the URLs.

The recovery script collected 1,456 Guardian articles with full body text before the API rate limit stopped the run.

The recovered data was converted into a model-ready JSONL format with these fields:

```text
title
content.body
date
section
url
```

The recovered full-text data is stored locally under `datasets/processed/guardian/`.

The full-text data is not committed to GitHub. The repository only includes the recovery and conversion scripts.

## Reddit text recovery

The original Reddit metadata file only contains limited fields and does not provide enough full post text for topic modelling.

I collected public Reddit posts using sustainability and circular economy keywords.

The Reddit recovery script collected 1,400 public Reddit records.

After filtering short or empty text records, 1,369 records were converted into a model-ready JSONL format with these fields:

```text
title
selftext
text
subreddit
keyword
created_utc
url
permalink
```

The main text field for modelling is `text`, which combines `title` and `selftext`.

The recovered Reddit data is stored locally and is not committed to GitHub. The repository only includes the recovery and conversion scripts.
## Twitter text recovery

The original Twitter files mainly contain tweet ids, user ids, URLs, and related ids.

I recovered Twitter/X text from tweet URLs and converted the recovered records into a model-ready JSONL format.

The Twitter recovery produced 1,500 model-ready records with these fields:

```text
source
tweet_id
url
text
recovery_method
```

The main text field for modelling is `text`.

The recovered Twitter data is stored locally as `datasets/twitter/twitter_for_models.jsonl`.

The recovered Twitter data is not committed to GitHub.The generated `.jsonl` files are ignored. 

The repository only includes the recovery script and documentation.

## Recommendation

The project should document:

- the required data file for each script
- where to get the full text data
- which column contains the text for modelling
- how to run scripts with relative paths
