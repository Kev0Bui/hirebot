#!/usr/bin/env python3
"""
Adzuna AU Job Search
Queries the Adzuna API for Australian job listings based on config.yaml settings.
Scores results against the candidate's profile and outputs a ranked table.
"""

import argparse
import csv
import os
import sys
from datetime import date
from pathlib import Path

import requests
import yaml

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

ADZUNA_BASE_URL = "https://api.adzuna.com/v1/api/jobs/au/search/{page}"
REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
CONFIG_PATH = REPO_ROOT / "config.yaml"
TRACKER_PATH = REPO_ROOT / "job_tracker.csv"

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------


def load_config() -> dict:
    """Load and validate config.yaml."""
    if not CONFIG_PATH.exists():
        print(f"Error: config.yaml not found at {CONFIG_PATH}", file=sys.stderr)
        print("Run /setup first or copy config.yaml to the repo root.", file=sys.stderr)
        sys.exit(1)

    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)

    # Validate required fields
    required = ["adzuna_app_id", "adzuna_app_key"]
    for field in required:
        value = config.get(field, "")
        if not value or value.startswith("YOUR_"):
            print(
                f"Error: '{field}' in config.yaml is not set.",
                file=sys.stderr,
            )
            print(
                "Sign up at https://developer.adzuna.com and add your credentials.",
                file=sys.stderr,
            )
            sys.exit(1)

    return config


# ---------------------------------------------------------------------------
# API
# ---------------------------------------------------------------------------


def search_adzuna(
    app_id: str,
    app_key: str,
    query: str,
    location: str,
    salary_min: int = 0,
    salary_max: int = 0,
    work_type: str = "",
    max_results: int = 50,
) -> list[dict]:
    """Query the Adzuna AU API and return raw results."""
    params = {
        "app_id": app_id,
        "app_key": app_key,
        "what": query,
        "where": location,
        "results_per_page": min(max_results, 50),
        "content-type": "application/json",
        "sort_by": "relevance",
    }

    if salary_min > 0:
        params["salary_min"] = salary_min
    if salary_max > 0:
        params["salary_max"] = salary_max
    if work_type:
        # Adzuna uses full_time, part_time, contract
        params["full_time"] = "1" if work_type == "full_time" else "0"
        params["part_time"] = "1" if work_type == "part_time" else "0"
        params["contract"] = "1" if work_type == "contract" else "0"

    all_results = []
    pages_needed = (max_results + 49) // 50

    for page in range(1, pages_needed + 1):
        url = ADZUNA_BASE_URL.format(page=page)
        try:
            resp = requests.get(url, params=params, timeout=15)
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if resp.status_code == 401:
                print(
                    "Error: Adzuna API returned 401 Unauthorised. Check your app_id and app_key.",
                    file=sys.stderr,
                )
                sys.exit(1)
            elif resp.status_code == 429:
                print(
                    "Error: Adzuna API rate limit exceeded. Wait a few minutes and try again.",
                    file=sys.stderr,
                )
                sys.exit(1)
            else:
                print(f"Error: Adzuna API request failed: {e}", file=sys.stderr)
                sys.exit(1)
        except requests.exceptions.ConnectionError:
            print(
                "Error: Could not connect to the Adzuna API. Check your internet connection.",
                file=sys.stderr,
            )
            sys.exit(1)
        except requests.exceptions.Timeout:
            print("Error: Adzuna API request timed out. Try again.", file=sys.stderr)
            sys.exit(1)

        data = resp.json()
        results = data.get("results", [])
        all_results.extend(results)

        if len(results) < 50:
            break  # No more pages

    return all_results


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------


def score_job(
    job: dict,
    target_roles: list[str],
    keywords_include: list[str],
) -> int:
    """
    Score a job 1–5 based on:
    - Title match with target roles (0–2 points)
    - Keyword overlap with description (0–3 points)
    """
    score = 1  # Base score — it appeared in the search results
    title = job.get("title", "").lower()
    description = job.get("description", "").lower()
    combined = f"{title} {description}"

    # Title match (up to 2 points)
    for role in target_roles:
        role_lower = role.lower()
        if role_lower in title:
            score += 2
            break
        # Partial match — at least half the words match
        role_words = role_lower.split()
        matches = sum(1 for w in role_words if w in title)
        if matches >= len(role_words) / 2:
            score += 1
            break

    # Keyword overlap (up to 2 points)
    if keywords_include:
        matches = sum(1 for kw in keywords_include if kw.lower() in combined)
        ratio = matches / len(keywords_include)
        if ratio >= 0.5:
            score += 2
        elif ratio >= 0.2:
            score += 1

    return min(score, 5)


def should_exclude(job: dict, keywords_exclude: list[str]) -> bool:
    """Check if a job matches any exclusion keywords."""
    title = job.get("title", "").lower()
    description = job.get("description", "").lower()
    combined = f"{title} {description}"

    for kw in keywords_exclude:
        if kw.lower() in combined:
            return True
    return False


# ---------------------------------------------------------------------------
# Deduplication and tracking
# ---------------------------------------------------------------------------


