# scripts/prepare_data.py
import json
import os
import shutil
import sys

def main():
    """
    Simulates finding workflows, creating a data directory for each,
    and printing a JSON list of their IDs for the GitHub Actions matrix.
    """
    print("--- Preparing data directories ---")
    
    # In a real scenario, you would clone the IWC repo here.
    # For this demo, we'll just simulate finding some workflow files.
    simulated_workflows = [
        "iwc/workflows/proteomics/workflow-a.ga",
        "iwc/workflows/metabolomics/workflow-b.ga",
        "iwc/workflows/genomics/workflow-c.ga",
    ]
    
    workflow_ids = []
    staging_base_dir = "staging"
    if os.path.exists(staging_base_dir):
        shutil.rmtree(staging_base_dir)
    os.makedirs(staging_base_dir)

    for wf_path in simulated_workflows:
        # Create a clean ID from the path, e.g., "workflow-a"
        wf_id = os.path.splitext(os.path.basename(wf_path))[0]
        workflow_ids.append(wf_id)
        
        # Create a dedicated directory for this workflow
        job_dir = os.path.join(staging_base_dir, wf_id)
        os.makedirs(job_dir)
        
        # Copy the workflow and test data into the job directory
        with open(os.path.join(job_dir, "workflow.ga"), "w") as f:
            f.write(f"# This is the content of {wf_path}\n")
        
        print(f"Prepared data directory: {job_dir}")

    # The final, most important step: print the JSON for GitHub Actions
    # This string will be captured by the workflow's 'run' step.
    print(f"\nGenerated {len(workflow_ids)} jobs.")
    json_output = json.dumps(workflow_ids)
    
    # This special syntax sets the GitHub Actions step output
    # Note: Ensure you are using bash as the shell in the workflow for this to work
    if 'GITHUB_OUTPUT' in os.environ:
        with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
            print(f"matrix_json={json_output}", file=f)
    
    print(f"Matrix for next step: {json_output}")

if __name__ == "__main__":
    main()
