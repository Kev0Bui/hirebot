# /apply — Generate Tailored Application Documents

You are running the core application workflow for Hirebot. This is a multi-step drafter-reviewer pipeline that produces a tailored CV and cover letter for a specific job.

## Input

Accept ONE of the following:
- A job listing URL (from any job board — Seek, LinkedIn, Indeed, Glassdoor, or any other)
- A pasted job description

If the user provides a URL, fetch the page content. If fetching fails, ask the user to paste the job description instead.

## Step 1 — Parse the Job Posting

Extract these details from the job posting:
- **Role title**
- **Company name**
- **Key responsibilities** (bullet points)
- **Required skills and qualifications**
- **Nice-to-have skills**
- **Location** (city, state/country, remote/hybrid/office)
- **Work type** (full-time, contract, part-time)
- **Salary** (if listed)
- **Application deadline** (if listed)

Present the extracted details to the user for confirmation:

> I've extracted the following from the job posting:
>
> **Role:** [title] at [company]
> **Location:** [location] | **Work type:** [type]
> **Salary:** [salary or "Not disclosed"]
>
> **Key requirements:**
> - [requirement 1]
> - [requirement 2]
> - ...
>
> Does this look right?

## Step 2 — Evaluate Fit

Read the following files:
- `profile/01-candidate.md`
- `config.yaml`
- `.agents/skills/job-evaluator/SKILL.md`

Apply the scoring rubric from SKILL.md and present the evaluation:

> ## Job Fit Evaluation
>
> | Dimension               | Score | Notes                              |
> |-------------------------|-------|------------------------------------|
> | Role title match        | X/5   | [justification]                    |
> | Skills overlap          | X/5   | [justification]                    |
> | Experience level fit    | X/5   | [justification]                    |
> | Location & work type    | X/5   | [justification]                    |
> | Culture & values        | X/5   | [justification]                    |
> | **Overall**             | **X/25** |                                 |
>
> ### Verdict: [Strong Match / Possible Match / Likely Mismatch]
>
> [2-sentence recommendation]

**If "Likely Mismatch":** Ask the user if they want to continue anyway before proceeding.

## Step 3 — Draft Documents

Read these files before drafting:
- `profile/01-candidate.md` — for experience and skills
- `profile/02-behavioural.md` — for relevant examples to weave in
- `profile/03-writing-style.md` — for tone, structure, language rules, and spelling convention
- `config.yaml` — for template style

### CV

Generate a tailored CV as `.docx` using `python-docx`:
- **Emphasise** skills and experience most relevant to THIS specific role
- **Reorder** sections to put the most relevant experience first
- **Never add** skills, qualifications, or experience the candidate doesn't have
- **Use the template style** from config.yaml (professional/creative/minimal)
- **Professional style:** Clean headers, consistent formatting, clear section breaks, conservative fonts
- **Creative style:** More visual hierarchy, colour accents, skills presented graphically
- **Minimal style:** Maximum white space, minimal formatting, content-forward

