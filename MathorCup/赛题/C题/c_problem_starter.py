from __future__ import annotations

import argparse
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.feature_selection import mutual_info_classif, mutual_info_regression
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier, export_text


CONSTITUTION_NAMES = [
    "Balanced",
    "Qi_deficiency",
    "Yang_deficiency",
    "Yin_deficiency",
    "Phlegm_dampness",
    "Damp_heat",
    "Blood_stasis",
    "Qi_stagnation",
    "Special_diathesis",
]

RAW_TO_ENGLISH = {
    "样本ID": "sample_id",
    "体质标签": "constitution_tag",
    "平和质": "balanced_score",
    "气虚质": "qi_deficiency_score",
    "阳虚质": "yang_deficiency_score",
    "阴虚质": "yin_deficiency_score",
    "痰湿质": "phlegm_score",
    "湿热质": "damp_heat_score",
    "血瘀质": "blood_stasis_score",
    "气郁质": "qi_stagnation_score",
    "特禀质": "special_diathesis_score",
    "ADL用厕": "adl_toilet",
    "ADL吃饭": "adl_eat",
    "ADL步行": "adl_walk",
    "ADL穿衣": "adl_dress",
    "ADL洗澡": "adl_bath",
    "ADL总分": "adl_total",
    "IADL购物": "iadl_shop",
    "IADL做饭": "iadl_cook",
    "IADL理财": "iadl_finance",
    "IADL交通": "iadl_transport",
    "IADL服药": "iadl_medication",
    "IADL总分": "iadl_total",
    "活动量表总分（ADL总分+IADL总分）": "activity_total",
    "HDL-C（高密度脂蛋白）": "hdl",
    "LDL-C（低密度脂蛋白）": "ldl",
    "TG（甘油三酯）": "tg",
    "TC（总胆固醇）": "tc",
    "空腹血糖": "glucose",
    "血尿酸": "uric_acid",
    "BMI": "bmi",
    "高血脂症二分类标签": "label",
    "血脂异常分型标签（确诊病例）": "subtype",
    "年龄组": "age_group",
    "性别": "sex",
    "吸烟史": "smoke",
    "饮酒史": "drink",
}

CONSTITUTION_SCORE_COLS = [
    "balanced_score",
    "qi_deficiency_score",
    "yang_deficiency_score",
    "yin_deficiency_score",
    "phlegm_score",
    "damp_heat_score",
    "blood_stasis_score",
    "qi_stagnation_score",
    "special_diathesis_score",
]

ACTIVITY_LAB_COLS = [
    "adl_toilet",
    "adl_eat",
    "adl_walk",
    "adl_dress",
    "adl_bath",
    "adl_total",
    "iadl_shop",
    "iadl_cook",
    "iadl_finance",
    "iadl_transport",
    "iadl_medication",
    "iadl_total",
    "activity_total",
    "hdl",
    "ldl",
    "tg",
    "tc",
    "glucose",
    "uric_acid",
    "bmi",
]

ACTIVITY_ITEM_COLS = [
    "adl_toilet",
    "adl_eat",
    "adl_walk",
    "adl_dress",
    "adl_bath",
    "iadl_shop",
    "iadl_cook",
    "iadl_finance",
    "iadl_transport",
    "iadl_medication",
]
PROBLEM1_MAIN_COLS = [
    "adl_total",
    "iadl_total",
    "hdl",
    "ldl",
    "tg",
    "tc",
    "glucose",
    "uric_acid",
    "bmi",
]
PROBLEM1_ITEM_ALT_COLS = ACTIVITY_ITEM_COLS + [
    "hdl",
    "ldl",
    "tg",
    "tc",
    "glucose",
    "uric_acid",
    "bmi",
]

BASE_INFO_COLS = ["age_group", "sex", "smoke", "drink"]
DIRECT_LIPID_COLS = ["hdl", "ldl", "tg", "tc"]
MODELING_WINSOR_COLS = ["hdl", "ldl", "tg", "tc", "glucose", "uric_acid", "bmi"]
ACTIVITY_LIMIT_THRESHOLD = 8.0
WINSOR_LOWER_Q = 0.01
WINSOR_UPPER_Q = 0.99
GLUCOSE_HIGH_THRESHOLD = 6.1
BMI_HIGH_THRESHOLD = 23.9
PHLEGM_HIGH_THRESHOLD = 60.0
ACTIVITY_LOW_THRESHOLD = 60.0
URIC_ACID_HIGH_THRESHOLD = {0: 357.0, 1: 428.0}
DIAGNOSTIC_FEATURE_COLS = CONSTITUTION_SCORE_COLS + [
    "constitution_top_score",
    "constitution_margin",
    "adl_total",
    "iadl_total",
    "activity_limited_count",
    "ldl_w",
    "tg_log1p",
    "glucose_w",
    "uric_acid_log1p",
    "bmi_w",
    "non_hdl",
] + BASE_INFO_COLS
EARLY_WARNING_FEATURE_COLS = CONSTITUTION_SCORE_COLS + [
    "constitution_top_score",
    "constitution_margin",
    "adl_total",
    "iadl_total",
    "activity_limited_count",
    "glucose_w",
    "uric_acid_log1p",
    "bmi_w",
] + BASE_INFO_COLS

