# Hirebot — Claude Code Instructions

## Purpose

This repository is an AI-powered job application framework that runs inside Claude Code. The core workflow is `/apply`: give it any job posting from any board in any country, and it drafts a tailored CV and cover letter based on your profile. A drafter-reviewer pipeline ensures quality before you send anything.

For users in Australia, `/scrape` adds optional automated job discovery via the Adzuna AU API. Everyone else just pastes URLs.

## Behaviour Rules

### Before every task
1. **Read `config.yaml`** to understand the candidate's target roles, preferences, and (if present) location and salary range. If `config.yaml` doesn't exist yet, tell the user to run `/setup` first (it creates `config.yaml` from `config.example.yaml`).
2. **Read the relevant `profile/` files** before drafting any document. Never generate content without first loading the candidate's actual experience and writing style.

### When drafting CVs and cover letters
- **Never fabricate skills, experience, or qualifications.** Every claim in a CV or cover letter must be verifiable against the profile files. If the candidate's profile doesn't mention a skill the job requires, note the gap — do not invent it.
- **Use the spelling and language conventions appropriate to the user's target market**, as captured in `profile/03-writing-style.md` or inferred from their location. For example, use Australian English for Australian roles, American English for US roles, etc.
- **Save all output as `.docx`** using `python-docx`. The `.docx` is for the candidate to edit and submit.
- **CVs** go to `outputs/cv/` with the naming format: `YYYY-MM-DD_CompanyName_RoleTitle.docx`
- **Cover letters** go to `outputs/cover_letters/` with the same naming format.
- **Cover letters should be forward-looking** — focus on what the candidate will bring to the role, not just what they've done.
- **Respect the candidate's writing style** as defined in `profile/03-writing-style.md`. Match their tone, structure preferences, and language choices.

### When evaluating job fit
- Use the scoring rubric in `.agents/skills/job-evaluator/SKILL.md`.
- Be honest about mismatches. A "Likely Mismatch" verdict is helpful — it saves the candidate time.

### General behaviour
- Be direct and practical. This is a job search tool, not a chatbot.
- When in doubt, ask the candidate rather than guessing.
- Track all discovered and applied jobs in `job_tracker.csv`.
- Never overwrite existing profile data without confirming with the user first.

## Slash Commands

### `/apply`
The core workflow. Accepts a job URL or pasted description from any job board in any country. Evaluates fit, drafts a tailored CV and cover letter, runs them through a reviewer, and saves final .docx files. See `.claude/commands/apply.md`.

### `/setup`
Run this first. Conducts a conversational onboarding interview, then populates the `profile/` files and updates `config.yaml`. See `.claude/commands/setup.md`.

### `/scrape` (Australia only)
Searches the Adzuna AU API for jobs matching the candidate's config. Requires free Adzuna API credentials. Displays results with fit scores and lets the user pick one to apply to. See `.claude/commands/scrape.md`.

## File Structure

```
config.example.yaml                  # Template config (tracked in git)
config.yaml                          # Personal config (gitignored, created by /setup)
profile/
  01-candidate.md                    # Professional profile
  02-behavioural.md                  # STAR-format examples
  03-writing-style.md                # Tone and language preferences
  04-interview-prep.md               # Interview preparation notes
.agents/skills/
  adzuna-search/search.py            # Adzuna API integration (AU only)
  job-evaluator/SKILL.md             # Fit evaluation rubric
.claude/commands/
  setup.md                           # /setup slash command
  scrape.md                          # /scrape slash command (AU only)
  apply.md                           # /apply slash command
outputs/
  cv/                                # Generated CVs (.docx)
  cover_letters/                     # Generated cover letters (.docx)
job_tracker.csv                      # Application tracking
```

## Session Context

<!-- Claude: update this section during each session to track what you're working on -->

**Current application:** None
**Last search:** None
**Active job posting:** None
**Draft status:** None
