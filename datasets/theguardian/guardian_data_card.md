# The Guardian Data Card

## Dataset Overview
- **Source**: The Guardian API
- **Purpose**: Academic research on circular economy topics
- **Collection method**: API-based data collection
- **Total records**: 17,484 articles

## Data Fields
- `date`: Publication date (YYYY-MM-DD)
- `section`: The Guardian section category
- `url`: Original article URL

## Processing Notes
- Data complies with The Guardian's content sharing policies
- Only essential metadata is retained
- All files use UTF-8 encoding
- No personal or sensitive information included

### Supported Tasks

- **Text Classification:** Categorising articles into different sections
- **Temporal Analysis:** Studying trends and patterns over time
- **Content Analysis:** Analysing article distribution across different sections

### Dataset Structure

#### Data Fields

- `date`: Publication date in YYYY-MM-DD format
- `section`: The Guardian section category (e.g., Environment, Business, Technology)
- `url`: Original article URL

#### Data Splits

The dataset contains 17,484 articles, sorted by date in descending order.

### Source Data

#### Initial Data Collection and Normalisation

- **Source:** The Guardian API
- **Collection Method:** API-based data collection
- **Collection Time Period:** 1945 to 2023
