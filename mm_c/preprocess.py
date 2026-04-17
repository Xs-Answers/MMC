from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from mm_c.config import LIPID_NORMAL_RANGES


def _winsorize_iqr(series: pd.Series, k: float = 1.5) -> pd.Series:
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    low = q1 - k * iqr
    high = q3 + k * iqr
    return series.clip(lower=low, upper=high)


def clean_dataset(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, float]]:
    """Impute missing values and clip extreme outliers."""
    cleaned = df.copy()
    missing_before = cleaned.isna().sum().sum()

    for col in cleaned.columns:
        med = cleaned[col].median()
        cleaned[col] = cleaned[col].fillna(med)
        if col not in {"sample_id", "constitution_tag", "hyperlipidemia_label", "lipid_subtype", "age_group", "sex", "smoke", "drink"}:
            cleaned[col] = _winsorize_iqr(cleaned[col])

    missing_after = cleaned.isna().sum().sum()
    report = {
        "rows": float(cleaned.shape[0]),
        "cols": float(cleaned.shape[1]),
        "missing_before": float(missing_before),
        "missing_after": float(missing_after),
    }
    return cleaned, report


def add_abnormal_flags(df: pd.DataFrame) -> pd.DataFrame:
    """Add abnormal flags for core blood indicators."""
    out = df.copy()
    for metric, (lo, hi) in LIPID_NORMAL_RANGES.items():
        out[f"{metric}_high"] = (out[metric] > hi).astype(int)
        out[f"{metric}_low"] = (out[metric] < lo).astype(int)

    male_ua = (208, 428)
    female_ua = (155, 357)
    lo = np.where(out["sex"] == 1, male_ua[0], female_ua[0])
    hi = np.where(out["sex"] == 1, male_ua[1], female_ua[1])
    out["uric_acid_high"] = (out["uric_acid"] > hi).astype(int)
    out["uric_acid_low"] = (out["uric_acid"] < lo).astype(int)
    out["lipid_abnormal_count"] = out[["tc_high", "tg_high", "ldl_high", "hdl_low"]].sum(axis=1)
    return out


def save_preprocess_outputs(df: pd.DataFrame, report: dict[str, float], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_dir / "step1_cleaned_dataset.csv", index=False, encoding="utf-8-sig")
    with (output_dir / "step1_clean_report.json").open("w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

