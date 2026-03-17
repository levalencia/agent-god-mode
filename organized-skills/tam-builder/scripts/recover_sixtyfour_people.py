#!/usr/bin/env python3
"""
Recover SixtyFour People Enrichment Results
--------------------------------------------
Reads exported SixtyFour lead enrichment results (JSON) and writes them
back to the Supabase people table.

This script exists because the original enrichment run succeeded on the
SixtyFour side but Supabase writes failed due to a missing sixtyfour_id
column. The enrichment data was lost but SixtyFour still has the results.

Matching strategy:
  - Match by first_name (lowercase) + company_name (lowercase)
  - Use title as tiebreaker for any duplicates
  - Fall back to company_domain matching if company_name doesn't match

Input format (JSON file with array of objects):
  [
    {
      "task_id": "optional-task-id",
      "structured_data": {
        "name": "Matt",
        "email": "matt@example.com",
        "phone": "+1-555-0100",
        "linkedin_url": "https://linkedin.com/in/mattcbrown",
        "title": "President & CEO",
        "seniority": "C-Suite",
        "department": "Executive",
        "location": "Palo Alto, CA",
        "skills": "...",
        "education": "...",
        "previous_companies": "...",
        "bio": "...",
        "company": "Waverley Software",
        "years_in_role": "31"
      },
      "confidence_score": 8,
      "references": {...},
      "notes": "..."
    },
    ...
  ]

Usage:
    python3 recover_sixtyfour_people.py --input exported_results.json [--dry-run] [--client hb-gtm-agency]
"""

import os
import sys
import json
import argparse

# Import shared supabase client
SUPABASE_TOOLS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..", "..", "..", "tools", "supabase"
)
sys.path.insert(0, os.path.abspath(SUPABASE_TOOLS))
from supabase_client import SupabaseClient


