from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mm_c.config import OUTPUT_DIR
from mm_c.data_io import load_dataset
from mm_c.preprocess import add_abnormal_flags, clean_dataset
from mm_c.problem1_analysis import run_problem1


def main() -> None:
    if (OUTPUT_DIR / "step1_cleaned_dataset.csv").exists():
        df = pd.read_csv(OUTPUT_DIR / "step1_cleaned_dataset.csv")
    else:
        raw = load_dataset()
        df, _ = clean_dataset(raw)
        df = add_abnormal_flags(df)

    run_problem1(df, OUTPUT_DIR)
    print("Step2 done -> outputs/problem1_*.csv")


if __name__ == "__main__":
    main()
