# Results Comparison

## Original Paper vs Reproduced Results

| Dataset | Model | Metric | Paper Reported | Reproduced | Match? | Notes |
|---|---|---|---:|---:|---|---|
| The Guardian | BERTopic | C_NPMI (SOO) | 0.1669 |  |  |  |
| Reddit | BERTopic | C_NPMI (SOO) | -0.0609 |  |  |  |
| Twitter | CorEx | C_NPMI (SOO) | 0.1538 |  |  |  |

## MOO Results from the Paper

| Dataset | Model | C_NPMI | Diversity | Perplexity | Reproduced C_NPMI | Reproduced Diversity | Reproduced Perplexity | Notes |
|---|---|---:|---:|---:|---:|---:|---:|---|
| The Guardian | BERTopic | 0.1381 | 0.9886 | 1.4469 |  |  |  |  |
| Reddit | BERTopic | -0.2627 | 0.8558 | 8.1827 |  |  |  |  |
| Twitter | BERTopic | -0.0111 | 0.9486 | 74.9202 |  |  |  |  |
