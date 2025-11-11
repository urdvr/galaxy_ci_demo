#!/usr/bin/env python3

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

def run_command(cmd):
    """Run a shell command and return output"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout, result.stderr, result.returncode

def parse_github_actions_url(url):
    """Parse a GitHub Actions URL and extract repo and run_id

    Expected format: https://github.com/owner/repo/actions/runs/RUN_ID
    """
    # Handle URL parsing
    parsed = urlparse(url)
    path = parsed.path

    # Pattern: /owner/repo/actions/runs/run_id
    match = re.match(r'^/([^/]+)/([^/]+)/actions/runs/(\d+)', path)

    if not match:
        print(f"\033[0;31mError: Invalid GitHub Actions URL format\033[0m")
        print(f"Expected format: https://github.com/owner/repo/actions/runs/RUN_ID")
        print(f"Received: {url}")
        sys.exit(1)

    owner, repo_name, run_id = match.groups()
    repo = f"{owner}/{repo_name}"

    return repo, run_id

def main(repo, run_id, output_dir):
    print(f"\033[0;34mFetching artifacts from GitHub Actions run {run_id}...\033[0m")

    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)

    # Fetch artifacts list
    print("\033[0;34mGetting list of artifacts...\033[0m")
    stdout, stderr, returncode = run_command(
        f'gh api "repos/{repo}/actions/runs/{run_id}/artifacts?per_page=100"'
    )

    if returncode != 0:
        print(f"\033[0;31mError fetching artifacts: {stderr}\033[0m")
        sys.exit(1)

    data = json.loads(stdout)
    artifacts = data.get('artifacts', [])
    total_count = len(artifacts)

    print(f"\033[0;32mFound {total_count} artifacts\033[0m")

    # Download each artifact
    success_count = 0
    skip_count = 0
    fail_count = 0

    for i, artifact in enumerate(artifacts, 1):
        artifact_id = artifact['id']
        artifact_name = artifact['name']
        expired = artifact['expired']

        if expired:
            print(f"\033[0;31m[{i}/{total_count}] Skipping expired artifact: {artifact_name}\033[0m")
            skip_count += 1
            continue

        print(f"\033[0;34m[{i}/{total_count}] Downloading: {artifact_name}\033[0m")

        # Download artifact
        output_file = Path(output_dir) / f"{artifact_name}.zip"
        stdout, stderr, returncode = run_command(
            f'gh api "repos/{repo}/actions/artifacts/{artifact_id}/zip" > "{output_file}"'
        )

        if returncode == 0 and output_file.exists() and output_file.stat().st_size > 0:
            print(f"\033[0;32m  ✓ Saved to: {output_file}\033[0m")

            # Extract artifact
            unzip_dir = Path(output_dir) / artifact_name
            unzip_dir.mkdir(exist_ok=True)

            stdout, stderr, returncode = run_command(
                f'unzip -q "{output_file}" -d "{unzip_dir}"'
            )

            if returncode == 0:
                print(f"\033[0;32m  ✓ Extracted to: {unzip_dir}\033[0m")
                success_count += 1
            else:
                print(f"\033[0;31m  ✗ Failed to extract\033[0m")
                fail_count += 1
        else:
            print(f"\033[0;31m  ✗ Failed to download\033[0m")
            fail_count += 1
            if output_file.exists():
                output_file.unlink()

    print(f"\n\033[0;32mDone! {success_count} artifacts downloaded successfully\033[0m")
    if skip_count > 0:
        print(f"\033[0;33m{skip_count} artifacts skipped (expired)\033[0m")
    if fail_count > 0:
        print(f"\033[0;31m{fail_count} artifacts failed to download\033[0m")
    print(f"\033[0;32mArtifacts saved to: {output_dir}\033[0m")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetch and extract artifacts from a GitHub Actions workflow run",
        epilog="Example: ./fetch_artifacts.py https://github.com/urdvr/galaxy_ci_demo/actions/runs/19144770808"
    )
    parser.add_argument(
        "url",
        help="GitHub Actions workflow run URL (e.g., https://github.com/owner/repo/actions/runs/RUN_ID)"
    )
    parser.add_argument(
        "--output-dir",
        help="Output directory for artifacts (default: ./artifacts_{RUN_ID})"
    )

    args = parser.parse_args()

    # Parse the URL to extract repo and run_id
    repo, run_id = parse_github_actions_url(args.url)

    # Set default output_dir if not provided
    output_dir = args.output_dir or f"./artifacts_{run_id}"

    print(f"\033[0;34mRepository: {repo}\033[0m")
    print(f"\033[0;34mRun ID: {run_id}\033[0m")
    print(f"\033[0;34mOutput directory: {output_dir}\033[0m\n")

    main(repo, run_id, output_dir)
