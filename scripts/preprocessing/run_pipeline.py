"""
Reproducible Research Pipeline
Author: Team Member 1

This script orchestrates the full data preprocessing pipeline.

Goals:
- Ensure reproducibility
- Standardize data format for further modeling
- Document each step clearly

Pipeline Steps:
1. Inspect raw datasets
2. Convert Guardian data to model-ready format
3. (Optional) Process Reddit data
4. (Optional) Process Twitter data

Note:
- Some datasets (Reddit, Twitter) require external data recovery. These are not included in the repository due to size/API limits
"""

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def run_command(cmd):
    """
    Run a shell command and print it for reproducibility.
    """
    print(f"\n[RUNNING] {cmd}")
    os.system(cmd)


def check_processed_data():
    """
    Check whether processed data exists.
    """
    guardian_path = ROOT / "datasets/processed/guardian/guardian_model_ready.jsonl"

    if guardian_path.exists():
        print("Guardian processed data exists")
    else:
        print("Guardian processed data NOT found!")


def main():
    print("=" * 60)
    print("Reproducible Research Data Pipeline")
    print("=" * 60)

    # --------------------------------------------------
    # Step 1: Inspect raw datasets
    # --------------------------------------------------
    print("\n[Step 1] Inspect dataset structure")
    run_command("python scripts/preprocessing/check_data_structure.py")

    # --------------------------------------------------
    # Step 2: Convert Guardian data to model-ready format
    # --------------------------------------------------
    print("\n[Step 2] Convert Guardian dataset")

    input_path = ROOT / "datasets/processed/guardian/guardian_3000_with_text.json"

    if input_path.exists():
        run_command("python scripts/preprocessing/convert_guardian_for_models.py")
    else:
        print("Guardian text data not found!")
        print("Please place file here:")
        print("datasets/processed/guardian/guardian_3000_with_text.json")

    # --------------------------------------------------
    # Step 3: Reddit (optional)
    # --------------------------------------------------
    print("\n[Step 3] Reddit dataset")

    reddit_path = ROOT / "datasets/processed/reddit"

    if reddit_path.exists():
        print("Reddit processed data exists")
    else:
        print("Reddit data not available!")

    # --------------------------------------------------
    # Step 4: Twitter (optional)
    # --------------------------------------------------
    print("\n[Step 4] Twitter dataset")

    twitter_path = ROOT / "datasets/processed/twitter"

    if twitter_path.exists():
        print("Twitter processed data exists")
    else:
        print("Twitter data not available!")

    # --------------------------------------------------
    # Step 5: Final check
    # --------------------------------------------------
    print("\n[Step 5] Final check")
    check_processed_data()

    print("\nPipeline finished.You can now run topic modeling scripts.")


if __name__ == "__main__":
    main()