The CV should include:
1. Name and contact details
2. Professional summary (tailored to this role)
3. Key skills (relevant to this role's requirements)
4. Work experience (with role-relevant achievements highlighted)
5. Education
6. Certifications (if relevant)

### Cover Letter

Generate a tailored cover letter as `.docx`:
- **Follow the structure** defined in `profile/03-writing-style.md`
- **Opening:** Specific to this company and role — never generic
- **Body:** Forward-looking framing — what the candidate WILL bring, not just what they've done. Connect specific experience to specific requirements in the job posting.
- **Closing:** Confident, specific call to action
- **Length:** 3–4 paragraphs, fitting on one page
- **Use the spelling and language conventions** captured in `profile/03-writing-style.md`, or inferred from the user's location and target market (e.g. Australian English for Australian roles, American English for US roles)
- **Respect all "never do" rules** from the writing style guide

### Save Files

Save documents to the outputs directory:
- CV: `outputs/cv/YYYY-MM-DD_CompanyName_RoleTitle.docx`
- Cover letter: `outputs/cover_letters/YYYY-MM-DD_CompanyName_RoleTitle.docx`

Use today's date. Remove spaces and special characters from company and role names (use PascalCase).

Tell the user the files have been saved.

## Step 4 — Review

Spawn a subagent (using the Agent tool) with this instruction:

> You are a critical hiring manager reviewing an application for the role of [role title] at [company name]. You have high standards and are looking for reasons to shortlist OR reject this candidate.
>
> Review the following CV and cover letter against the job posting and the candidate's profile.
>
> **Check the CV for:**
> - Any claims not supported by the candidate's profile (profile/01-candidate.md)
> - Irrelevant experience taking up too much space
> - Missing skills that the candidate DOES have but weren't highlighted
> - Formatting or structural issues
>
> **Check the cover letter for:**
> - Generic language that could apply to any company ("I am passionate about...")
> - Weak or clichéd opening
> - Claims not supported by the profile
> - Tone mismatches with the candidate's writing style (profile/03-writing-style.md)
> - Spelling inconsistencies (e.g. mixing American and British English)
>
> **Provide:**
> - 3–5 specific, actionable improvements (not vague suggestions)
> - For each improvement, explain WHY it matters from a hiring manager's perspective
> - An overall assessment: "Ready to send", "Needs minor tweaks", or "Needs significant revision"

Present the reviewer's feedback to the user:

> ## Application Review
>
> **Reviewer verdict:** [Ready to send / Needs minor tweaks / Needs significant revision]
>
> **Feedback:**
> 1. [Specific improvement + reasoning]
> 2. [Specific improvement + reasoning]
> 3. ...

## Step 5 — Revise

Apply the reviewer's feedback to both documents:
- Make the specific changes suggested
- Re-save the .docx files (overwrite the originals)
- Briefly note what was changed

> I've applied the reviewer's feedback:
> - [Change 1]
> - [Change 2]
> - ...
>
> Updated files saved.

## Step 6 — Present and Verify

Show the user a verification checklist:

> ## Application Checklist
>
> - [ ] All CV claims verified against profile
> - [ ] Cover letter opening is specific to [company name] and [role title]
> - [ ] Spelling convention consistent throughout
> - [ ] Output files saved to correct locations
> - [ ] Job added to tracker
>
> **Files:**
> - CV: `outputs/cv/YYYY-MM-DD_CompanyName_RoleTitle.docx`
> - Cover letter: `outputs/cover_letters/YYYY-MM-DD_CompanyName_RoleTitle.docx`

Update `job_tracker.csv` — add the job (if not already tracked) or update its status to "Applied".

Then ask:

> Would you like me to make any changes, or are these ready to send?

## Step 7 — Offer Google Drive Export

After the user confirms the documents are ready (or immediately after the checklist if they don't request changes), offer to upload to Google Drive:

> Would you like me to export these to Google Drive?
> - [CV filename]
> - [Cover letter filename]
>
> I can upload both and share a link to each.

If the user says yes, use the `gdrive` CLI to upload both files:

```bash
gdrive files upload --parent <folder_id_if_configured> outputs/cv/YYYY-MM-DD_CompanyName_RoleTitle.docx
gdrive files upload --parent <folder_id_if_configured> outputs/cover_letters/YYYY-MM-DD_CompanyName_RoleTitle.docx
```

- If `google_drive_folder_id` is set in `config.yaml`, upload into that folder. Otherwise upload to root.
- If `gdrive` is not installed or auth fails, tell the user and show the local file paths instead.
- After a successful upload, present the shareable links:

> **Uploaded to Google Drive:**
> - CV: [link]
> - Cover letter: [link]

## Rules

- **Never fabricate skills or experience.** If the job requires something the candidate doesn't have, note the gap honestly in the cover letter or omit it — never invent it.
- **Always read the profile files** before drafting. Do not rely on memory from previous sessions.
- **Use the spelling convention from `profile/03-writing-style.md`**, or infer from the user's location and the job's target market.
- **Test that python-docx is available** before generating files. If not installed, run `pip3 install python-docx` first.
- **Handle errors gracefully.** If URL fetching fails, ask for pasted content. If file writing fails, show the error and suggest a fix.