TCM_MONTHLY_COST = {1: 30, 2: 80, 3: 130}
TRAIN_UNIT_COST = {1: 3, 2: 5, 3: 8}
COMBO_FACTOR_COLS = [
    "lipid_abnormal",
    "uric_high",
    "glucose_high",
    "bmi_high",
    "smoke_yes",
    "drink_yes",
    "phlegm_high",
    "activity_low",
]
COMBO_FACTOR_LABELS = {
    "lipid_abnormal": "lipid_abnormal",
    "uric_high": "uric_high",
    "glucose_high": "glucose_high",
    "bmi_high": "bmi_high",
    "smoke_yes": "smoke_yes",
    "drink_yes": "drink_yes",
    "phlegm_high": "phlegm_high",
    "activity_low": "activity_low",
}


@dataclass
class PlanResult:
    sample_id: int
    age_group: int
    activity_total: float
    baseline_score: float
    target_score: float
    intensity: int
    frequency: int
    final_score: float
    total_cost: float
    meets_target: bool
    monthly_records: list[tuple[int, int, float, float, float]]


@dataclass
class AuditResult:
    total_rows: int
    total_cols: int
    missing_total: int
    duplicate_rows: int
    duplicate_sample_ids: int
    adl_total_match: int
    iadl_total_match: int
    activity_total_match: int
    subtype_consistent: int
    raw_constitution_tag_match: int


@dataclass
class ModelPreprocessor:
    clip_bounds: dict[str, tuple[float, float]]
    lower_q: float = WINSOR_LOWER_Q
    upper_q: float = WINSOR_UPPER_Q

def find_default_xlsx(root: Path) -> Path:
    for path in root.rglob("*.xlsx"):
        if path.name.startswith("~$"):
            continue
        if path.parent.name.startswith("C"):
            return path
    raise FileNotFoundError("Could not find the C-problem sample workbook.")


def load_dataframe(path: Path) -> "pd.DataFrame":
    df = pd.read_excel(path)

    missing = [col for col in RAW_TO_ENGLISH if col not in df.columns]
    if missing:
        raise ValueError(f"Workbook is missing expected columns: {missing}")

    df = df.rename(columns=RAW_TO_ENGLISH).copy()
    keep_cols = list(RAW_TO_ENGLISH.values())
    df = df[keep_cols]
    for col in keep_cols:
        df[col] = pd.to_numeric(df[col], errors="raise")
    raw_constitution_tag = df["constitution_tag"].to_numpy().astype(int)
    corrected_constitution_tag = dominant_constitution_codes(df).astype(int)
    df.attrs["raw_constitution_tag_match"] = int(
        (raw_constitution_tag == corrected_constitution_tag).sum()
    )
    df["constitution_tag"] = corrected_constitution_tag
    return df


def dominant_constitution_codes(df: "pd.DataFrame") -> np.ndarray:
    return df[CONSTITUTION_SCORE_COLS].to_numpy().argmax(axis=1) + 1


def audit_dataframe(df: "pd.DataFrame") -> AuditResult:
    adl_total_match = int(
        (
            df["adl_toilet"]
            + df["adl_eat"]
            + df["adl_walk"]
            + df["adl_dress"]
            + df["adl_bath"]
            == df["adl_total"]
        ).sum()
    )
    iadl_total_match = int(
        (
            df["iadl_shop"]
            + df["iadl_cook"]
            + df["iadl_finance"]
            + df["iadl_transport"]
            + df["iadl_medication"]
            == df["iadl_total"]
        ).sum()
    )
    activity_total_match = int(((df["adl_total"] + df["iadl_total"]) == df["activity_total"]).sum())
    subtype_consistent = int((((df["label"] == 0) & (df["subtype"] == 0)) | ((df["label"] == 1) & (df["subtype"] > 0))).sum())
    raw_constitution_tag_match = int(
        df.attrs.get(
            "raw_constitution_tag_match",
            (dominant_constitution_codes(df) == df["constitution_tag"].to_numpy()).sum(),
        )
    )
    return AuditResult(
        total_rows=int(len(df)),
        total_cols=int(df.shape[1]),
        missing_total=int(df.isna().sum().sum()),
        duplicate_rows=int(df.duplicated().sum()),
        duplicate_sample_ids=int(df["sample_id"].duplicated().sum()),
        adl_total_match=adl_total_match,
        iadl_total_match=iadl_total_match,
        activity_total_match=activity_total_match,
        subtype_consistent=subtype_consistent,
        raw_constitution_tag_match=raw_constitution_tag_match,
    )


