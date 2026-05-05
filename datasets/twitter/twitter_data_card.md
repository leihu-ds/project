# Twitter Data Card

## Dataset Overview
- **Source**: Twitter
- **Purpose**: Academic research on information sharing patterns
- **Collection method**: Collected and processed in accordance with Twitter's data policies
- **Total records**: 54,033
  - Tweets with external links: 41,575
  - Unique users without external links: 12,458

## Data Files

1. `data_twitter.json`
- Contains tweet metadata (tweet IDs, user IDs, URLs)

2. `data_twitter_external_links.json`
- Contains tweets with external links
- Structure: {"urls": ["https://t.co/xxx"], "user_id": "username"}
- Records: 41,575

3. `data_twitter_related_ids.json`
- Contains additional user IDs related to tweets
- Records: 12,458

## Processing Notes
- All user IDs are preserved in original format
- URLs are stored in shortened t.co format
- Data has been cleaned and deduplicated
- All files use UTF-8 encoding 
