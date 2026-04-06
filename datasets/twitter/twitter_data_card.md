# Twitter Data Card

## Dataset Overview
- **Source**: Twitter
- **Purpose**: Academic research on information sharing patterns
- **Collection method**: Collected and processed in accordance with Twitter's data policies
- **Total records**: 54,033
  - Tweets with external links: 41,575
  - Unique users without external links: 12,458

## Data Files
1. `data_twitter_external_links.json`
   - Contains tweets with external links
   - Structure: `{"urls": ["https://t.co/xxx"], "user_id": "username"}`
   - Records: 41,575

2. `skipped_tweets_processed.json`
   - Contains unique user IDs of tweets without external links
   - Structure: `{"user_id": "username"}`
   - Records: 12,458

3. `twitter_skipped_tweets.json`
   - Original file containing all skipped tweets (for reference)

## Processing Notes
- All user IDs are preserved in original format
- URLs are stored in shortened t.co format
- Data has been cleaned and deduplicated
- All files use UTF-8 encoding 