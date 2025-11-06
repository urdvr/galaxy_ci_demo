import argparse
import json
import subprocess
import os

def main(ga_file, yml_file):
    """
    Runs a planemo test for a specific workflow and extracts the invocation ID.
    """
    print(f"--- Running test for workflow: {ga_file} ---")
    print(f"Current directory: {os.getcwd()}")

    command = [
        "planemo", "run", ga_file, yml_file,
        "--no_wait",
        "--galaxy_url", "https://test.usegalaxy.org",
        "--galaxy_user_key", "0f055db60f177b5b8129334512dc892f",
        "--test_output_json", "out.json",
        "--simultaneous_uploads",
        "--check_uploads_ok"
    ]

    try:
        subprocess.run(command, check=True)
        with open("out.json", "r") as f:
            results = json.load(f)
        invocation_id = results["tests"][0]["data"]["invocation_details"]["details"]["invocation_id"]
        print(invocation_id)
    except (subprocess.CalledProcessError, FileNotFoundError, KeyError, IndexError) as e:
        print(f"Error running planemo or parsing output: {e}")
        exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ga_file", help="The path to the .ga workflow file.")
    parser.add_argument("yml_file", help="The path to the .yml test file.")
    args = parser.parse_args()
    main(args.ga_file, args.yml_file)