def fit_model_preprocessor(train_df: "pd.DataFrame") -> ModelPreprocessor:
    clip_bounds = {}
    for col in MODELING_WINSOR_COLS:
        lower = float(train_df[col].quantile(WINSOR_LOWER_Q))
        upper = float(train_df[col].quantile(WINSOR_UPPER_Q))
        clip_bounds[col] = (lower, upper)
    return ModelPreprocessor(clip_bounds=clip_bounds)


def prepare_modeling_dataframe(
    df: "pd.DataFrame", preprocessor: ModelPreprocessor
) -> "pd.DataFrame":
    engineered = df.copy()

    constitution_scores = engineered[CONSTITUTION_SCORE_COLS].to_numpy()
    sorted_scores = np.sort(constitution_scores, axis=1)
    engineered["constitution_top_score"] = sorted_scores[:, -1]
    engineered["constitution_margin"] = sorted_scores[:, -1] - sorted_scores[:, -2]
    engineered["activity_limited_count"] = (
        engineered[ACTIVITY_ITEM_COLS] < ACTIVITY_LIMIT_THRESHOLD
    ).sum(axis=1).astype(float)

    for col, (lower, upper) in preprocessor.clip_bounds.items():
        engineered[f"{col}_w"] = engineered[col].clip(lower=lower, upper=upper)

    engineered["tg_log1p"] = np.log1p(engineered["tg_w"])
    engineered["uric_acid_log1p"] = np.log1p(engineered["uric_acid_w"])
    engineered["non_hdl"] = engineered["tc_w"] - engineered["hdl_w"]
    return engineered


def rank_problem1_candidates(
    df: "pd.DataFrame", candidate_cols: list[str]
) -> "pd.DataFrame":
    x_candidates = df[candidate_cols]
    y_phlegm = df["phlegm_score"]
    y_label = df["label"].astype(int)

    spearman_scores = {}
    for name in candidate_cols:
        spearman_scores[name] = float(spearmanr(x_candidates[name], y_phlegm).statistic)

    mi_reg = mutual_info_regression(x_candidates, y_phlegm, random_state=42)
    mi_clf = mutual_info_classif(x_candidates, y_label, random_state=42)

    rf_reg = RandomForestRegressor(n_estimators=400, random_state=42)
    rf_clf = RandomForestClassifier(n_estimators=400, random_state=42)
    rf_reg.fit(x_candidates, y_phlegm)
    rf_clf.fit(x_candidates, y_label)

    score_rows = []
    for i, name in enumerate(candidate_cols):
        score_rows.append(
            {
                "name": name,
                "spearman": spearman_scores[name],
                "spearman_abs": abs(spearman_scores[name]),
                "mi_reg": float(mi_reg[i]),
                "mi_clf": float(mi_clf[i]),
                "rf_reg": float(rf_reg.feature_importances_[i]),
                "rf_clf": float(rf_clf.feature_importances_[i]),
            }
        )
    score_df = pd.DataFrame(score_rows)

    points: dict[str, int] = {name: 0 for name in candidate_cols}
    for metric in ["spearman_abs", "mi_reg", "mi_clf", "rf_reg", "rf_clf"]:
        ordered = score_df.sort_values(metric, ascending=False)["name"].tolist()
        total = len(ordered)
        for pos, name in enumerate(ordered):
            points[name] += total - pos
        rank_map = {name: i + 1 for i, name in enumerate(ordered)}
        score_df[f"rank_{metric}"] = score_df["name"].map(rank_map)

    return (
        score_df.assign(consensus_score=score_df["name"].map(points))
        .sort_values("consensus_score", ascending=False)
        .reset_index(drop=True)
    )


