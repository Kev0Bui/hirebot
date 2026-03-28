# Job Evaluator Skill

## Purpose

Evaluate how well a specific job posting matches the candidate's profile. This skill produces a structured fit assessment to help the candidate decide whether to apply.

## Instructions

When evaluating a job, you MUST:

1. Read `profile/01-candidate.md` to understand the candidate's experience, skills, and preferences
2. Read `config.yaml` to understand their target roles, salary range, and location preferences
3. Compare the job posting against the candidate's profile across all five dimensions below

## Scoring Rubric

Score each dimension from 1 (poor fit) to 5 (excellent fit).

### 1. Role Title Match

| Score | Description |
|-------|-------------|
| 5 | Exact or near-exact match with a target role title |
| 4 | Strong overlap — the role is clearly in the same discipline |
| 3 | Adjacent role — related but not a direct match (e.g. "Technical Writer" when targeting "Content Designer") |
| 2 | Tangentially related — some skill overlap but different discipline |
| 1 | Different field entirely |

### 2. Skills Overlap

| Score | Description |
|-------|-------------|
| 5 | Candidate has 90%+ of required skills and most nice-to-haves |
| 4 | Candidate has 70–90% of required skills |
| 3 | Candidate has 50–70% of required skills — some gaps but transferable experience |
| 2 | Candidate has 30–50% of required skills — significant gaps |
| 1 | Candidate has fewer than 30% of required skills |

### 3. Experience Level Fit

| Score | Description |
|-------|-------------|
| 5 | Experience level is an exact match (e.g. "5+ years" and candidate has 6) |
| 4 | Slightly over- or under-qualified but within a reasonable range |
| 3 | Noticeable gap — candidate could argue their case but it's a stretch |
| 2 | Significantly over- or under-qualified |
| 1 | Major mismatch — entry-level role for a senior candidate, or vice versa |

### 4. Location and Work Type Fit

| Score | Description |
|-------|-------------|
| 5 | Perfect match — location and work type (remote/hybrid/office) align exactly |
| 4 | Minor flexibility needed — e.g. hybrid when candidate prefers remote, but in the right city |
| 3 | Requires compromise — different city but same state, or work type doesn't fully match |
| 2 | Significant mismatch — relocation likely needed or work type is incompatible |
| 1 | Impossible — wrong country or completely incompatible arrangement |

### 5. Culture and Values Alignment

| Score | Description |
|-------|-------------|
| 5 | Strong alignment — company values, team structure, and work style match the candidate's preferences closely |
| 4 | Good alignment — most cultural signals are positive |
| 3 | Neutral — not enough information to assess, or mixed signals |
| 2 | Some red flags — company culture appears to conflict with candidate's preferences |
| 1 | Clear mismatch — values or work environment fundamentally incompatible |

## Output Format

Present the evaluation in this exact format:

```
## Job Fit Evaluation

**Role:** [Job title] at [Company]
**Location:** [Location] | **Work type:** [Full-time/Contract/etc.]
**Salary:** [If listed, otherwise "Not disclosed"]

| Dimension               | Score | Notes                              |
|-------------------------|-------|------------------------------------|
| Role title match        | X/5   | [Brief justification]              |
| Skills overlap          | X/5   | [Brief justification]              |
| Experience level fit    | X/5   | [Brief justification]              |
| Location & work type    | X/5   | [Brief justification]              |
| Culture & values        | X/5   | [Brief justification]              |
| **Overall**             | **X/25** |                                 |

### Fit Verdict: [Strong Match / Possible Match / Likely Mismatch]

[2-sentence recommendation on whether to apply and why.]
```

## Verdict Thresholds

- **Strong Match** (20–25): Apply with confidence. This role aligns well with the candidate's profile.
- **Possible Match** (13–19): Worth applying if the candidate is interested, but there are gaps to address in the application.
- **Likely Mismatch** (5–12): Probably not worth the effort unless the candidate has a compelling reason to apply.

## Important

- Be honest. A "Likely Mismatch" verdict saves the candidate time and energy.
- If information is missing from the job posting (e.g. no salary, vague requirements), note this in the evaluation and score conservatively.
- Never inflate scores to make the candidate feel better. Accuracy builds trust.
