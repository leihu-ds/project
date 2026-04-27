# Preprocessing Summary

## What I checked

I checked the dataset files, data fields, record counts, and data loading paths.

## Scripts added

```text
scripts/preprocessing/check_data_structure.py
scripts/preprocessing/inspect_dataset_fields.py
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

## Recommendation

The project should document:

- the required data file for each script
- where to get the full text data
- which column contains the text for modelling
- how to run scripts with relative paths
