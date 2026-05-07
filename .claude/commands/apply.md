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

Before drafting, determine **pivot status** from the JD:

- Read `target_roles` from `config.yaml`.
- If the role title strongly matches one of `target_roles` (exact or near-exact discipline match), `is_pivot_role = false`.
- Otherwise — e.g. Business Analyst, Product Manager, Service Designer, Engagement Manager, AI Governance, or any role outside the candidate's primary discipline — `is_pivot_role = true`.

The pivot rules below only apply when `is_pivot_role = true`. For non-pivot roles, draft normally.

Generate a tailored CV as `.docx` using `python-docx`:

- **Emphasise** skills and experience most relevant to THIS specific role
- **Reorder** content to put the most relevant experience first
- **Never add** skills, qualifications, or experience the candidate doesn't have
- **Never paraphrase JD verbs as the candidate's own actions** unless the action is directly verifiable in `profile/01-candidate.md`. Borrowing JD phrasing (e.g. JD says "you'll own product initiatives end-to-end" → CV/letter says "owned product initiatives across the full lifecycle") is a common overclaim trap, especially in pivot applications. Use the candidate's actual language from their profile and let the reader connect the dots. If the profile doesn't say it, neither does the application.
- **Never include referees** on the CV — no names, phone numbers, or emails. Do not add "References available on request" either; it's expected and wastes space.
- **Use the template style** from config.yaml (professional/creative/minimal)
- **Professional style:** Clean headers, consistent formatting, clear section breaks, conservative fonts
- **Creative style:** More visual hierarchy, colour accents, skills presented graphically
- **Minimal style:** Maximum white space, minimal formatting, content-forward

#### CV sections

1. Name and contact details
2. Professional summary — see rules below
3. Key skills — see rules below
4. Work experience — see bullet rules below
5. Education
6. Certifications (if relevant)
7. Public Speaking / Community — **conditional**, see rules below

#### Professional summary — 3 sentences max, ≤ 80 words total

Three sentences (≤ 4 if a pivot bridge sentence is added), in this order:

1. **What you are** — role + years of experience + sector context.
2. **What makes you differentiated for *this specific role*** — drawn from the JD's most prominent requirements, matched to real profile evidence.
3. **One outcome-anchored credibility marker** — concrete numbers preferred (e.g. "$50k support savings", "93 → 13 minutes per release note").

**Hard word cap: 80 words total** (100 with bridge). Sentence count alone is not enough — long sentences stitched with semicolons create the same wall-of-text problem. If the summary is over the cap, cut.

No "brings X" / "known for Y" filler clauses. No adjective stacking. No generic openers ("Results-driven", "Passionate", "Highly motivated"). Don't pack a single sentence with semicolon-stitched lists of every surface the candidate has touched.

**If `is_pivot_role = true`:** add a single **bridge sentence** to the summary that names the adjacent practice honestly, using the candidate's actual experience drawn from `profile/01-candidate.md`. Example shape: *"Content Designer with deep BA-adjacent practice: BPMN 2.0 process modelling, requirements elicitation, and cross-functional workshop facilitation."* Pull the specific practices from the candidate's real profile — do not invent.

**Never** include lines that announce the pivot — "Open to applying this experience in a [target] context", "Looking to apply...", "Ready to bring...", or any equivalent. Bridge, don't disguise.

#### Key skills — keyword grid, not essay

- 6–10 skill items total. No more.
- Each item is the skill name or a 2–4 word phrase. No descriptions, no paragraph explanations, no sub-clauses.
- Lay out as a clean 2-column grid (use a `python-docx` borderless table or a 2-column section).
- Optimised to scan in 5 seconds and pass ATS keyword matching.

Example transform:

- ❌ "Cross-Functional Collaboration: Embedded across Engineering, Product, Data, Design, Legal, and Risk teams; governance operationalised across product and operational lifecycles."
- ✅ "Cross-functional collaboration"

#### Work experience bullets — single idea, two lines max

Every bullet must:

