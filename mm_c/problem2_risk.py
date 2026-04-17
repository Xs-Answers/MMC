from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, roc_curve
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text

from mm_c.config import CONSTITUTION_NAMES


def _youden_threshold(y_true: np.ndarray, proba: np.ndarray) -> float:
    fpr, tpr, thresholds = roc_curve(y_true, proba)
    idx = np.argmax(tpr - fpr)
    return float(thresholds[idx])


def build_problem2_features(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    feature_cols = CONSTITUTION_NAMES + [
        "adl_total",
        "iadl_total",
        "activity_total",
        "glucose",
        "uric_acid",
        "bmi",
        "age_group",
        "sex",
        "smoke",
        "drink",
    ]
    return df[feature_cols].copy(), feature_cols


def fit_risk_model(df: pd.DataFrame) -> tuple[RandomForestClassifier, dict[str, float], list[str], float, float]:
    x, feature_cols = build_problem2_features(df)
    y = df["hyperlipidemia_label"].astype(int)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, stratify=y, random_state=42)
    model = RandomForestClassifier(n_estimators=500, min_samples_leaf=5, random_state=42)
    model.fit(x_train, y_train)

    proba = model.predict_proba(x_test)[:, 1]
    y_hat = (proba >= 0.5).astype(int)

    low_cut = _youden_threshold(y_test.to_numpy(), proba)
    high_cut = max(0.8, low_cut + 0.2)

    metrics = {
        "auc": float(roc_auc_score(y_test, proba)),
        "accuracy": float(accuracy_score(y_test, y_hat)),
    }
    return model, metrics, feature_cols, low_cut, high_cut


def fit_cart_threshold_tree(df: pd.DataFrame) -> str:
    cart_features = ["phlegm_dampness", "activity_total", "hdl", "ldl", "tg", "tc", "glucose", "uric_acid", "bmi"]
    x = df[cart_features]
    y = df["hyperlipidemia_label"].astype(int)
    tree = DecisionTreeClassifier(max_depth=3, min_samples_leaf=30, random_state=42)
    tree.fit(x, y)
    return export_text(tree, feature_names=cart_features)


def assign_risk_level(row: pd.Series, prob: float, low_cut: float, high_cut: float) -> str:
    abnormal = int(row["tc"] > 6.2) + int(row["tg"] > 1.7) + int(row["ldl"] > 3.1) + int(row["hdl"] < 1.04)
    if (abnormal >= 1 and row["phlegm_dampness"] >= 60) or (abnormal == 0 and row["phlegm_dampness"] >= 80 and row["activity_total"] < 40):
        return "high"
    if prob >= high_cut:
        return "high"
    if abnormal >= 1 or row["phlegm_dampness"] >= 60 or prob >= low_cut:
        return "medium"
    return "low"


def run_problem2(df: pd.DataFrame, output_dir: Path) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)
    model, metrics, feature_cols, low_cut, high_cut = fit_risk_model(df)
    tree_rules = fit_cart_threshold_tree(df)

    x_all = df[feature_cols]
    prob = model.predict_proba(x_all)[:, 1]
    pred = []
    for i, row in df.iterrows():
        pred.append(assign_risk_level(row, float(prob[i]), low_cut, high_cut))

    out = df[["sample_id", "hyperlipidemia_label", "phlegm_dampness", "activity_total", "tc", "tg", "ldl", "hdl"]].copy()
    out["risk_probability"] = prob
    out["risk_level"] = pred
    out.to_csv(output_dir / "problem2_risk_predictions.csv", index=False, encoding="utf-8-sig")

    fi = pd.DataFrame({"feature": feature_cols, "importance": model.feature_importances_}).sort_values("importance", ascending=False)
    fi.to_csv(output_dir / "problem2_feature_importance.csv", index=False, encoding="utf-8-sig")

    risk_counts = out["risk_level"].value_counts().to_dict()
    with (output_dir / "problem2_summary.json").open("w", encoding="utf-8") as f:
        json.dump(
            {
                "metrics": metrics,
                "thresholds": {"low_cut": low_cut, "high_cut": high_cut},
                "risk_counts": risk_counts,
                "cart_rules": tree_rules,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )

    return out