def load_tracked_ids() -> set[str]:
    """Load job IDs already in the tracker."""
    ids = set()
    if TRACKER_PATH.exists():
        with open(TRACKER_PATH, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                ids.add(row.get("job_id", ""))
    return ids


def append_to_tracker(jobs: list[dict]) -> int:
    """Append new jobs to job_tracker.csv. Returns count of new entries."""
    tracked = load_tracked_ids()
    new_count = 0

    file_exists = TRACKER_PATH.exists() and TRACKER_PATH.stat().st_size > 0
    with open(TRACKER_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow([
                "date_added", "job_id", "company", "role_title", "location",
                "work_type", "salary", "fit_score", "source_url", "status", "notes",
            ])

        for job in jobs:
            job_id = str(job.get("id", ""))
            if job_id in tracked:
                continue

            salary = ""
            if job.get("salary_min") and job.get("salary_max"):
                salary = f"${int(job['salary_min']):,}–${int(job['salary_max']):,}"
            elif job.get("salary_min"):
                salary = f"${int(job['salary_min']):,}+"
            elif job.get("salary_max"):
                salary = f"Up to ${int(job['salary_max']):,}"

            location = job.get("location", {}).get("display_name", "Unknown")
            work_type = job.get("contract_time", "")

            writer.writerow([
                date.today().isoformat(),
                job_id,
                job.get("company", {}).get("display_name", "Unknown"),
                job.get("title", "Unknown"),
                location,
                work_type,
                salary,
                job.get("_score", 1),
                job.get("redirect_url", ""),
                "Discovered",
                "",
            ])
            tracked.add(job_id)
            new_count += 1

    return new_count


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------


def format_table(jobs: list[dict]) -> str:
    """Format jobs as a readable table for stdout."""
    if not jobs:
        return "No matching jobs found."

    lines = []
    header = f"{'#':<4} {'Score':<6} {'Title':<40} {'Company':<25} {'Location':<20} {'Salary':<25} {'URL'}"
    lines.append(header)
    lines.append("─" * len(header))

    for i, job in enumerate(jobs, 1):
        title = job.get("title", "Unknown")[:39]
        company = job.get("company", {}).get("display_name", "Unknown")[:24]
        location = job.get("location", {}).get("display_name", "Unknown")[:19]

        salary = ""
        if job.get("salary_min") and job.get("salary_max"):
            salary = f"${int(job['salary_min']):,}–${int(job['salary_max']):,}"
        elif job.get("salary_min"):
            salary = f"${int(job['salary_min']):,}+"
        elif job.get("salary_max"):
            salary = f"Up to ${int(job['salary_max']):,}"
        salary = salary[:24]

        score = job.get("_score", 1)
        url = job.get("redirect_url", "")

        lines.append(
            f"{i:<4} {'★' * score + '☆' * (5 - score):<6} {title:<40} {company:<25} {location:<20} {salary:<25} {url}"
        )

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(description="Search Adzuna AU for jobs.")
    parser.add_argument("--role", type=str, help="Override target role (single role)")
    parser.add_argument("--location", type=str, help="Override location (single location)")
    parser.add_argument("--max-results", type=int, default=20, help="Max results per query (default: 20)")
    args = parser.parse_args()

    config = load_config()

    app_id = config["adzuna_app_id"]
    app_key = config["adzuna_app_key"]
    target_roles = [args.role] if args.role else config.get("target_roles", [])
    locations = [args.location] if args.location else config.get("locations", [])
    salary_min = config.get("salary_min_aud", 0)
    salary_max = config.get("salary_max_aud", 0)
    work_types = config.get("work_types", ["full_time"])
    keywords_include = config.get("keywords_include", [])
    keywords_exclude = config.get("keywords_exclude", [])

    if not target_roles:
        print("Error: No target_roles defined in config.yaml.", file=sys.stderr)
        sys.exit(1)

    if not locations:
        print("Error: No locations defined in config.yaml.", file=sys.stderr)
        sys.exit(1)

    # Collect all results across role × location combinations
    all_jobs = {}
    total_queries = len(target_roles) * len(locations)
    query_num = 0

    for role in target_roles:
        for loc in locations:
            query_num += 1
            print(
                f"Searching [{query_num}/{total_queries}]: '{role}' in {loc}...",
                file=sys.stderr,
            )

            results = search_adzuna(
                app_id=app_id,
                app_key=app_key,
                query=role,
                location=loc,
                salary_min=salary_min,
                salary_max=salary_max,
                max_results=args.max_results,
            )

            for job in results:
                job_id = str(job.get("id", ""))
                if not job_id:
                    continue

                # Skip excluded jobs
                if should_exclude(job, keywords_exclude):
                    continue

                # Score and deduplicate (keep highest score)
                score = score_job(job, target_roles, keywords_include)
                job["_score"] = score

                if job_id not in all_jobs or all_jobs[job_id]["_score"] < score:
                    all_jobs[job_id] = job

    # Sort by score descending
    sorted_jobs = sorted(all_jobs.values(), key=lambda j: j.get("_score", 0), reverse=True)

    # Output table
    print()
    print(format_table(sorted_jobs))
    print()

    # Append to tracker
    new_count = append_to_tracker(sorted_jobs)
    print(f"Found {len(sorted_jobs)} jobs. {new_count} new entries added to job_tracker.csv.", file=sys.stderr)


if __name__ == "__main__":
    main()