def summarize_problem_1(df: "pd.DataFrame") -> dict[str, object]:
    y_phlegm = df["phlegm_score"]
    y_label = df["label"].astype(int)
    consensus = rank_problem1_candidates(df, PROBLEM1_MAIN_COLS)
    item_sensitivity = rank_problem1_candidates(df, PROBLEM1_ITEM_ALT_COLS)

    base_rate = float(y_label.mean())
    tag_rows = []
    for tag in range(1, 10):
        subset = df[df["constitution_tag"] == tag]
        rate = float(subset["label"].mean())
        tag_rows.append(
            {
                "tag": tag,
                "name": CONSTITUTION_NAMES[tag - 1],
                "count": int(len(subset)),
                "positive_rate": rate,
                "lift": rate / base_rate if base_rate else 0.0,
            }
        )
    tag_summary = pd.DataFrame(tag_rows)

    constitution_scaler = StandardScaler()
    z_constitution = pd.DataFrame(
        constitution_scaler.fit_transform(df[CONSTITUTION_SCORE_COLS]),
        columns=CONSTITUTION_SCORE_COLS,
        index=df.index,
    )
    logit_x = pd.concat([z_constitution, df[BASE_INFO_COLS].astype(float)], axis=1)
    constitution_logit = LogisticRegression(max_iter=5000, random_state=42)
    constitution_logit.fit(logit_x, y_label)
    constitution_beta = constitution_logit.coef_[0][: len(CONSTITUTION_SCORE_COLS)]
    constitution_prob = constitution_logit.predict_proba(logit_x)[:, 1]

    ame_rows = []
    for i, name in enumerate(CONSTITUTION_NAMES):
        beta = float(constitution_beta[i])
        ame = float(np.mean(constitution_prob * (1 - constitution_prob) * beta))
        ame_rows.append({"name": name, "coef": beta, "ame": ame, "abs_ame": abs(ame)})
    constitution_ame = pd.DataFrame(ame_rows)
    abs_ame_sum = float(constitution_ame["abs_ame"].sum())
    constitution_ame["share"] = (
        constitution_ame["abs_ame"] / abs_ame_sum if abs_ame_sum else 0.0
    )
    constitution_ame = constitution_ame.sort_values("abs_ame", ascending=False).reset_index(
        drop=True
    )

    return {
        "consensus": consensus,
        "item_sensitivity": item_sensitivity,
        "tag_summary": tag_summary,
        "constitution_ame": constitution_ame,
    }


def build_feature_matrix(
    df: "pd.DataFrame", preprocessor: ModelPreprocessor
) -> tuple["pd.DataFrame", list[str]]:
    prepared = prepare_modeling_dataframe(df, preprocessor)
    return prepared[DIAGNOSTIC_FEATURE_COLS].copy(), list(DIAGNOSTIC_FEATURE_COLS)


def build_early_warning_matrix(
    df: "pd.DataFrame", preprocessor: ModelPreprocessor
) -> tuple["pd.DataFrame", list[str]]:
    prepared = prepare_modeling_dataframe(df, preprocessor)
    return prepared[EARLY_WARNING_FEATURE_COLS].copy(), list(EARLY_WARNING_FEATURE_COLS)


