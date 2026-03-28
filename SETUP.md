# Detailed Setup Guide

This guide walks you through every step of setting up AI Job Search AU, including installing prerequisites. If you're comfortable with Python and the command line, the [Quick Start in the README](README.md) might be all you need.

---

## Step 1: Install Python

You need Python 3.10 or newer.

### Check if Python is already installed

Open your terminal (on macOS: search for "Terminal" in Spotlight) and type:

```bash
python3 --version
```

If you see something like `Python 3.12.4`, you're good — skip to Step 2.

### Install Python on macOS

The easiest way is via Homebrew:

```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python
```

Alternatively, download the installer from [python.org/downloads](https://www.python.org/downloads/).

### Install Python on Windows

Download the installer from [python.org/downloads](https://www.python.org/downloads/). During installation, **tick the box that says "Add Python to PATH"** — this is important.

### Install Python on Linux

```bash
sudo apt update && sudo apt install python3 python3-pip
```

---

## Step 2: Install Claude Code

Claude Code is the AI assistant that powers this framework. You need the CLI installed.

### Install via npm

```bash
npm install -g @anthropic-ai/claude-code
```

If you don't have npm, install Node.js first from [nodejs.org](https://nodejs.org/).

### Verify installation

```bash
claude --version
```

You should see a version number. If not, check the [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code/overview) for troubleshooting.

---

## Step 3: Get an Adzuna API Key

Adzuna is a job search engine that aggregates listings from across Australia. Their API is free for personal use.

1. Go to [developer.adzuna.com](https://developer.adzuna.com/)
2. Click **"Sign Up"** in the top right
3. Fill in your details and create an account
4. Once logged in, you'll be taken to your dashboard
5. You'll see two values:
   - **Application ID** — a short string like `a1b2c3d4`
   - **Application Key** — a longer string like `abcdef1234567890abcdef1234567890`
6. Copy both of these — you'll need them in Step 5

The free tier gives you 250 API calls per day, which is plenty for job searching.

---

## Step 4: Clone the Repository

Open your terminal and run:

```bash
git clone https://github.com/YOUR_USERNAME/ai-job-search-au.git
cd ai-job-search-au
```

Then install the Python dependencies:

```bash
pip install -r requirements.txt
```

If `pip` doesn't work, try `pip3` instead:

```bash
pip3 install -r requirements.txt
```

---

## Step 5: Edit config.yaml

Open `config.yaml` in any text editor. This is the only file you need to edit before running `/setup`.

Here's what each field means:

### `candidate_name`
Your full name as it should appear on your CV and cover letters.

```yaml
candidate_name: "Jane Smith"
```

### `target_roles`
The job titles you're looking for. Be specific — these are used to search job boards.

```yaml
target_roles:
  - "Content Designer"
  - "UX Writer"
  - "Business Analyst"
```

### `locations`
Australian cities or regions you'd work in. Use "Remote" for fully remote roles.

```yaml
locations:
  - "Brisbane"
  - "Sydney"
  - "Remote"
```

### `salary_min_aud` and `salary_max_aud`
Your salary range in AUD (annual, before tax). This filters Adzuna results. Set to `0` to disable.

```yaml
salary_min_aud: 80000
salary_max_aud: 140000
```

### `work_types`
Types of employment you're open to. Options: `full_time`, `contract`, `part_time`.

```yaml
work_types:
  - "full_time"
  - "contract"
```

### `keywords_include`
Terms that should appear in relevant job listings. Jobs with more of these keywords get higher fit scores.

```yaml
keywords_include:
  - "content design"
  - "UX writing"
  - "agile"
```

### `keywords_exclude`
Terms that signal irrelevant roles. Jobs matching these are filtered out entirely.

```yaml
keywords_exclude:
  - "senior manager"
  - "unpaid"
  - "internship"
```

### `adzuna_app_id` and `adzuna_app_key`
Your Adzuna API credentials from Step 3.

```yaml
adzuna_app_id: "a1b2c3d4"
adzuna_app_key: "abcdef1234567890abcdef1234567890"
```

### `output_format`
Currently only `docx` is supported. Leave this as-is.

```yaml
output_format: "docx"
```

### `cv_template_style`
Controls the visual layout of generated CVs. Options:

- `professional` — Clean and conservative. Good for government, enterprise, and traditional industries.
- `creative` — More visual hierarchy with colour accents. Good for design and marketing roles.
- `minimal` — Maximum white space, minimal formatting. Good for tech and startup roles.

```yaml
cv_template_style: "professional"
```

---

## Step 6: Run /setup

Start a Claude Code session:

```bash
claude
```

Once inside the session, type:

```
/setup
```

Claude will conduct a conversational interview to build your professional profile. This takes about 10–15 minutes. You can also paste in an existing CV to speed things up.

---

## Step 7: Start Searching

After setup is complete, you have two main commands:

```
/scrape     # Search for jobs matching your profile
/apply      # Generate a tailored CV and cover letter for a specific job
```

Run `/scrape` to see what's available, pick a job, and `/apply` handles the rest.

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'yaml'"
You need to install the dependencies. Run:
```bash
pip install -r requirements.txt
```

### "Error: 'adzuna_app_id' in config.yaml is not set"
Open `config.yaml` and replace `YOUR_ADZUNA_APP_ID` and `YOUR_ADZUNA_APP_KEY` with your actual credentials from [developer.adzuna.com](https://developer.adzuna.com/).

### "Error: Adzuna API returned 401 Unauthorised"
Your API credentials are incorrect. Double-check them at [developer.adzuna.com](https://developer.adzuna.com/) — make sure you're using the Application ID and Application Key (not your login password).

### "python3: command not found"
Python isn't installed or isn't on your PATH. Follow Step 1 above.

### "claude: command not found"
Claude Code isn't installed. Follow Step 2 above.

### Generated .docx files won't open
Make sure `python-docx` is installed: `pip install python-docx`. If the file still won't open, check that the `outputs/` directories exist: `mkdir -p outputs/cv outputs/cover_letters`.

### The search returns no results
Try:
- Broadening your `target_roles` (use more general terms)
- Adding more `locations`
- Lowering `salary_min_aud` or setting it to `0`
- Removing restrictive `keywords_exclude` terms
