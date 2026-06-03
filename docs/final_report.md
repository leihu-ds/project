# Final Reproducibility Report

## 1. Introduction

This project is a reproducibility study of a published topic modelling research project on the Digital Circular Electrochemical Economy (DCEE). The original study applied several topic modelling methods, including BERTopic, LDA, and CorEx, to public attention text data collected from The Guardian, Reddit, and Twitter/X.

The main goal of this project was not to improve model performance. Instead, the project focused on evaluating whether the original research workflow could be reproduced using the published GitHub repository and available datasets. The project also aimed to identify practical reproducibility problems and document the steps needed to make the workflow more transparent.

## 2. Original Study and Repository

The original study used text data from The Guardian, Reddit, and Twitter/X to analyse public attention toward circular economy-related topics. The published repository included code for topic modelling and hyperparameter optimisation.

However, during reproduction, we found that the available repository data did not fully contain the cleaned full-text corpus required for direct topic modelling reproduction. Therefore, our reproduction focused on three questions:

1. Can the original repository be set up and executed in a new environment?
2. Are the available datasets sufficient for direct reproduction?
3. Can a transparent local pipeline be built to reproduce the topic modelling workflow as closely as possible?

## 3. Reproduction Workflow

The project followed six main stages:

1. Environment setup and dependency installation;
2. Dataset inspection and data structure checking;
3. Data recovery and preprocessing;
4. Initial reproduction attempts using the original scripts;
5. Improved BERTopic reproduction on cleaned local datasets;
6. Documentation of issues, results, and limitations.

The workflow was managed using GitHub branches. Each member worked on a separate part of the project, and documentation files were used to record reproduction logs, issues, outputs, and final results.

## 4. Environment Setup

The initial environment reproduction used Python 3.8 in a Conda environment named `dcee`. The basic setup commands were:

```bash
git clone https://github.com/leihu-ds/project.git
cd project

conda create --name dcee python=3.8 -y
conda activate dcee

pip install numpy==1.23.5
pip install spacy==3.5.0
pip install -r requirements.txt

python -m spacy download en_core_web_sm
```

The initial reproduction command was:

```bash
cd scripts/bertopic
python bert_grid_guardian.py
```

The initial environment setup was possible, but dependency conflicts and missing data issues appeared. In particular, some packages required careful version control, and the original scripts could not be fully evaluated without usable full-text data. This confirmed that stable dependency documentation and clear data preparation instructions are important for reproducibility.

## 5. Dataset and Preprocessing Reproduction

The dataset inspection showed that the visible repository files mainly contained metadata rather than full text. For example, The Guardian data contained fields such as date, section, and URL. Reddit data included source, type, URL, created time, and post ID. Twitter/X data mainly included IDs, user IDs, and URLs.

This created a major reproducibility problem because topic modelling requires actual text input. The model scripts expected full article text, Reddit post text, tweet text, titles, or cleaned text fields, but these were not directly available in the repository data.

### 5.1 Metadata Records vs Final Modelling Datasets

The larger dataset numbers refer to metadata records available in the repository, not directly usable modelling documents.

| Dataset / File           | Initial Records in Repository | Main Available Fields                   | Usable for Direct Topic Modelling? |
| ------------------------ | ----------------------------: | --------------------------------------- | ---------------------------------- |
| The Guardian metadata    |                        17,484 | date, section, url                      | No                                 |
| Reddit metadata          |                           680 | source, type, url, created_utc, post_id | No                                 |
| Twitter/X metadata       |                         5,298 | id, user_id, url                        | No                                 |
| Twitter/X external links |                        41,575 | urls, user_id                           | No                                 |
| Twitter/X related IDs    |                        12,458 | user_id                                 | No                                 |

After preprocessing and text recovery, the model-ready datasets before final filtering were smaller:

| Dataset      | Model-Ready Records Before Final Filtering | Explanation                           |
| ------------ | -----------------------------------------: | ------------------------------------- |
| The Guardian |                                      1,456 | Recovered full-text Guardian articles |
| Reddit       |                                      1,369 | Model-ready Reddit posts before final cleaning/filtering |
| Twitter/X    |                                      1,500 | Recovered Twitter/X text records      |

These model-ready counts are not the same as the final documents used in the improved BERTopic run. The final improved run applied additional cleaning, duplicate removal, and dataset-specific quality filtering.

| Dataset      | Final Documents Used in Improved BERTopic |
| ------------ | ----------------------------------------: |
| The Guardian |                                       976 |
| Reddit       |                                     1,335 |
| Twitter/X    |                                       839 |