def fit_risk_models(df: "pd.DataFrame") -> dict[str, object]:
    y = df["label"].astype(int)
    train_df, test_df, ya_train, ya_test = train_test_split(
        df, y, test_size=0.25, stratify=y, random_state=42
    )
    preprocessor = fit_model_preprocessor(train_df)

    xa_train, all_names = build_feature_matrix(train_df, preprocessor)
    xa_test, _ = build_feature_matrix(test_df, preprocessor)
    diagnostic_model = RandomForestClassifier(
        n_estimators=500, min_samples_leaf=5, random_state=42
    )
    diagnostic_model.fit(xa_train, ya_train)
    pa = diagnostic_model.predict_proba(xa_test)[:, 1]

    xe_train, ew_names = build_early_warning_matrix(train_df, preprocessor)
    xe_test, _ = build_early_warning_matrix(test_df, preprocessor)
    early_warning_model = RandomForestClassifier(
        n_estimators=500, min_samples_leaf=5, random_state=42
    )
    early_warning_model.fit(xe_train, ya_train)
    pe = early_warning_model.predict_proba(xe_test)[:, 1]

    rule_tree_names = [
        "phlegm_score",
        "activity_total",
        "hdl",
        "ldl",
        "tg",
        "tc",
        "glucose",
        "uric_acid",
        "bmi",
    ]
    rule_tree = DecisionTreeClassifier(max_depth=3, min_samples_leaf=40, random_state=42)
    rule_tree.fit(df[rule_tree_names], y)

    diagnostic_importance = (
        pd.DataFrame({"name": all_names, "importance": diagnostic_model.feature_importances_})
        .sort_values("importance", ascending=False)
        .reset_index(drop=True)
    )
    ew_importance = (
        pd.DataFrame({"name": ew_names, "importance": early_warning_model.feature_importances_})
        .sort_values("importance", ascending=False)
        .reset_index(drop=True)
    )
    risk_profile = annotate_risk_samples(df, early_warning_model, preprocessor)
    risk_counts = (
        risk_profile["risk_level"]
        .value_counts()
        .reindex(["low", "medium", "high"], fill_value=0)
        .rename_axis("level")
        .reset_index(name="count")
    )
    combo_summary = summarize_high_risk_combinations(risk_profile)

    return {
        "diagnostic_model": diagnostic_model,
        "early_warning_model": early_warning_model,
        "preprocessor": preprocessor,
        "diagnostic_auc": float(roc_auc_score(ya_test, pa)),
        "diagnostic_acc": float(accuracy_score(ya_test, pa >= 0.5)),
        "ew_auc": float(roc_auc_score(ya_test, pe)),
        "ew_acc": float(accuracy_score(ya_test, pe >= 0.5)),
        "diagnostic_importance": diagnostic_importance,
        "ew_importance": ew_importance,
        "rule_tree_text": export_text(rule_tree, feature_names=rule_tree_names),
        "risk_profile": risk_profile,
        "risk_counts": risk_counts,
        "high_risk_base_rate": combo_summary["high_risk_base_rate"],
        "combo_pairs": combo_summary["pair_summary"],
        "combo_triples": combo_summary["triple_summary"],
        "combo_all": combo_summary["all_summary"],
        "rule_driven_pair": combo_summary["rule_driven_pair"],
    }


def lipid_abnormal_count(row: "pd.Series") -> int:
    return int(
        (row["tc"] > 6.2)
        + (row["tg"] > 1.7)
        + (row["ldl"] > 3.1)
        + (row["hdl"] < 1.04)
    )


def build_early_warning_row(
    row: "pd.Series", preprocessor: ModelPreprocessor
) -> "pd.DataFrame":
    row_df = pd.DataFrame([row.to_dict()])
    prepared = prepare_modeling_dataframe(row_df, preprocessor)
    return prepared[EARLY_WARNING_FEATURE_COLS]


def assign_risk_level(
    row: "pd.Series",
    early_warning_model: RandomForestClassifier,
    preprocessor: ModelPreprocessor,
) -> tuple[str, float]:
    prob = float(
        early_warning_model.predict_proba(build_early_warning_row(row, preprocessor))[0, 1]
    )
    phlegm = float(row["phlegm_score"])
    activity = float(row["activity_total"])
    abnormal = lipid_abnormal_count(row)

    if (abnormal >= 1 and phlegm >= 60) or (
        abnormal == 0 and phlegm >= 80 and activity < 40
    ) or prob >= 0.80:
        return "high", prob
    if abnormal >= 1 or phlegm >= 60 or (prob >= 0.45 and activity < 60):
        return "medium", prob
    return "low", prob


def summarize_risk_levels(
    df: "pd.DataFrame",
    early_warning_model: RandomForestClassifier,
    preprocessor: ModelPreprocessor,
) -> "pd.DataFrame":
    annotated = annotate_risk_samples(df, early_warning_model, preprocessor)
    return (
        annotated["risk_level"]
        .value_counts()
        .reindex(["low", "medium", "high"], fill_value=0)
        .rename_axis("level")
        .reset_index(name="count")
    )


def uric_acid_upper_limit(sex: int) -> float:
    return URIC_ACID_HIGH_THRESHOLD.get(int(sex), 428.0)


