from __future__ import annotations

from mm_c.data_io import load_dataset
from mm_c.preprocess import add_abnormal_flags, clean_dataset


def test_load_and_clean_smoke() -> None:
    df = load_dataset()
    cleaned, report = clean_dataset(df)
    assert cleaned.shape[0] > 0
    assert report["missing_after"] == 0

    with_flags = add_abnormal_flags(cleaned)
    assert "lipid_abnormal_count" in with_flags.columns

