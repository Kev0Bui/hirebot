# Adzuna AU Job Search

This skill queries the [Adzuna API](https://developer.adzuna.com/) for Australian job listings, scores them against your profile, and tracks results in `job_tracker.csv`.

## Getting API Credentials

1. Go to [developer.adzuna.com](https://developer.adzuna.com/)
2. Click **Sign Up** and create a free account
3. Once logged in, you'll see your **Application ID** and **Application Key** on the dashboard
4. Copy both values into `config.yaml`:

```yaml
adzuna_app_id: "your-app-id-here"
adzuna_app_key: "your-app-key-here"
```

The free tier allows 250 API calls per day, which is more than enough for job searching.

## What It Does

1. Reads your target roles, locations, salary range, and keywords from `config.yaml`
2. Queries Adzuna AU for every combination of role × location
3. Deduplicates results by job ID
4. Filters out jobs matching your `keywords_exclude` list
5. Scores each job 1–5 based on:
   - **Title match** (0–2 points): How closely the job title matches your target roles
   - **Keyword overlap** (0–2 points): How many of your `keywords_include` appear in the listing
   - **Base score** (1 point): Every result gets 1 point for appearing in search results
6. Outputs a ranked table to stdout
7. Appends new results to `job_tracker.csv` (skips duplicates)

## Running Manually

```bash
# Use config.yaml settings
python .agents/skills/adzuna-search/search.py

# Override role and location
python .agents/skills/adzuna-search/search.py --role "UX Writer" --location "Melbourne"

# Limit results
python .agents/skills/adzuna-search/search.py --max-results 10
```

## Output

The script prints a table like this:

```
#    Score  Title                                    Company                   Location             Salary                    URL
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
1    ★★★★★  Content Designer                         Services Australia        Brisbane             $95,000–$110,000          https://...
2    ★★★★☆  UX Writer                                Suncorp Group             Sydney               $100,000–$120,000         https://...
3    ★★★☆☆  Digital Content Specialist               Queensland Government     Brisbane             $85,000+                  https://...
```

New results are automatically appended to `job_tracker.csv` with status "Discovered".

## Used By

This script is called by the `/scrape` slash command. You don't normally need to run it directly — but you can if you want to test your API credentials or experiment with different search parameters.
