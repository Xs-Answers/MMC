from __future__ import annotations

import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import shap
from scipy.stats import mannwhitneyu, spearmanr, ttest_ind
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import LassoCV, LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier, XGBRegressor

from mm_c.config import ACTIVITY_LAB_NAMES, CONSTITUTION_NAMES


def run_correlation_and_tests(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    feature_cols = ACTIVITY_LAB_NAMES
    y_phlegm = df["phlegm_dampness"]
    y_label = df["hyperlipidemia_label"]

    corr_rows = []
    test_rows = []
    for col in feature_cols:
        coef, p_val = spearmanr(df[col], y_phlegm)
        corr_rows.append({"feature": col, "spearman_r": coef, "spearman_p": p_val})

        g0 = df.loc[y_label == 0, col]
        g1 = df.loc[y_label == 1, col]
        t_res = ttest_ind(g0, g1, equal_var=False, nan_policy="omit")
        u_stat, u_p = mannwhitneyu(g0, g1, alternative="two-sided")
        test_rows.append(
            {
                "feature": col,
                "t_stat": float(t_res.statistic),
                "t_p": float(t_res.pvalue),
                "u_stat": float(u_stat),
                "u_p": float(u_p),
            }
        )

    corr_df = pd.DataFrame(corr_rows).sort_values("spearman_r", ascending=False)
    test_df = pd.DataFrame(test_rows).sort_values("u_p")
    return corr_df, test_df


def run_lasso_xgb_importance(df: pd.DataFrame) -> pd.DataFrame:
    feature_cols = ACTIVITY_LAB_NAMES
    x = df[feature_cols].values
    y_phlegm = df["phlegm_dampness"].values
    y_label = df["hyperlipidemia_label"].astype(int).values

    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(x)

    # LassoCV may emit convergence warnings on noisy medical indicators; tune iterations for stability.
    lasso = LassoCV(cv=5, random_state=42, max_iter=30000, tol=1e-4)
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=ConvergenceWarning)
        lasso.fit(x_scaled, y_phlegm)

    # Use L2 logistic coefficients to avoid deprecation warnings in newer sklearn versions.
    logit = LogisticRegression(solver="liblinear", max_iter=8000)
    logit.fit(x_scaled, y_label)

    xgb_reg = XGBRegressor(n_estimators=300, max_depth=4, learning_rate=0.05, subsample=0.8, colsample_bytree=0.8, random_state=42)
    xgb_clf = XGBClassifier(n_estimators=300, max_depth=4, learning_rate=0.05, subsample=0.8, colsample_bytree=0.8, eval_metric="logloss", random_state=42)
    xgb_reg.fit(x, y_phlegm)
    xgb_clf.fit(x, y_label)

    out = pd.DataFrame(
        {
            "feature": feature_cols,
            "lasso_coef": lasso.coef_,
            "logit_coef": logit.coef_[0],
            "xgb_reg_importance": xgb_reg.feature_importances_,
            "xgb_clf_importance": xgb_clf.feature_importances_,
        }
    )
    out["score"] = (
        np.abs(out["lasso_coef"])
        + np.abs(out["logit_coef"])
        + out["xgb_reg_importance"]
        + out["xgb_clf_importance"]
    )
    return out.sort_values("score", ascending=False)


def run_constitution_or_shap(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    x = df[CONSTITUTION_NAMES]
    y = df["hyperlipidemia_label"].astype(int)

    scaler = StandardScaler()
    xs = scaler.fit_transform(x)

    logit = LogisticRegression(max_iter=3000)
    logit.fit(xs, y)
    or_df = pd.DataFrame(
        {
            "constitution": CONSTITUTION_NAMES,
            "coef": logit.coef_[0],
            "odds_ratio": np.exp(logit.coef_[0]),
        }
    ).sort_values("odds_ratio", ascending=False)

    x_train, x_test, y_train, _ = train_test_split(x, y, test_size=0.25, stratify=y, random_state=42)
    xgb = XGBClassifier(n_estimators=300, max_depth=4, learning_rate=0.05, subsample=0.8, colsample_bytree=0.8, eval_metric="logloss", random_state=42)
    xgb.fit(x_train, y_train)

    explainer = shap.TreeExplainer(xgb)
    shap_values = explainer.shap_values(x_test)
    if isinstance(shap_values, list):
        shap_values = shap_values[1]

    shap_df = pd.DataFrame(
        {
            "constitution": CONSTITUTION_NAMES,
            "mean_abs_shap": np.abs(shap_values).mean(axis=0),
        }
    ).sort_values("mean_abs_shap", ascending=False)
    return or_df, shap_df


def run_problem1(df: pd.DataFrame, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    corr_df, test_df = run_correlation_and_tests(df)
    imp_df = run_lasso_xgb_importance(df)
    or_df, shap_df = run_constitution_or_shap(df)

    corr_df.to_csv(output_dir / "problem1_spearman.csv", index=False, encoding="utf-8-sig")
    test_df.to_csv(output_dir / "problem1_group_tests.csv", index=False, encoding="utf-8-sig")
    imp_df.to_csv(output_dir / "problem1_feature_importance.csv", index=False, encoding="utf-8-sig")
    or_df.to_csv(output_dir / "problem1_constitution_or.csv", index=False, encoding="utf-8-sig")
    shap_df.to_csv(output_dir / "problem1_constitution_shap.csv", index=False, encoding="utf-8-sig")

    with (output_dir / "problem1_top_summary.json").open("w", encoding="utf-8") as f:
        json.dump(
            {
                "top_features": imp_df.head(10)["feature"].tolist(),
                "top_constitution_or": or_df.head(3)["constitution"].tolist(),
                "top_constitution_shap": shap_df.head(3)["constitution"].tolist(),
            },
            f,
            ensure_ascii=False,
            indent=2,
        )

