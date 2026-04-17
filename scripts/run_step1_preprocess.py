from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mm_c.config import OUTPUT_DIR
from mm_c.data_io import load_dataset
from mm_c.preprocess import add_abnormal_flags, clean_dataset, save_preprocess_outputs


def main() -> None:
    df = load_dataset()
    cleaned, report = clean_dataset(df)
    cleaned = add_abnormal_flags(cleaned)
    save_preprocess_outputs(cleaned, report, OUTPUT_DIR)
    print("Step1 done -> outputs/step1_cleaned_dataset.csv")


if __name__ == "__main__":
    main()
