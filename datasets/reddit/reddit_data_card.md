# Reddit Data Card

## Dataset Overview
- **Source**: Reddit (r/circular_economy and related subreddits)
- **Purpose**: Academic research on the circular economy
- **Collection method**: Collected and processed in accordance with Reddit's Public Content Policy
- **Temporal coverage**: 19 July 2014 to 29 May 2023
- **Total records**: 680
  - Original Reddit posts (only post_id and date retained): 191
  - External links (only url and date retained): 489

## Field Descriptions
- `source`: Data source (all are 'reddit')
- `type`: Data type ('original_post' or 'shared_link')
- `post_id`: Unique identifier for original Reddit posts (present only for 'original_post')
- `url`: External link (present only for 'shared_link')
- `created_utc`: Date of publication (format: YYYY-MM-DD)

## Temporal Distribution
- **Yearly distribution**:
  - 2014: 89
  - 2015: 68
  - 2016: 17
  - 2017: 23
  - 2018: 28
  - 2019: 65
  - 2020: 102
  - 2021: 110
  - 2022: 132
  - 2023: 46
- **Earliest date**: 19 July 2014
- **Latest date**: 29 May 2023

## Processing and Compliance Notes
- Only content permitted for public sharing by Reddit is retained (no user information, no post text, no comments, no usernames)
- All external links were publicly shared by Reddit users
- Data processing complies with Reddit's [Public Content Policy](https://www.redditinc.com/blog/publishing-our-public-content-policy-and-introducing-a-new-community-for-researchers)
- Suitable for non-commercial academic research and compliant with EPSRC project requirements
