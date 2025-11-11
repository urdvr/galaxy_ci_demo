import argparse
import json
import subprocess
import os
from uuid import uuid4

def check_existing_invocation(run_id, invocation_file):
    """
    Check if an invocation already exists for this workflow.
    Returns the invocation ID if found, None otherwise.
    """
    if not os.path.exists(invocation_file):
        return None

    with open(invocation_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('\t')
            if len(parts) == 2 and parts[0] == run_id:
                return parts[1]
    return None

def main(ga_file, yml_file, run_id):
    """
    Runs a planemo test for a specific workflow and extracts the invocation ID.
    Skips creating new invocations if one already exists for this workflow.
    """
    print(f"--- Running test for workflow: {ga_file} ---")
    print(f"Current directory: {os.getcwd()}")

    # Check if invocation already exists
    invocation_file = os.path.join(os.environ.get('GITHUB_WORKSPACE', ''), 'all_invocation_ids.txt')
    existing_invocation = check_existing_invocation(run_id, invocation_file)

    if existing_invocation:
        print(f"Found existing invocation for {run_id}: {existing_invocation}")
        print("Skipping planemo run and using existing invocation ID.")
        with open(f'invocation_id--{run_id}.txt', 'w+') as f:
            f.write(f'{run_id}\t{existing_invocation}')
        return

    # Retrieve the API key from an environment variable
    api_key = os.environ.get("GALAXY_USER_KEY")
    if not api_key:
        print("Error: GALAXY_USER_KEY environment variable not set.")
        exit(1)

    command = [
        "planemo", "run", ga_file, yml_file,
        "--no_wait",
        "--galaxy_url", "https://vgp.usegalaxy.org",
        "--galaxy_user_key", api_key,
        "--test_output_json", "out.json",
        "--simultaneous_uploads",
        "--check_uploads_ok"
    ]

    print("No existing invocation found. Creating new invocation...")
    try:
        subprocess.run(command, check=True)
        with open("out.json", "r") as f:
            results = json.load(f)
        invocation_id = results["tests"][0]["data"]["invocation_details"]["details"]["invocation_id"]
        print(f"Created new invocation: {invocation_id}")
        with open(f'invocation_id--{run_id}.txt', 'w+') as f:
            f.write(f'{run_id}\t{invocation_id}')
    except (subprocess.CalledProcessError, FileNotFoundError, KeyError, IndexError) as e:
        print(f"Error running planemo or parsing output: {e}")
        exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ga_file", help="The path to the .ga workflow file.")
    parser.add_argument("yml_file", help="The path to the .yml test file.")
    parser.add_argument("run_id", help="The run ID to use for the invocation ID.")
    args = parser.parse_args()
    main(args.ga_file, args.yml_file, args.run_id)
