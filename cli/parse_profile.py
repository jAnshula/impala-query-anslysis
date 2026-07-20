# cli/parse_profile.py

import argparse
import sys
from services.execution_profile_builder import ExecutionProfileBuilder
from storage.query_repository import QueryRepository

def main():
    parser = argparse.ArgumentParser(description="Parse Impala query profile")
    parser.add_argument("file", help="Path to query profile file")
    parser.add_argument("--store", action="store_true", help="Store profile in repository")
    args = parser.parse_args()

    try:
        with open(args.file, "r", encoding="utf-8") as f:
            raw_profile = f.read()
    except Exception as e:
        print(f"Error reading file {args.file}: {e}", file=sys.stderr)
        sys.exit(1)

    builder = ExecutionProfileBuilder()
    profile = builder.build(raw_profile)

    if args.store:
        repo = QueryRepository()
        repo.save_profile(profile)
        print(f"Profile stored successfully.")
    else:
        print(f"Profile health score: {profile.health_score}")
        print(f"Findings: {len(profile.findings)} issues detected.")

if __name__ == "__main__":
    main()