This distinction between metadata records, model-ready records, and final modelling documents is a central reproducibility issue. Although the repository contains a relatively large number of records, most of them are not directly usable for topic modelling because they do not include full text. After text recovery and preprocessing, only records with usable cleaned text could be included in the improved modelling pipeline.

### 5.2 Data Recovery and Cleaning

To address this problem, the team reconstructed usable text data:

* The Guardian article text was partially recovered from URL metadata;
* Reddit public posts were collected and converted into model-ready text format;
* Twitter/X text was recovered from available tweet URLs;
* A light cleaning workflow was added to create cleaned text fields for modelling.

The recovered and cleaned datasets allowed the team to test the modelling workflow, but they cannot be assumed to be identical to the original paper corpus.

## 6. Modelling Reproduction

The modelling reproduction focused mainly on BERTopic because it was central to the original study and because final outputs were successfully produced for all three datasets.

The final modelling stage used Member 3's improved BERTopic pipeline. The final outputs were generated on the `Member3-Model-Methodology-Analyst` branch and saved under `outputs/member3/`.

The final output files include:

* `outputs/member3/guardian_bertopic_improved_*`
* `outputs/member3/reddit_bertopic_improved_*`
* `outputs/member3/twitter_bertopic_improved_*`
* `outputs/member3/member3_modeling_notes.md`

On the Member 3 branch, the command used to generate the final improved BERTopic outputs was:

```bash
.venv/bin/python scripts/member3/run_bertopic_repro_improved.py --dataset all --mode improved
```

The script expects the following cleaned datasets to be available locally:

```text
datasets/theguardian/guardian_cleaned.jsonl
datasets/reddit/reddit_cleaned.jsonl
datasets/twitter/twitter_cleaned.jsonl
```

This improved BERTopic pipeline kept the original BERTopic model family but added additional preprocessing and filtering steps, including duplicate removal, platform-specific stopwords, Twitter quality filtering, and Guardian circular economy / section filtering. These steps were necessary because the locally recovered datasets were not identical to the original paper datasets.

## 7. Results Comparison

The reproduction was partially successful. The team generated BERTopic outputs for all three datasets, but the results should not be treated as exact replications because the local recovered datasets and preprocessing steps differ from the original paper.

| Dataset      | Documents | Topics |  C_NPMI | Topic Diversity | Status               |
| ------------ | --------: | -----: | ------: | --------------: | -------------------- |
| The Guardian |       976 |     20 |  0.2215 |          0.9300 | Partially reproduced |
| Reddit       |     1,335 |     14 |  0.0340 |          0.9357 | Partially reproduced |
| Twitter/X    |       839 |      8 | -0.2828 |          0.9250 | Limited reproduction |

Compared with the paper's SOO BERTopic C_NPMI results, The Guardian and Reddit showed usable local reproduction results, while Twitter/X remained difficult.

| Dataset      | Paper SOO C_NPMI | Our Improved C_NPMI | Interpretation                                                                                     |
| ------------ | ---------------: | ------------------: | -------------------------------------------------------------------------------------------------- |
| The Guardian |           0.1669 |              0.2215 | Strong local result, but not an exact replication due to data and preprocessing differences.       |
| Reddit       |          -0.0609 |              0.0340 | Improved local coherence and more granular community-level topics.                                 |
| Twitter/X    |           0.1354 |             -0.2828 | Did not reproduce the paper coherence score; short and noisy recovered text remained a limitation. |

Example topic areas from the final improved BERTopic outputs include:

| Dataset      | Example Topic Areas                                                           |
| ------------ | ----------------------------------------------------------------------------- |
| The Guardian | Net zero / UK politics; ULEZ / air pollution; sewage / river pollution        |
| Reddit       | Plastic waste / recycling; recycling behaviour; batteries / electric vehicles |
| Twitter/X    | Climate change; renewables / wind / solar; circular economy / packaging       |

The Guardian and Reddit results show the strongest local reproduction performance. Twitter/X remains the weakest dataset because the recovered text is short, sparse, and hashtag-heavy. Therefore, Twitter/X can only be interpreted as a limited reproduction.

## 8. Reproducibility Issues

The main reproducibility issues were:

