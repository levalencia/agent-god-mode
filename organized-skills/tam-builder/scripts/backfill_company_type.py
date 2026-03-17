#!/usr/bin/env python3
"""
Backfill company_type for existing companies in Supabase.

Reads all companies, classifies each using metadata.keywords + industry + tech_stack,
and patches the company_type column.

Usage:
    python3 skills/capabilities/tam-builder/scripts/backfill_company_type.py \
      --config skills/capabilities/tam-builder/configs/hb-gtm-agency.json \
      [--dry-run]

    --dry-run   Preview classifications without writing to Supabase.
"""

import os
import sys
import json
import argparse

# Import shared modules
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SUPABASE_TOOLS = os.path.join(SCRIPT_DIR, "..", "..", "..", "..", "tools", "supabase")
sys.path.insert(0, os.path.abspath(SUPABASE_TOOLS))
sys.path.insert(0, SCRIPT_DIR)

from supabase_client import SupabaseClient
from tam_builder import classify_company_type, load_config, load_env


def backfill(config, env, dry_run=False):
    sb = SupabaseClient(env["SUPABASE_URL"], env["SUPABASE_SERVICE_ROLE_KEY"])
    client_name = config["client_name"]

    if not sb.test_connection():
        print("ERROR: Cannot connect to Supabase.")
        return

    # Fetch all companies with fields needed for classification
    companies = sb.get_all_companies(
        client_name,
        select="id,company_name,domain,industry,tech_stack,metadata,company_type"
    )

    print(f"Total companies for {client_name}: {len(companies)}")

    # Stats
    counts = {"product": 0, "services": 0, "agency": 0, "unknown": 0}
    already_set = 0
    updated = 0
    changes = []

    for c in companies:
        # Build org_data dict for classifier
        meta = c.get("metadata") or {}
        org_data = {
            "keywords": meta.get("keywords") or [],
            "industry": c.get("industry") or "",
            "tech_stack": c.get("tech_stack") or [],
        }

        new_type = classify_company_type(org_data)
        counts[new_type] += 1

        old_type = c.get("company_type")
        if old_type == new_type:
            already_set += 1
            continue

        changes.append({
            "id": c["id"],
            "domain": c.get("domain", "?"),
            "name": c.get("company_name", "?"),
            "old": old_type,
            "new": new_type,
            "keywords": (meta.get("keywords") or [])[:5],
        })

    print(f"\nClassification breakdown:")
    print(f"  Product:  {counts['product']}")
    print(f"  Services: {counts['services']}")
    print(f"  Agency:   {counts['agency']}")
    print(f"  Unknown:  {counts['unknown']}")
    print(f"\n  Already correct: {already_set}")
    print(f"  Need update: {len(changes)}")

    # Show sample changes
    if changes:
        print(f"\nSample changes (up to 20):")
        for ch in changes[:20]:
            kw_str = ", ".join(ch["keywords"][:3]) if ch["keywords"] else "none"
            print(f"  {ch['name'][:35]:<35} {ch['domain'][:25]:<25} {str(ch['old']):<10} -> {ch['new']:<10} kw: {kw_str}")

        if len(changes) > 20:
            print(f"  ... and {len(changes) - 20} more")

    if dry_run:
        print(f"\n[DRY RUN] No changes written. Remove --dry-run to apply.")
        return

    if not changes:
        print(f"\nNo updates needed — all companies already classified.")
        return

    # Apply updates
    print(f"\nApplying {len(changes)} updates...")
    for i, ch in enumerate(changes):
        sb._request(
            "PATCH",
            "companies",
            params={"id": f"eq.{ch['id']}"},
            data={"company_type": ch["new"]},
            extra_headers={"Prefer": "return=minimal"},
        )
        updated += 1
        if (i + 1) % 50 == 0:
            print(f"  Updated {i + 1}/{len(changes)}...")

    print(f"\nDone. Updated {updated} companies.")


def main():
    parser = argparse.ArgumentParser(description="Backfill company_type for existing companies")
    parser.add_argument("--config", required=True, help="Path to TAM config JSON")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    args = parser.parse_args()

    config = load_config(args.config)
    env = load_env()

    backfill(config, env, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
