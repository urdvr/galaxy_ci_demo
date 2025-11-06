# scripts/run_test.py
import argparse
import time
import uuid
import os
from pathlib import Path

def main(ga_file):
    """
    Simulates running a planemo test for a specific workflow.
    """
    print(f"--- Running test for workflow: {ga_file} ---")
    print(f"Current directory: {os.getcwd()}")
    
    # Simulate a long-running test
    time.sleep(5) 
    
    # Simulate planemo generating an invocation ID
    invocation_id = str(uuid.uuid4())
    
    output_file_name = Path(ga_file).stem
    output_file = f"invocation_id_{output_file_name}.txt"
    
    with open(output_file, "w") as f:
        f.write(invocation_id)
        
    print(f"Test for '{ga_file}' complete. Invocation ID: {invocation_id}")
    print(f"ID written to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ga-file", required=True, help="The path to the .ga workflow file.")
    args = parser.parse_args()
    main(args.ga_file)