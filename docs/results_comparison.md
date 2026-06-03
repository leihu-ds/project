# Results Comparison

## Summary

The reproduction was partially successful. The team was able to run a local BERTopic reproduction pipeline on recovered and cleaned datasets for The Guardian, Reddit, and Twitter/X. However, the results should not be treated as an exact replication of the original paper because the released repository data mainly contained metadata rather than the full cleaned text corpus used in the paper.

The final comparison therefore focuses on whether the workflow could be made executable and whether meaningful topic modelling outputs could be generated under a transparent local pipeline.

## Original Paper Baseline

The original paper reported BERTopic results under both single-objective optimisation (SOO) and multi-objective optimisation (MOO). For direct C_NPMI comparison, the SOO BERTopic results are the clearest baseline.

| Dataset      | Model    | Paper SOO C_NPMI |
| ------------ | -------- | ---------------: |
| The Guardian | BERTopic |           0.1669 |
| Reddit       | BERTopic |          -0.0609 |
| Twitter/X    | BERTopic |           0.1354 |

The paper also reported MOO BERTopic results:

| Dataset      | Model    | Paper MOO C_NPMI | Paper MOO Topic Diversity | Paper MOO Perplexity |
| ------------ | -------- | ---------------: | ------------------------: | -------------------: |
| The Guardian | BERTopic |           0.1381 |                    0.9886 |               1.4469 |
| Reddit       | BERTopic |          -0.2627 |                    0.8558 |               8.1827 |
| Twitter/X    | BERTopic |          -0.0111 |                    0.9486 |              74.9202 |

## Metadata Records vs Final Modelling Datasets

One important issue in the reproduction process is that the initial dataset records in the repository are not the same as the final model-ready datasets. The larger numbers refer to metadata records, not directly usable text documents.

| Dataset / File           | Initial Records in Repository | Main Available Fields                   | Usable for Direct Topic Modelling? |
| ------------------------ | ----------------------------: | --------------------------------------- | ---------------------------------- |
| The Guardian metadata    |                        17,484 | date, section, url                      | No                                 |
| Reddit metadata          |                           680 | source, type, url, created_utc, post_id | No                                 |
| Twitter/X metadata       |                         5,298 | id, user_id, url                        | No                                 |
| Twitter/X external links |                        41,575 | urls, user_id                           | No                                 |
| Twitter/X related IDs    |                        12,458 | user_id                                 | No                                 |

After preprocessing and text recovery, the model-ready datasets before final filtering were smaller:

| Dataset      | Model-Ready Records Before Final Filtering | Explanation                                              |
| ------------ | -----------------------------------------: | -------------------------------------------------------- |
| The Guardian |                                      1,456 | Recovered full-text Guardian articles                    |
| Reddit       |                                      1,369 | Model-ready Reddit posts before final cleaning/filtering |
| Twitter/X    |                                      1,500 | Recovered Twitter/X text records                         |

These model-ready counts are not the same as the final documents used in the improved BERTopic run. The final improved run applied additional cleaning, duplicate removal, and dataset-specific quality filtering.

| Dataset      | Final Documents Used in Improved BERTopic |
| ------------ | ----------------------------------------: |
| The Guardian |                                       976 |
| Reddit       |                                     1,335 |
| Twitter/X    |                                       839 |

This distinction is central to the reproducibility evaluation. The repository contains many records, but most of them are metadata records rather than full-text documents. After text recovery and preprocessing, only records with usable cleaned text could be included in the improved modelling pipeline.

## Our Final Improved BERTopic Results

The final local reproduction used the improved BERTopic pipeline developed by Member 3. This pipeline kept the BERTopic model family but added additional preprocessing and filtering steps to make the local workflow more robust for the recovered datasets.

The final outputs were generated on the `Member3-Model-Methodology-Analyst` branch and saved under `outputs/member3/`.

The final output files are:

* `outputs/member3/guardian_bertopic_improved_*`
* `outputs/member3/reddit_bertopic_improved_*`
* `outputs/member3/twitter_bertopic_improved_*`
* `outputs/member3/member3_modeling_notes.md`

