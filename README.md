# Hirebot

An AI-powered job application framework built on [Claude Code](https://claude.ai/claude-code). Paste any job posting from any board in any country, and get a tailored CV and cover letter — all from your terminal.

## What Makes This Different

Most job search tools are either glorified spreadsheets or black-box resume builders. This framework is different:

- **Your profile is the source of truth.** Claude reads your actual experience and writing style before generating anything. It never fabricates skills or experience.
- **Drafter-reviewer pipeline.** Every application goes through an AI review step that catches generic language, unsupported claims, and weak openings before you send anything.
- **Works anywhere.** Paste a job URL (or drop a PDF of the job description) from any board in any country — Seek, LinkedIn, Indeed, Glassdoor, or anything else .  `/apply` handles the rest.
- **Minimal setup.** Python + pip. Output is `.docx` — the format recruiters and ATS systems often expect.
- **Runs inside Claude Code.** Three slash commands handle the entire workflow. No web app, no SaaS subscription.

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/Kev0Bui/hirebot.git
cd hirebot

# 2. Install dependencies
pip3 install -r requirements.txt

# 3. Start Claude Code and run setup
claude
# Then inside the Claude session:
/setup
```

After setup, paste any job URL into `/apply` to generate a tailored application.

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Claude Code CLI                    │
│                                                      │
│  /setup          /apply             /scrape          │
│  Onboarding      CV + cover letter  Job search       │
│  interview       generation         via Adzuna AU    │
│                                     (optional)       │
├──────────┬───────────┬──────────────┬────────────────┤
│ profile/ │ config.yaml│ .agents/     │ outputs/       │
│          │           │ skills/      │ cv/            │
│ 01-candidate.md      │ adzuna-search│ cover_letters/ │
│ 02-behavioural.md    │ job-evaluator│                │
│ 03-writing-style.md  │              │                │
│ 04-interview-prep.md │              │                │
├──────────┴───────────┴──────────────┴────────────────┤
│                  job_tracker.csv                      │
└─────────────────────────────────────────────────────┘
```

## Slash Commands

### `/setup` — Onboarding

Runs a conversational interview to build your professional profile. Claude asks about your experience, skills, writing style, and behavioural examples, then saves everything to the `profile/` files. Run this once to get started, or again any time you want to update your profile. The more information you provide, the better.

### `/apply` — Generate Application

The core workflow. Accepts a job URL or pasted description from any job board, then:

1. Parses the job posting
2. Evaluates fit against your profile (scored rubric)
3. Drafts a tailored CV and cover letter (.docx)
4. Reviews both documents through a critical hiring manager lens
5. Applies feedback and saves final versions
6. Presents a verification checklist

### `/scrape` — Australian Job Search (optional)

Searches the Adzuna AU API for jobs matching your config. Displays results as a ranked list with fit scores. Pick a number to apply, or paste a URL to start an application.

> **This command is for the Australian market only.** It requires free API credentials from [developer.adzuna.com](https://developer.adzuna.com/). If you're not in Australia, skip `/scrape` and use `/apply` directly with job URLs or pasted descriptions from your local job boards.

To set up `/scrape`:
```bash
# Add Adzuna credentials to .env (free from developer.adzuna.com)
echo 'ADZUNA_APP_ID=your-app-id' >> .env
echo 'ADZUNA_APP_KEY=your-app-key' >> .env
```

## Prerequisites

- **Python 3.10+** — [python.org](https://www.python.org/downloads/)
- **Claude Code** — [Installation guide](https://docs.anthropic.com/en/docs/claude-code/overview)
- **Adzuna API key** (free, optional, AU only) — [developer.adzuna.com](https://developer.adzuna.com/) — only required for `/scrape`

## File Structure

| Path | Purpose |
|------|---------|
| `config.example.yaml` | Template config — copied to `config.yaml` by `/setup` |
| `config.yaml` | Your personal config (gitignored, created by `/setup`) |
| `profile/01-candidate.md` | Professional profile — experience, skills, education |
| `profile/02-behavioural.md` | STAR-format examples for interviews and cover letters |
| `profile/03-writing-style.md` | Tone, structure, and language preferences |
| `profile/04-interview-prep.md` | Interview questions, company research, salary notes |
| `.agents/skills/adzuna-search/` | Adzuna API integration script (AU only) |
| `.agents/skills/job-evaluator/` | Job fit evaluation rubric |
| `.claude/commands/setup.md` | `/setup` slash command definition |
| `.claude/commands/scrape.md` | `/scrape` slash command definition (AU only) |
| `.claude/commands/apply.md` | `/apply` slash command definition |
| `outputs/cv/` | Generated CVs (.docx) |
| `outputs/cover_letters/` | Generated cover letters (.docx) |
| `job_tracker.csv` | Application tracking spreadsheet |
| `CLAUDE.md` | Instructions for Claude Code |

## Contributing

Contributions are welcome! Here's how to get involved:

### Adding a New Job Board

Each job board lives under `.agents/skills/` as its own directory. To add one:

1. Create `.agents/skills/your-board-name/`
2. Add a search script (Python) that reads from `config.yaml` and outputs results in the same format as the Adzuna script
3. Add a `README.md` explaining how to get API credentials (if needed) and how the script works
4. Update the `/scrape` command to support the new source

### General Contributing Guidelines

1. Fork the repo and create a feature branch
2. Keep changes focused — one feature or fix per PR
3. Test your changes with a real Claude Code session if possible
4. Submit a pull request with a clear description of what you changed and why

## Roadmap

- [ ] **Seek scraper** — Browser-based scraping via Playwright for Seek.com.au listings
- [ ] **LinkedIn manual paste helper** — Structured workflow for jobs found on LinkedIn
- [ ] **Interview scheduler** — Track interview dates and prep in the tracker
- [ ] **Multiple candidate profiles** — Support switching between profiles for different role types
- [ ] **Application analytics** — Track response rates, time-to-response, and fit score accuracy

## Licence

[MIT](LICENCE)

## Acknowledgements

- Inspired by [ai-job-search](https://github.com/MadsLorentzen/ai-job-search) by Mads Lorentzen
- Built on [Claude Code](https://claude.ai/claude-code) by Anthropic
- Job data provided by [Adzuna](https://www.adzuna.com.au/)
