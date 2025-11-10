#!/usr/bin/env python3

import argparse
import os
from pathlib import Path

def main(artifacts_dir, output_file):
    artifacts_path = Path(artifacts_dir)

    if not artifacts_path.exists():
        print(f"Error: Directory {artifacts_dir} does not exist")
        return

    # Get all subdirectories
    subdirs = sorted([d for d in artifacts_path.iterdir() if d.is_dir()])

    print(f"Found {len(subdirs)} artifact directories")
    print(f"Concatenating to {output_file}...")

    with open(output_file, 'w') as outfile:
        for subdir in subdirs:
            # Find all .txt files in the subdirectory
            txt_files = list(subdir.glob("*.txt"))

            for txt_file in txt_files:
                # Read and write the content
                with open(txt_file, 'r') as infile:
                    content = infile.read().strip()
                    if content:
                        outfile.write(f"{content}\n")

    print(f"✓ Done! All invocation IDs concatenated to {output_file}")

    # Show summary
    with open(output_file, 'r') as f:
        line_count = sum(1 for _ in f)
    print(f"  Total lines: {line_count}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Concatenate all .txt files from artifact subdirectories into a single file"
    )
    parser.add_argument(
        "--artifacts-dir",
        default="./artifacts_19144770808",
        help="Directory containing artifact subdirectories (default: ./artifacts_19144770808)"
    )
    parser.add_argument(
        "--output-file",
        default="./all_invocation_ids.txt",
        help="Output file path (default: ./all_invocation_ids.txt)"
    )

    args = parser.parse_args()

    main(args.artifacts_dir, args.output_file)
