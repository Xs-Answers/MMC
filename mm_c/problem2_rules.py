from __future__ import annotations

from pathlib import Path

import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules


def _binarize_for_rules(df: pd.DataFrame) -> pd.DataFrame:
    x = pd.DataFrame()
    x["phlegm_high"] = (df["phlegm_dampness"] >= 60).astype(int)
    x["activity_low"] = (df["activity_total"] < 40).astype(int)
    x["tc_high"] = (df["tc"] > 6.2).astype(int)
    x["tg_high"] = (df["tg"] > 1.7).astype(int)
    x["ldl_high"] = (df["ldl"] > 3.1).astype(int)
    x["hdl_low"] = (df["hdl"] < 1.04).astype(int)
    x["risk_high"] = (df["risk_level"] == "high").astype(int)
    x["risk_medium_or_high"] = df["risk_level"].isin(["medium", "high"]).astype(int)
    return x


def run_problem2_rules(risk_df: pd.DataFrame, output_dir: Path, min_support: float = 0.05) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    bin_df = _binarize_for_rules(risk_df)

    freq = apriori(bin_df.astype(bool), min_support=min_support, use_colnames=True)
    if freq.empty:
        empty = pd.DataFrame(columns=["antecedents", "consequents", "support", "confidence", "lift"])
        empty.to_csv(output_dir / "problem2_association_rules.csv", index=False, encoding="utf-8-sig")
        return empty

    rules = association_rules(freq, metric="confidence", min_threshold=0.5)
    rules = rules[["antecedents", "consequents", "support", "confidence", "lift"]].copy()
    rules["antecedents"] = rules["antecedents"].astype(str)
    rules["consequents"] = rules["consequents"].astype(str)

    rules = rules[rules["consequents"].str.contains("risk_high|risk_medium_or_high", regex=True)]
    rules = rules.sort_values(["lift", "confidence", "support"], ascending=False)
    rules.to_csv(output_dir / "problem2_association_rules.csv", index=False, encoding="utf-8-sig")
    return rules