def annotate_risk_samples(
    df: "pd.DataFrame",
    early_warning_model: RandomForestClassifier,
    preprocessor: ModelPreprocessor,
) -> "pd.DataFrame":
    annotated = df.copy()
    levels: list[str] = []
    probs: list[float] = []
    for _, row in annotated.iterrows():
        level, prob = assign_risk_level(row, early_warning_model, preprocessor)
        levels.append(level)
        probs.append(prob)

    annotated["risk_level"] = levels
    annotated["ew_prob"] = probs
    annotated["high_risk"] = annotated["risk_level"].eq("high")
    annotated["lipid_abnormal"] = annotated.apply(lipid_abnormal_count, axis=1) >= 1
    annotated["uric_high"] = annotated.apply(
        lambda row: float(row["uric_acid"]) > uric_acid_upper_limit(int(row["sex"])),
        axis=1,
    )
    annotated["glucose_high"] = annotated["glucose"] > GLUCOSE_HIGH_THRESHOLD
    annotated["bmi_high"] = annotated["bmi"] > BMI_HIGH_THRESHOLD
    annotated["smoke_yes"] = annotated["smoke"] == 1
    annotated["drink_yes"] = annotated["drink"] == 1
    annotated["phlegm_high"] = annotated["phlegm_score"] >= PHLEGM_HIGH_THRESHOLD
    annotated["activity_low"] = annotated["activity_total"] < ACTIVITY_LOW_THRESHOLD
    return annotated


def format_combo_label(combo: tuple[str, ...]) -> str:
    return " + ".join(COMBO_FACTOR_LABELS[name] for name in combo)


def summarize_high_risk_combinations(
    risk_df: "pd.DataFrame",
    min_high_count: int = 80,
    min_lift: float = 1.05,
    top_n: int = 5,
) -> dict[str, object]:
    high_risk_base_rate = float(risk_df["high_risk"].mean())
    high_risk_total = int(risk_df["high_risk"].sum())
    rows: list[dict[str, object]] = []

    for size in (2, 3):
        for combo in combinations(COMBO_FACTOR_COLS, size):
            mask = risk_df[list(combo)].all(axis=1)
            count_all = int(mask.sum())
            if count_all == 0:
                continue

            count_high = int((mask & risk_df["high_risk"]).sum())
            if count_high == 0:
                continue

            confidence = count_high / count_all
            lift = confidence / high_risk_base_rate if high_risk_base_rate else np.nan
            support_high = count_high / high_risk_total if high_risk_total else np.nan
            rows.append(
                {
                    "size": size,
                    "pattern_key": "|".join(combo),
                    "pattern_label": format_combo_label(combo),
                    "count_all": count_all,
                    "count_high": count_high,
                    "confidence": confidence,
                    "lift": lift,
                    "support_high": support_high,
                }
            )

    all_summary = (
        pd.DataFrame(rows)
        .sort_values(["size", "count_high", "lift", "confidence"], ascending=[True, False, False, False])
        .reset_index(drop=True)
    )
    filtered = all_summary[
        (all_summary["count_high"] >= min_high_count) & (all_summary["lift"] > min_lift)
    ].copy()
    pair_summary = (
        filtered[filtered["size"] == 2]
        .sort_values(["count_high", "lift", "confidence"], ascending=[False, False, False])
        .head(top_n)
        .reset_index(drop=True)
    )
    triple_summary = (
        filtered[filtered["size"] == 3]
        .sort_values(["count_high", "lift", "confidence"], ascending=[False, False, False])
        .head(top_n)
        .reset_index(drop=True)
    )
    rule_driven_pair = all_summary[all_summary["pattern_key"] == "lipid_abnormal|phlegm_high"]
    if rule_driven_pair.empty:
        rule_driven_pair_dict: dict[str, object] | None = None
    else:
        rule_driven_pair_dict = rule_driven_pair.iloc[0].to_dict()

    return {
        "high_risk_base_rate": high_risk_base_rate,
        "all_summary": all_summary,
        "pair_summary": pair_summary,
        "triple_summary": triple_summary,
        "rule_driven_pair": rule_driven_pair_dict,
    }


def tcm_level(score: float) -> int:
    if score <= 58:
        return 1
    if score <= 61:
        return 2
    return 3


def allowed_intensities(age_group: int, activity_total: float) -> list[int]:
    if age_group <= 2:
        age_allowed = {1, 2, 3}
    elif age_group <= 4:
        age_allowed = {1, 2}
    else:
        age_allowed = {1}

    if activity_total < 40:
        score_allowed = {1}
    elif activity_total < 60:
        score_allowed = {1, 2}
    else:
        score_allowed = {1, 2, 3}

    return sorted(age_allowed & score_allowed)


def activity_monthly_drop(intensity: int, frequency: int) -> float:
    if frequency < 5:
        return 0.0
    return 0.03 * (intensity - 1) + 0.01 * (frequency - 5)


