# Dataset Documentation

## Dataset files checked

| Platform | File | Format | Records | Fields |
|---|---|---|---:|---|
| Guardian | `datasets/theguardian/data_guardian.json` | JSON | 17,484 | `date`, `section`, `url` |
| Reddit | `datasets/reddit/data_reddit.json` | JSON | 680 | `source`, `type`, `url`, `created_utc`, `post_id` |
| Twitter | `datasets/twitter/data_twitter.json` | JSON | 5,298 | `id`, `user_id`, `url` |
| Twitter | `datasets/twitter/data_twitter_external_links.json` | JSON | 41,575 | `urls`, `user_id` |
| Twitter | `datasets/twitter/data_twitter_related_ids.json` | JSON | 12,458 | `user_id` |

## Data checking scripts

```text
scripts/preprocessing/check_data_structure.py
scripts/preprocessing/inspect_dataset_fields.py
```

## Reports

```text
docs/data_structure_report.md
docs/dataset_fields_report.md
```

## Main notes

The checked files mainly contain metadata.

I did not find full text fields needed for topic modelling, such as article text, Reddit post body, tweet text, title, or cleaned text.

The model scripts seem to expect other data files, such as:

- `guardian_all_data`
- `subreddit_posts_updated.json`
- `twitter_junhao.csv`

## Git note

Local raw and processed data folders are ignored by Git:

```text
datasets/raw/
datasets/processed/
```