The command used to generate the final improved BERTopic outputs was:

```bash
.venv/bin/python scripts/member3/run_bertopic_repro_improved.py --dataset all --mode improved
```

The script expects the following cleaned datasets locally:

```text
datasets/theguardian/guardian_cleaned.jsonl
datasets/reddit/reddit_cleaned.jsonl
datasets/twitter/twitter_cleaned.jsonl
```

Final improved BERTopic metrics:

| Dataset      | Documents | Topics | Our C_NPMI | Our Topic Diversity | Reproduction Status  |
| ------------ | --------: | -----: | ---------: | ------------------: | -------------------- |
| The Guardian |       976 |     20 |     0.2215 |              0.9300 | Partially reproduced |
| Reddit       |     1,335 |     14 |     0.0340 |              0.9357 | Partially reproduced |
| Twitter/X    |       839 |      8 |    -0.2828 |              0.9250 | Limited reproduction |

More precise stored C_NPMI values:

| Dataset      | Stored C_NPMI |
| ------------ | ------------: |
| The Guardian |  0.2215193722 |
| Reddit       |  0.0340445376 |
| Twitter/X    | -0.2828273109 |

## Paper vs Our Improved Results

| Dataset      | Paper SOO C_NPMI | Our Improved C_NPMI | Main Finding                                                                                                                                                                                                                    |
| ------------ | ---------------: | ------------------: | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| The Guardian |           0.1669 |              0.2215 | The local result achieved higher coherence and produced broader 20-topic coverage of policy, energy, pollution, and climate themes. However, it is not an exact replication because the corpus and preprocessing are different. |
| Reddit       |          -0.0609 |              0.0340 | The local result improved from negative to small positive coherence and produced more granular community-level topics.                                                                                                          |
| Twitter/X    |           0.1354 |             -0.2828 | The local result did not match the paper's coherence score. Twitter/X remained difficult because the recovered texts were short, sparse, and hashtag-heavy.                                                                     |

## Example Topics

### The Guardian

| Topic Area               | Example Topic Words                                     |
| ------------------------ | ------------------------------------------------------- |
| Net zero / UK politics   | sunak, rishi, rishi sunak, tory, petrol, petrol diesel  |
| ULEZ / air pollution     | ulez, air pollution, khan, clean air, vehicle, drivers  |
| Sewage / river pollution | sewage, rivers, england, thames, water companies, river |

### Reddit

| Topic Area                    | Example Topic Words                                          |
| ----------------------------- | ------------------------------------------------------------ |
| Plastic waste / recycling     | plastics, plastic waste, plastic recycling, recycled plastic |
| Recycling behaviour           | bin, recyclable, trash, recyclables, compost, recycling bin  |
| Batteries / electric vehicles | batteries, vehicles, lithium, battery, electric, lithium ion |

### Twitter/X

| Topic Area                   | Example Topic Words                                                 |
| ---------------------------- | ------------------------------------------------------------------- |
| Climate change               | climate change, climatecrisis, climatechange, earth, climate action |
| Renewables / wind / solar    | renewables, renewable, wind, renewableenergy, solarenergy           |
| Circular economy / packaging | circular, waste, circular economy, packaging, recycling             |

## Interpretation

The Guardian and Reddit results are the strongest parts of the reproduction. Both datasets produced usable and interpretable topic structures under the local improved BERTopic pipeline. The Guardian result shows cleaner policy, energy, pollution, and climate-related topics after filtering. Reddit produced more granular community-level topics related to plastics, bins, clothing, reuse, and batteries.

Twitter/X was the weakest part of the reproduction. Although the filtering process made the top words cleaner, the final C_NPMI score remained negative. This is likely because the recovered Twitter/X corpus does not fully match the original paper dataset and contains many short, hashtag-style posts. For this dataset, qualitative topic inspection and topic diversity are more informative than coherence alone.

Overall, the project should be reported as a partial reproduction. The team successfully made the workflow executable and generated meaningful BERTopic outputs, but exact reproduction of the original paper was limited by missing full-text data, non-identical recovered corpora, dependency issues, and incomplete preprocessing documentation.