def simulate_plan(
    baseline_score: float,
    intensity: int,
    frequency: int,
    months: int = 6,
) -> tuple[float, float, list[tuple[int, int, float, float, float]]]:
    score = float(baseline_score)
    total_cost = 0.0
    history = []
    monthly_drop = activity_monthly_drop(intensity, frequency)

    for month in range(1, months + 1):
        current_tcm_level = tcm_level(score)
        tcm_cost = TCM_MONTHLY_COST[current_tcm_level]
        train_cost = TRAIN_UNIT_COST[intensity] * frequency * 4
        total_cost += tcm_cost + train_cost
        score = score * (1 - monthly_drop)
        history.append((month, current_tcm_level, round(score, 3), tcm_cost, train_cost))

    return score, total_cost, history


def optimize_intervention(
    row: "pd.Series",
    target_ratio: float = 0.90,
    budget: float = 2000.0,
) -> PlanResult:
    sample_id = int(row["sample_id"])
    age_group = int(row["age_group"])
    activity_total = float(row["activity_total"])
    baseline_score = float(row["phlegm_score"])
    target_score = baseline_score * target_ratio

    candidates = []
    for intensity in allowed_intensities(age_group, activity_total):
        for frequency in range(1, 11):
            final_score, total_cost, history = simulate_plan(
                baseline_score, intensity, frequency
            )
            meets_target = final_score <= target_score and total_cost <= budget
            candidates.append(
                PlanResult(
                    sample_id=sample_id,
                    age_group=age_group,
                    activity_total=activity_total,
                    baseline_score=baseline_score,
                    target_score=target_score,
                    intensity=intensity,
                    frequency=frequency,
                    final_score=final_score,
                    total_cost=total_cost,
                    meets_target=meets_target,
                    monthly_records=history,
                )
            )

    candidates.sort(
        key=lambda item: (
            not item.meets_target,
            item.total_cost,
            item.final_score,
            -item.frequency,
        )
    )
    return candidates[0]


def print_problem_1(summary: dict[str, object]) -> None:
    print("=== Problem 1: main-analysis indicators ===")
    for _, row in summary["consensus"].iterrows():
        print(
            f"{row['name']:<22} "
            f"spearman={row['spearman']:+.3f} "
            f"mi_phlegm={row['mi_reg']:.3f} "
            f"mi_label={row['mi_clf']:.3f}"
        )

    print("\nSupplementary mixed item-level analysis")
    for _, row in summary["item_sensitivity"].head(10).iterrows():
        print(
            f"{row['name']:<22} "
            f"spearman={row['spearman']:+.3f} "
            f"mi_phlegm={row['mi_reg']:.3f} "
            f"mi_label={row['mi_clf']:.3f}"
        )

    print("\nDominant constitution positive rates")
    for _, row in summary["tag_summary"].iterrows():
        print(
            f"{int(row['tag'])}. {row['name']:<18} "
            f"n={int(row['count']):<3d} "
            f"rate={row['positive_rate']:.3f} "
            f"lift={row['lift']:.3f}"
        )

    print("\nModel-based constitution contribution (standardized logit + AME)")
    for _, row in summary["constitution_ame"].iterrows():
        print(
            f"{row['name']:<18} "
            f"coef={row['coef']:+.3f} "
            f"ame={row['ame']:+.4f} "
            f"share={row['share']:.3f}"
        )


def print_preprocessing_audit(audit: AuditResult) -> None:
    print("=== Data audit ===")
    print(
        f"missing_total={audit.missing_total}, duplicate_rows={audit.duplicate_rows}, "
        f"duplicate_sample_ids={audit.duplicate_sample_ids}"
    )
    print(
        f"adl_total_consistency={audit.adl_total_match}/{audit.total_rows}, "
        f"iadl_total_consistency={audit.iadl_total_match}/{audit.total_rows}, "
        f"activity_total_consistency={audit.activity_total_match}/{audit.total_rows}"
    )
    print(
        f"label_subtype_consistency={audit.subtype_consistent}/{audit.total_rows}, "
        f"raw_constitution_tag_match={audit.raw_constitution_tag_match}/{audit.total_rows}, "
        f"raw_constitution_tag_corrected={audit.total_rows - audit.raw_constitution_tag_match}"
    )