def load_env():
    """Walk up from script dir looking for .env."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    d = script_dir
    for _ in range(6):
        env_path = os.path.join(d, ".env")
        if os.path.exists(env_path):
            env = {}
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        env[k.strip()] = v.strip().strip('"').strip("'")
            return env
        d = os.path.dirname(d)
    return {}


def normalize(s):
    """Lowercase, strip whitespace."""
    return (s or "").lower().strip()


def extract_first_name(name_str):
    """Extract first name from a name string."""
    parts = (name_str or "").strip().split()
    return parts[0].lower() if parts else ""


def build_person_index(people):
    """Build lookup indexes from Supabase people records.

    Returns:
        name_company: dict[(first_name, company_name)] -> list[person]
        name_domain: dict[(first_name, company_domain)] -> list[person]
    """
    name_company = {}
    name_domain = {}

    for p in people:
        first = normalize(p.get("name") or p.get("first_name") or "")
        company = normalize(p.get("company_name") or "")
        domain = normalize(p.get("company_domain") or "")

        key_nc = (first, company)
        name_company.setdefault(key_nc, []).append(p)

        if domain:
            key_nd = (first, domain)
            name_domain.setdefault(key_nd, []).append(p)

    return name_company, name_domain


def match_result_to_person(result, name_company, name_domain):
    """Match a SixtyFour result to a Supabase person.

    Returns:
        (person_dict, match_method) or (None, reason)
    """
    sd = result.get("structured_data", {})
    sf_name = extract_first_name(sd.get("name", ""))
    sf_company = normalize(sd.get("company", ""))
    sf_title = normalize(sd.get("title", ""))

    if not sf_name:
        return None, "no_name"

    # Try name + company match
    candidates = name_company.get((sf_name, sf_company), [])

    if len(candidates) == 1:
        return candidates[0], "name+company"

    if len(candidates) > 1:
        # Disambiguate by title
        for c in candidates:
            if normalize(c.get("title", ""))[:30] == sf_title[:30]:
                return c, "name+company+title"
        # Return first if can't disambiguate
        return candidates[0], "name+company(first)"

    # Fallback: try fuzzy company matching (SixtyFour might use a different company name)
    # e.g., "Waverley Software" vs "Waverley"
    for (first, company), persons in name_company.items():
        if first == sf_name and (company in sf_company or sf_company in company):
            if len(persons) == 1:
                return persons[0], "name+company(fuzzy)"

    return None, "no_match"


def merge_enrichment(person, result):
    """Build the Supabase update payload from SixtyFour result.

    Only updates fields that have actual data from SixtyFour.
    Never overwrites existing non-null values.
    """
    sd = result.get("structured_data", {})
    task_id = result.get("task_id")
    confidence = result.get("confidence_score", 0)

    update = {}

    # Core contact fields — only set if SixtyFour returned them
    if sd.get("email"):
        update["email"] = sd["email"]
    if sd.get("phone"):
        update["phone"] = sd["phone"]

    # LinkedIn URL — replace synthetic apollo:// with real URL
    if sd.get("linkedin_url") and sd["linkedin_url"].startswith("http"):
        old_linkedin = person.get("linkedin_url", "")
        if old_linkedin.startswith("apollo://"):
            update["linkedin_url"] = sd["linkedin_url"]

    # Name — SixtyFour might have full name
    sf_name = (sd.get("name") or "").strip()
    if sf_name and " " in sf_name:
        parts = sf_name.split(None, 1)
        if not person.get("last_name"):
            update["first_name"] = parts[0]
            update["last_name"] = parts[1]
            update["name"] = sf_name

    # Title — keep existing if present
    if sd.get("title") and not person.get("title"):
        update["title"] = sd["title"]

    # Seniority
    if sd.get("seniority"):
        update["seniority_level"] = sd["seniority"]

    # Headline / bio
    if sd.get("bio") and not person.get("headline"):
        update["headline"] = sd["bio"]

    # Location
    if sd.get("location") and not person.get("location"):
        update["location"] = sd["location"]

    # Skills — store as text array
    if sd.get("skills"):
        skills_raw = sd["skills"]
        if isinstance(skills_raw, str):
            skills_list = [s.strip() for s in skills_raw.split(",") if s.strip()]
        elif isinstance(skills_raw, list):
            skills_list = skills_raw
        else:
            skills_list = []
        if skills_list and not person.get("skills"):
            update["skills"] = skills_list

    # SixtyFour tracking
    if task_id:
        update["sixtyfour_id"] = task_id

    # Enrichment status
    update["enrichment_status"] = "complete"
    update["updated_by"] = "sixtyfour-recovery"

    # Store full SixtyFour result in raw_data
    existing_raw = person.get("raw_data") or {}
    update["raw_data"] = {
        **existing_raw,
        "_sixtyfour_data": {
            "structured_data": sd,
            "confidence_score": confidence,
            "references": result.get("references"),
            "notes": result.get("notes"),
        },
    }

    return update


def main():
    parser = argparse.ArgumentParser(description="Recover SixtyFour people enrichment")
    parser.add_argument("--input", required=True, help="Path to exported JSON file")
    parser.add_argument("--client", default="hb-gtm-agency", help="Client name")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    parser.add_argument("--min-confidence", type=float, default=5.0,
                        help="Skip results below this confidence score")
    args = parser.parse_args()

    # Load input
    with open(args.input) as f:
        results = json.load(f)

    if isinstance(results, dict):
        # Maybe it's wrapped in a key
        for key in ("results", "data", "items", "records"):
            if key in results and isinstance(results[key], list):
                results = results[key]
                break

    if not isinstance(results, list):
        print(f"ERROR: Expected a JSON array, got {type(results).__name__}")
        sys.exit(1)

    print(f"Loaded {len(results)} SixtyFour results from {args.input}")

    # Load env + connect
    env = load_env()
    sb = SupabaseClient(env["SUPABASE_URL"], env["SUPABASE_SERVICE_ROLE_KEY"])

    if not sb.test_connection():
        print("ERROR: Cannot connect to Supabase")
        sys.exit(1)

    # Fetch all people for this client
    print(f"Fetching people for client '{args.client}'...")
    people = sb._paginate("people", params={
        "select": "*",
        "client_name": f"eq.{args.client}",
    })
    print(f"  Found {len(people)} people in database")

    # Build indexes
    name_company, name_domain = build_person_index(people)

    # Process results
    matched = 0
    unmatched = 0
    skipped_low_conf = 0
    updated = 0
    errors = 0
    unmatched_results = []

    for i, result in enumerate(results):
        sd = result.get("structured_data", {})
        name = sd.get("name", "?")
        company = sd.get("company", "?")
        confidence = result.get("confidence_score", 0)

        if isinstance(confidence, str):
            try:
                confidence = float(confidence)
            except (ValueError, TypeError):
                confidence = 0

        if confidence < args.min_confidence:
            skipped_low_conf += 1
            continue

        person, method = match_result_to_person(result, name_company, name_domain)

        if person is None:
            unmatched += 1
            unmatched_results.append({
                "name": name,
                "company": company,
                "reason": method,
            })
            continue

        matched += 1
        update_payload = merge_enrichment(person, result)

        email = sd.get("email") or "no email"
        linkedin = sd.get("linkedin_url", "")[:50] if sd.get("linkedin_url") else "no linkedin"

        if args.dry_run:
            print(f"  [{i+1}] {name} @ {company} → MATCH ({method}) | {email} | {linkedin}")
        else:
            try:
                old_linkedin = person.get("linkedin_url", "")
                new_linkedin = update_payload.get("linkedin_url")

                if new_linkedin and old_linkedin and old_linkedin.startswith("apollo://"):
                    # LinkedIn URL changing — must patch by ID to avoid unique constraint
                    sb.patch_person_by_id(person["id"], update_payload)
                else:
                    # No LinkedIn change — safe to upsert
                    payload = {**person, **update_payload}
                    # Remove server-managed fields
                    for key in ("created_at", "updated_at"):
                        payload.pop(key, None)
                    sb.upsert_people([payload])

                updated += 1
                if (updated % 50) == 0:
                    print(f"  Updated {updated} people...")
            except Exception as e:
                errors += 1
                print(f"  ERROR updating {name} @ {company}: {e}")

    # Summary
    print(f"\n{'='*60}")
    print(f"Recovery Summary")
    print(f"{'='*60}")
    print(f"  Total results:      {len(results)}")
    print(f"  Matched:            {matched}")
    print(f"  Unmatched:          {unmatched}")
    print(f"  Skipped (low conf): {skipped_low_conf}")
    if not args.dry_run:
        print(f"  Updated:            {updated}")
        print(f"  Errors:             {errors}")
    else:
        print(f"  [DRY RUN — no writes made]")

    if unmatched_results:
        print(f"\nUnmatched results:")
        for r in unmatched_results[:20]:
            print(f"  - {r['name']} @ {r['company']} ({r['reason']})")
        if len(unmatched_results) > 20:
            print(f"  ... and {len(unmatched_results) - 20} more")


if __name__ == "__main__":
    main()
