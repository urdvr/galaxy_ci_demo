import json
import os
from pathlib import Path
import argparse
import sys

def find_terminal_dirs(root_dir):
    terminal_dirs = []
    for dirpath, _, filenames in os.walk(root_dir):
        has_ga = any(f.endswith('.ga') for f in filenames)
        has_yml = any(f.endswith('.yml') for f in filenames)
        if has_ga and has_yml:
            relative_path = Path(dirpath).relative_to(root_dir)
            terminal_dirs.append(str(relative_path))
    return terminal_dirs

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", required=True)
    args = parser.parse_args()

    if not os.path.isdir(args.input_dir):
        print(f"Error: Directory not found: {args.input_dir}", file=sys.stderr)
        # Still output an empty matrix to avoid breaking the pipeline.
        matrix = []
    else:
        matrix = find_terminal_dirs(args.input_dir)

    matrix_json = json.dumps(matrix)
    
    # For GHA, setting the output.
    if os.getenv("GITHUB_OUTPUT"):
        with open(os.getenv("GITHUB_OUTPUT"), "a") as f:
            print(f"matrix_json={matrix_json}", file=f)
    else:
        # Fallback for local execution
        print(f"::set-output name=matrix_json::{matrix_json}")


if __name__ == "__main__":
    main()
