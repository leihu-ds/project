from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "datasets"

def inspect_json(path: Path):
    print(f"\nFILE: {path.relative_to(ROOT)}")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print("Format: JSON")
    print("Top-level type:", type(data).__name__)

    if isinstance(data, list):
        print("Records:", len(data))
        if data:
            first = data[0]
            print("First record type:", type(first).__name__)
            if isinstance(first, dict):
                print("Columns/keys:", list(first.keys()))
                print("Sample keys:", list(first.keys())[:10])

    elif isinstance(data, dict):
        print("Top-level keys:", list(data.keys()))
        for key, value in data.items():
            print(f"First key: {key}")
            print("Value type:", type(value).__name__)
            if isinstance(value, list):
                print("Records:", len(value))
                if value and isinstance(value[0], dict):
                    print("First record keys:", list(value[0].keys()))
            break

def inspect_csv(path: Path):
    print(f"\nFILE: {path.relative_to(ROOT)}")
    df = pd.read_csv(path)
    print("Format: CSV")
    print("Rows:", len(df))
    print("Columns:", list(df.columns))
    print("Missing values per column:")
    print(df.isna().sum())
    print("First 3 rows:")
    print(df.head(3))

def main():
    files = [p for p in DATA_DIR.rglob("*") if p.is_file()]
    print(f"Found {len(files)} files under {DATA_DIR.relative_to(ROOT)}")

    for path in files:
        suffix = path.suffix.lower()
        if suffix == ".json":
            inspect_json(path)
        elif suffix == ".csv":
            inspect_csv(path)
        elif suffix in {".txt", ".md"}:
            continue
        else:
            print(f"\nSkipping unsupported file: {path.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