- **Start with an action verb** (Designed, Led, Shipped, Cut, Reduced, Launched, Built, Drove).
- **Be ~25–30 words max** — fits on two lines of a standard A4 CV.
- **Express one idea**, with a measurable outcome where one exists in the candidate's profile.
- **No nested clauses.** No em-dash sub-explanations. No multi-clause sentences cramming action + outcome + secondary outcome + context into one sentence.

Example transform:

- ❌ "Designed and shipped the Content Review Desk — a structured, automated workflow for release notes that cut production time from 93 minutes to 13 minutes per release note."
- ✅ "Designed the Content Review Desk, an automated release notes workflow that cut production time from 93 to 13 minutes."

**If `is_pivot_role = true`:**

- Keep each role's bullets as a **flat list** under the candidate's actual job title from their profile.
- **Do not** invent structural sub-headers like "AI Governance & Responsible AI" or "Service design practice" to retitle existing work.
- Reordering bullets so the most relevant come first is fine. Inventing headers that retitle the role is not.

#### Public Speaking / Community — conditional inclusion

**Include** this section only when applying for roles in:

- Content design
- UX writing
- Technical writing
- Communications
- Marketing
- Copywriting
- Learning / training / education

**Drop** this section for roles in:

- Business Analyst
- Product Manager
- Service Design (when treated as a pivot)
- Engagement Manager
- Governance / AI Governance / Risk
- Consulting
- Process improvement / operations

When in doubt, drop it. Space on a CV is finite.

### Cover Letter

Generate a tailored cover letter as `.docx`:
- **Follow the structure** defined in `profile/03-writing-style.md`
- **Opening:** Specific to this company and role — never generic
- **Body:** Forward-looking framing — what the candidate WILL bring, not just what they've done. Connect specific experience to specific requirements in the job posting.
- **Closing:** Confident, specific call to action
- **Length:** 3–5 paragraphs, fitting on one page
- **Per-paragraph cap: ≤ 70 words.** One idea per paragraph. If a paragraph is stitching together pricing comms, a workflow project, and mentorship in a 90-word run-on, split it into two. Highlight reels read as hedging — chosen arguments read as confident.
- **No JD-verb borrowing** in the cover letter either — see the CV rule above. The cover letter is where overclaim usually leaks (the JD says "you'll lead discovery" and the candidate writes "I led discovery" without profile evidence).
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
> - **Professional summary length** — must be ≤ 3 sentences (or ≤ 4 if a pivot bridge sentence is included) AND ≤ 80 words total (100 with bridge). Flag if either limit is breached, including semicolon-stitched mega-sentences that comply with sentence count but violate word count.
> - **Skills section format** — must be a 6–10 item keyword grid with 2–4 word phrases. Flag essay-style descriptions, paragraph explanations, or more than 10 items.
> - **Bullet density** — each bullet must be one idea, ~25–30 words max, no nested clauses, no em-dash sub-explanations. Flag multi-clause walls.
> - **JD-verb borrowing** — flag any CV or cover letter phrasing that paraphrases a JD verb without verifiable profile evidence (e.g. JD: "you'll own product initiatives end-to-end" → application: "owned product initiatives across the full lifecycle" with no profile support). Quote both the JD line and the application line.
> - **Pivot positioning** (if the role is outside the candidate's primary discipline) — flag invented sub-headers retitling existing work, and flag any pivot-announcing lines like "Open to applying...", "Looking to apply...", "Ready to bring...", "Pivoting into [target role]...".
> - **Public Speaking section** — verify it's only included for content / UX writing / technical writing / communications / marketing / copywriting / learning roles. Flag if present for BA, PM, governance, service design, engagement manager, or consulting roles.
> - **Referees** — flag any referee names, phone numbers, emails, or "References available on request" text on the CV body.
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

## Rules

- **Never fabricate skills or experience.** If the job requires something the candidate doesn't have, note the gap honestly in the cover letter or omit it — never invent it.
- **Always read the profile files** before drafting. Do not rely on memory from previous sessions.
- **Use the spelling convention from `profile/03-writing-style.md`**, or infer from the user's location and the job's target market.
- **Test that python-docx is available** before generating files. If not installed, run `pip3 install python-docx` first.
- **Handle errors gracefully.** If URL fetching fails, ask for pasted content. If file writing fails, show the error and suggest a fix.
