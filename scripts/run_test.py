# scripts/run_test.py
import argparse
import time
import uuid
import os

def main(workflow_id):
    """
    Simulates running a planemo test for a specific workflow ID.
    It expects to be run inside the directory prepared by the setup job.
    """
    print(f"--- Running test for workflow: {workflow_id} ---")
    print(f"Current directory: {os.getcwd()}")
    print(f"Files in this directory: {os.listdir('.')}")
    
    # Simulate a long-running test
    time.sleep(5) 
    
    # Simulate planemo generating an invocation ID
    invocation_id = str(uuid.uuid4())
    output_file = "invocation_id.txt"
    with open(output_file, "w") as f:
        f.write(invocation_id)
        
    print(f"Test for '{workflow_id}' complete. Invocation ID: {invocation_id}")
    print(f"ID written to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--workflow-id", required=True, help="The ID of the workflow to test.")
    args = parser.parse_args()
    main(args.workflow_id)