| Issue                          | Description                                                                                                                  | Impact                                                                                         | Action Taken                                                                               |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| Missing full-text data         | The released repository data mainly contained metadata such as URLs, IDs, dates, and sections.                               | The original topic modelling scripts could not run directly.                                   | The team recovered usable text data and documented the limitation.                         |
| Metadata-only records          | The initial record counts were much larger than the final modelling datasets because most records did not contain full text. | Dataset size could be misleading if metadata records were confused with model-ready documents. | The team documented the difference between metadata records and final model-ready records. |
| Hard-coded file paths          | Some scripts expected local absolute paths from the original author's machine.                                               | Scripts failed on other machines.                                                              | Paths were documented and replaced or avoided in the local workflow.                       |
| Dependency conflicts           | Some package versions were difficult to install consistently.                                                                | Environment setup was unstable.                                                                | Python 3.8 and key package fixes were documented.                                          |
| Missing preprocessing details  | The original cleaning pipeline was not fully documented.                                                                     | Exact reproduction of the original corpus was not possible.                                    | A transparent local cleaning workflow was added.                                           |
| Non-identical recovered corpus | The recovered data may not match the original paper dataset.                                                                 | Results are comparable but not identical.                                                      | The project reports partial reproduction rather than full replication.                     |
| Twitter/X short-text noise     | Twitter/X posts were short, sparse, and hashtag-heavy.                                                                       | C_NPMI remained low even after filtering.                                                      | Additional filtering and qualitative interpretation were used.                             |

## 9. Improvements Made

The project improved reproducibility in several ways:

1. Created documentation files for reproduction logs, issue tracking, result comparison, and final reporting;
2. Inspected and documented the dataset structure and available fields;
3. Added scripts and notes for data recovery and preprocessing;
4. Built model-ready and cleaned local datasets;
5. Ran improved BERTopic pipelines for The Guardian, Reddit, and Twitter/X;
6. Generated output files for topic information, topic words, document-topic assignments, and metrics;
7. Clearly documented which parts were reproducible and which parts remained limited.

These improvements make the workflow easier for future users to understand, even though the original paper cannot be exactly reproduced from the released repository alone.

## 10. Team Contributions

Member 1 focused on environment reproduction and initial modelling setup. This included cloning the repository, creating the Python environment, installing dependencies, resolving compatibility issues, and testing the initial BERTopic scripts.

Member 2 focused on data reproduction and preprocessing. This included checking the dataset structure, identifying missing full-text fields, distinguishing initial metadata records from final model-ready datasets, recovering text data, converting data into model-ready format, and documenting data limitations.

Member 3 focused on modelling reproduction and improvement. This member implemented and improved the BERTopic modelling component for The Guardian, Reddit, and Twitter/X cleaned datasets. The work included aligning baseline settings with the paper's SOO and MOO parameters, developing an improved BERTopic pipeline with duplicate removal, platform-specific stopwords, Twitter quality filtering, and Guardian CE / section filtering, and generating final topic outputs, document-topic assignments, C_NPMI scores, and topic diversity metrics. Member 3 also documented how to reproduce the results, how they compare with the paper, and why Twitter/X remains difficult to match exactly due to differences in the recovered short-text corpus.

Member 4 focused on results and documentation. This included maintaining the reproduction log, issue tracking file, results comparison, final report structure, and summarising the overall reproducibility findings. The main contribution of Member 4 was to make the reproduction process transparent by documenting what worked, what failed, what was fixed, and what limitations remained.

## 11. Discussion

The project shows that code availability alone is not enough for full reproducibility. Even though the original repository was available, direct reproduction was limited by missing full-text data, unclear preprocessing steps, hard-coded paths, and dependency issues.

The strongest local reproduction results came from The Guardian and Reddit. Both datasets produced interpretable BERTopic topics under the improved local pipeline. Twitter/X remained more difficult because the recovered text was short and noisy, which weakened coherence scores.

The comparison with the original paper should therefore be interpreted carefully. We can compare model structure, parameter choices, number of topics, C_NPMI, topic diversity, and qualitative topic themes. However, we cannot claim exact reproduction because our recovered datasets do not fully match the original paper datasets.

## 12. Conclusion

This project successfully documented and tested the reproducibility of a topic modelling study on public attention data in the DCEE context. The team was able to reconstruct usable data, run local BERTopic pipelines, generate outputs, and compare results with the original paper where possible.

However, exact reproduction was not possible because the full original cleaned datasets and complete preprocessing workflow were not fully available. The final result should therefore be reported as a partial reproduction and reproducibility evaluation rather than an exact replication.

The project's main contribution is the transparent documentation of the reproduction process, including what worked, what failed, what was addressed, and what limitations remained.
