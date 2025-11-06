# scripts/aggregate_results.py
import os

def main():
    """
    Simulates the fan-in job. Finds all downloaded invocation IDs
    and combines them into a single file.
    """
    print("--- Aggregating all invocation IDs ---")
    ids_dir = "all-invocation-ids"
    combined_file = "combined_ids.txt"
    
    if not os.path.exists(ids_dir):
        print(f"Error: Directory '{ids_dir}' not found!")
        return

    all_ids = []
    for filename in os.listdir(ids_dir):
        if filename.endswith(".txt"):
            with open(os.path.join(ids_dir, filename), "r") as f:
                all_ids.append(f.read().strip())
    
    print(f"Found {len(all_ids)} invocation IDs.")
    
    with open(combined_file, "w") as f:
        for an_id in all_ids:
            f.write(f"{an_id}\n")
            
    print(f"All IDs have been combined into '{combined_file}'")
    print("\n--- Content of combined file ---")
    with open(combined_file, "r") as f:
        print(f.read())
    print("---------------------------------")
    print("Ready to re-run tasks to check for caching.")

if __name__ == "__main__":
    main()