def print_problem_2(summary: dict[str, object], df: "pd.DataFrame") -> None:
    print("\n=== Problem 2: risk model ===")
    print(
        f"Train-based winsorization ({summary['preprocessor'].lower_q:.0%}-{summary['preprocessor'].upper_q:.0%}) "
        f"applied to: {', '.join(MODELING_WINSOR_COLS)}"
    )
    print(
        "Derived features: tg_log1p, uric_acid_log1p, non_hdl, "
        "activity_limited_count, "
        "constitution_top_score, constitution_margin"
    )
    print(
        f"Diagnostic model   AUC={summary['diagnostic_auc']:.4f} "
        f"ACC={summary['diagnostic_acc']:.4f}"
    )
    print(
        f"Early warning model AUC={summary['ew_auc']:.4f} "
        f"ACC={summary['ew_acc']:.4f}"
    )

    print("\nTop diagnostic features")
    for _, row in summary["diagnostic_importance"].head(10).iterrows():
        print(f"{row['name']:<22} {row['importance']:.4f}")

    print("\nTop early warning features")
    for _, row in summary["ew_importance"].head(10).iterrows():
        print(f"{row['name']:<22} {row['importance']:.4f}")

    print("\nRule tree with direct lipids")
    print(summary["rule_tree_text"].strip())

    print("Assigned low/medium/high counts")
    for _, row in summary["risk_counts"].iterrows():
        print(f"{row['level']:<6} {int(row['count'])}")

    print(
        f"\nHigh-risk base rate = {summary['high_risk_base_rate']:.3f} "
        "(used for combination lift)"
    )
    print("Top pairwise high-risk combinations")
    for _, row in summary["combo_pairs"].iterrows():
        print(
            f"{row['pattern_label']:<45} "
            f"high={int(row['count_high']):<3d} "
            f"conf={row['confidence']:.3f} "
            f"lift={row['lift']:.3f}"
        )

    print("\nTop triple high-risk combinations")
    for _, row in summary["combo_triples"].iterrows():
        print(
            f"{row['pattern_label']:<45} "
            f"high={int(row['count_high']):<3d} "
            f"conf={row['confidence']:.3f} "
            f"lift={row['lift']:.3f}"
        )

    if summary["rule_driven_pair"] is not None:
        row = summary["rule_driven_pair"]
        print(
            "\nRule-driven pattern check\n"
            f"{row['pattern_label']:<45} "
            f"high={int(row['count_high']):<3d} "
            f"conf={row['confidence']:.3f} "
            f"lift={row['lift']:.3f}"
        )


def print_problem_3(
    df: "pd.DataFrame",
    sample_ids: list[int],
    target_ratio: float,
    budget: float,
) -> None:
    print("\n=== Problem 3: intervention optimization ===")
    for sample_id in sample_ids:
        matches = df[df["sample_id"] == sample_id]
        if matches.empty:
            print(f"Sample {sample_id} not found.")
            continue

        result = optimize_intervention(matches.iloc[0], target_ratio=target_ratio, budget=budget)
        print(
            f"Sample {sample_id}: baseline={result.baseline_score:.1f}, "
            f"target<={result.target_score:.1f}, activity_total={result.activity_total:.1f}, "
            f"age_group={result.age_group}"
        )
        print(
            f"  plan: intensity={result.intensity}, frequency={result.frequency}/week, "
            f"final={result.final_score:.2f}, cost={result.total_cost:.0f}, "
            f"meets_target={result.meets_target}"
        )
        for month, level, score, tcm_cost, train_cost in result.monthly_records:
            print(
                f"  month {month}: tcm_level={level}, score={score:.3f}, "
                f"tcm_cost={tcm_cost:.0f}, train_cost={train_cost:.0f}"
            )


def main() -> None:
    parser = argparse.ArgumentParser(description="Pandas-based starter analysis for the MathorCup C problem.")
    parser.add_argument("--xlsx", type=Path, default=None, help="Path to the sample workbook.")
    parser.add_argument("--budget", type=float, default=2000.0, help="6-month intervention budget.")
    parser.add_argument(
        "--target-ratio",
        type=float,
        default=0.90,
        help="Target final phlegm score as a ratio of baseline score.",
    )
    parser.add_argument(
        "--sample-ids",
        type=int,
        nargs="*",
        default=[1, 2, 3],
        help="Sample IDs for the intervention section.",
    )
    args = parser.parse_args()

    workbook = args.xlsx or find_default_xlsx(Path.cwd())
    df = load_dataframe(workbook)
    audit = audit_dataframe(df)
    print(f"Workbook: {workbook}")
    print(f"Rows={len(df)}, Cols={df.shape[1]}")
    print_preprocessing_audit(audit)

    problem_1 = summarize_problem_1(df)
    problem_2 = fit_risk_models(df)

    print_problem_1(problem_1)
    print_problem_2(problem_2, df)
    print_problem_3(df, args.sample_ids, args.target_ratio, args.budget)


if __name__ == "__main__":
    main()
