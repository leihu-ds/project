# Member 3 BERTopic Reproduction and Improvement Notes

## Paper Baseline

The paper uses BERTopic with UMAP dimensionality reduction and KMeans clustering.
For single-objective optimisation (SOO), the reported objective is topic coherence
using C_NPMI.

Paper SOO BERTopic parameters:

| Dataset | n_gram | n_clusters | n_components | n_neighbors | Paper C_NPMI |
| --- | ---: | ---: | ---: | ---: | ---: |
| The Guardian | 2 | 2 | 5 | 20 | 0.1669 |
| Reddit | 2 | 2 | 15 | 20 | -0.0609 |
| Twitter | 2 | 10 | 10 | 10 | 0.1354 |

Paper MOO BERTopic parameters:

| Dataset | n_gram | n_clusters | n_components | n_neighbors | Paper C_NPMI | Diversity | Perplexity |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| The Guardian | 1 | 20 | 11 | 19 | 0.1381 | 0.9886 | 1.4469 |
| Reddit | 1 | 14 | 13 | 15 | -0.2627 | 0.8558 | 8.1827 |
| Twitter | 1 | 8 | 7 | 15 | -0.0111 | 0.9486 | 74.9202 |

## Current Improvement Direction

The script `scripts/member3/run_bertopic_repro_improved.py` keeps the paper's
BERTopic structure but improves the local reproducibility pipeline:

- exact duplicate removal on the model text;
- platform-specific stopword removal;
- removal of URLs, handles, dates, numeric tokens, and low-information social
  media tokens;
- `min_df=2` and `max_df=0.85` in the improved vectorizer to reduce one-off
  terms and overly common terms;
- compact output files that avoid storing very long representative documents in
  `topic_info`;
- local metrics output for C_NPMI and topic diversity.
- Twitter quality filtering removes exact duplicates, known account-level spam
  tokens, likely multilingual short-token noise, and generic promotional tweets
  that lack a clear CE signal.
- Guardian quality filtering keeps documents with stronger CE terms and limits
  the analysis to news/policy/business/environment-oriented sections, reducing
  sports, culture, recipe, and lifestyle spillover.

This gives the project two defensible tracks:

1. `paper-soo` / `paper-moo`: reproduce the original paper settings as closely
   as possible on the collected data.
2. `improved`: keep the paper model family but make preprocessing and topic
   quality reporting more robust for this group's scraped datasets.

## Commands

Run the improved model for all three datasets:

```bash
.venv/bin/python scripts/member3/run_bertopic_repro_improved.py --dataset all --mode improved
```

Run the paper SOO baseline for Twitter:

```bash
.venv/bin/python scripts/member3/run_bertopic_repro_improved.py --dataset twitter --mode paper-soo
```

Run the paper MOO parameter set for Reddit:

```bash
.venv/bin/python scripts/member3/run_bertopic_repro_improved.py --dataset reddit --mode paper-moo
```

Run a quick sample check:

```bash
.venv/bin/python scripts/member3/run_bertopic_repro_improved.py --dataset twitter --mode improved --sample 200
```

Run the local SOO-style grid search:

```bash
.venv/bin/python scripts/member3/run_bertopic_repro_improved.py --dataset twitter --mode grid-search
```

## Latest Improved Results

After adding Twitter quality filtering and Guardian CE/section filtering:

| Dataset | Documents | Topics | C_NPMI | Topic diversity | Reading |
| --- | ---: | ---: | ---: | ---: | --- |
| The Guardian | 976 | 20 | 0.2215 | 0.9300 | Cleaner than the earlier Guardian run; sports/film/recipe noise is reduced while policy, energy, pollution, and climate topics remain. |
| Reddit | 1335 | 14 | 0.0340 | 0.9357 | More granular than the paper SOO two-topic result; useful for community-level themes such as plastics, bins, clothing, reuse, and batteries. |
| Twitter | 839 | 8 | -0.2828 | 0.9250 | Top words are much cleaner after filtering, but coherence remains weak because short texts and hashtag-style discourse are sparse and fragmented. |

Interpretation for the report: the final improved run is strongest for The
Guardian and Reddit. Twitter should be discussed as a platform where topic
diversity is high but coherence remains difficult, which supports the paper's
argument that short social media text benefits from multi-objective evaluation
and human interpretability checks rather than coherence alone.
