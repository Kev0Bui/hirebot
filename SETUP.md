# Detailed Setup Guide

This guide walks you through every step of setting up Hirebot, including installing prerequisites. If you're comfortable with Python and the command line, the [Quick Start in the README](README.md) might be all you need.

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

## Step 3: Clone the Repository

Open your terminal and run:

```bash
git clone https://github.com/Kev0Bui/hirebot.git
cd hirebot
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

## Step 4: Understand config.example.yaml

The repo includes `config.example.yaml` as a template. You don't need to edit it — when you run `/setup` in Step 5, Claude will create your personal `config.yaml` (which is gitignored so your details stay private).

Here's what each field means, so you know what to expect:

### Core config

#### `candidate_name`
Your full name as it should appear on your CV and cover letters.

```yaml
candidate_name: "Jane Smith"
```

#### `target_roles`
The job titles you're looking for. Be specific — these are used to score job postings.

```yaml
target_roles:
  - "Content Designer"
  - "UX Writer"
  - "Business Analyst"
```

#### `keywords_include`
Terms that should appear in relevant job listings. Jobs with more of these keywords get higher fit scores.

```yaml
keywords_include:
  - "content design"
  - "UX writing"
  - "agile"
```

#### `keywords_exclude`
Terms that signal irrelevant roles. Jobs matching these are filtered out entirely.

```yaml
keywords_exclude:
  - "senior manager"
  - "unpaid"
  - "internship"
```

#### `work_types`
Types of employment you're open to. Options: `full_time`, `contract`, `part_time`.

```yaml
work_types:
  - "full_time"
  - "contract"
```

#### `cv_template_style`
Controls the visual layout of generated CVs. Options:

- `professional` — Clean and conservative. Good for government, enterprise, and traditional industries.
- `creative` — More visual hierarchy with colour accents. Good for design and marketing roles.
- `minimal` — Maximum white space, minimal formatting. Good for tech and startup roles.

```yaml
cv_template_style: "professional"
```

### Australian job search config (optional)

These fields are only used by the `/scrape` command, which searches Australian job boards via the Adzuna API. If you're not in Australia, you can ignore this section entirely.

#### `locations`
Australian cities or regions you'd work in. Use "Remote" for fully remote roles.

```yaml
locations:
  - "Brisbane"
  - "Sydney"
  - "Remote"
```

#### `salary_min_aud` and `salary_max_aud`
Your salary range in AUD (annual, before tax). This filters Adzuna results. Set to `0` to disable.

```yaml
salary_min_aud: 80000
salary_max_aud: 140000
```

#### Adzuna API credentials

To use `/scrape`, you need free Adzuna API credentials. Your credentials go in a `.env` file (not `config.yaml`) so they don't get committed to git:

1. Sign up at [developer.adzuna.com](https://developer.adzuna.com/) (free)
2. Copy your Application ID and Application Key from the dashboard
3. Create a `.env` file in the repo root:

```
ADZUNA_APP_ID=a1b2c3d4
ADZUNA_APP_KEY=abcdef1234567890abcdef1234567890
```

Replace the values with your actual credentials. The free tier gives you 250 API calls per day, which is plenty for job searching.

---

## Step 5: Run /setup

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

## Step 6: Start Applying

After setup is complete, you're ready to go:

```
/apply      # Paste a job URL or description to generate a tailored CV and cover letter
```

If you're in Australia and have Adzuna credentials set up:

```
/scrape     # Search Australian job boards for matching roles
```

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'yaml'"
You need to install the dependencies. Run:
```bash
pip install -r requirements.txt
```

### "Error: 'adzuna_app_id' is not set"
Create a `.env` file in the repo root with your Adzuna credentials. See the Adzuna API credentials section under Step 4.

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
