from __future__ import annotations

from pathlib import Path

import pandas as pd

from mm_c.config import BASE_COLUMNS, DEFAULT_XLSX


def load_dataset(xlsx_path: Path | None = None) -> pd.DataFrame:
    """Load workbook and remap columns to fixed schema by position."""
    path = xlsx_path or DEFAULT_XLSX
    df = pd.read_excel(path, engine="openpyxl")
    if df.shape[1] < len(BASE_COLUMNS):
        raise ValueError(f"Expected at least {len(BASE_COLUMNS)} columns, got {df.shape[1]}.")

    df = df.iloc[:, : len(BASE_COLUMNS)].copy()
    df.columns = BASE_COLUMNS
    for col in BASE_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def ensure_output_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)

