# /scrape — Search for Jobs

You are running the Adzuna job search for AI Job Search AU.

## Process

### Step 1 — Run the Search

Execute the Adzuna search script:

```bash
python .agents/skills/adzuna-search/search.py
```

If the script fails:
- **401 error:** Tell the user their Adzuna API credentials are invalid and point them to https://developer.adzuna.com
- **No results:** Suggest broadening their search — fewer keywords_exclude, wider salary range, or more locations
- **Other errors:** Show the error message and suggest checking their internet connection

### Step 2 — Display Results

Parse the output and present it as a clean numbered list:

> **Job Search Results**
>
> Found X jobs matching your profile. Here are the top results:
>
> 1. **Content Designer** at Services Australia — Brisbane, Full-time
>    Salary: $95,000–$110,000 | Fit: ★★★★★
>    🔗 [View on Adzuna](url)
>
> 2. **UX Writer** at Suncorp Group — Sydney, Full-time
>    Salary: $100,000–$120,000 | Fit: ★★★★☆
>    🔗 [View on Adzuna](url)
>
> ... (show up to 15 results)

### Step 3 — Ask the User What to Do

> **What would you like to do?**
>
> - Enter a **number** (e.g. `3`) to start an application for that job
> - Paste a **job URL** to apply to a specific listing (from Seek, LinkedIn, or any job board)
> - Paste a **job description** to apply to a role you found elsewhere
> - Type `more` to see additional results
> - Type `done` to finish

### Step 4 — Handle the Response

- **If the user picks a number:** Extract the job URL from the search results and immediately run the `/apply` workflow. Read `.claude/commands/apply.md` and follow its instructions, passing the job URL.
- **If the user pastes a URL:** Run the `/apply` workflow with that URL.
- **If the user pastes a job description:** Run the `/apply` workflow with that pasted description.
- **If the user types `more`:** Show the next batch of results from the search output.
- **If the user types `done`:** End with a summary of how many jobs were found and remind them they can run `/apply` directly any time.

## Rules

- Always read `config.yaml` before running the search to confirm credentials are set.
- Display results clearly — don't dump raw script output at the user.
- If there are no results at all, be helpful: suggest adjusting target roles, expanding locations, or lowering salary_min_aud.
- Use Australian English throughout.
