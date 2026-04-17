from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.metrics import auc, roc_curve


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _df_to_markdown(df: pd.DataFrame, max_rows: int = 10) -> str:
    view = df.head(max_rows).copy()
    headers = list(view.columns)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for _, row in view.iterrows():
        values = [str(row[h]) for h in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_problem2_artifacts(output_dir: Path) -> dict[str, Path]:
    figures_dir = output_dir / "figures"
    tables_dir = output_dir / "tables"
    _ensure_dir(figures_dir)
    _ensure_dir(tables_dir)

    risk_df = pd.read_csv(output_dir / "problem2_risk_predictions.csv")
    fi_df = pd.read_csv(output_dir / "problem2_feature_importance.csv")
    rules_df = pd.read_csv(output_dir / "problem2_association_rules.csv")

    risk_table = (
        risk_df["risk_level"].value_counts(dropna=False).rename_axis("risk_level").reset_index(name="count")
    )
    risk_table["ratio"] = (risk_table["count"] / risk_table["count"].sum()).round(4)
    risk_table.to_csv(tables_dir / "problem2_risk_level_table.csv", index=False, encoding="utf-8-sig")

    top_rules = rules_df.head(10).copy()
    top_rules.to_csv(tables_dir / "problem2_top_rules_table.csv", index=False, encoding="utf-8-sig")

    plt.figure(figsize=(7, 4))
    sns.barplot(data=risk_table, x="risk_level", y="count", hue="risk_level", legend=False)
    plt.title("Problem 2 Risk Level Counts")
    plt.xlabel("Risk level")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(figures_dir / "problem2_risk_level_counts.png", dpi=150)
    plt.close()

    top_fi = fi_df.head(10).sort_values("importance")
    plt.figure(figsize=(8, 5))
    plt.barh(top_fi["feature"], top_fi["importance"])
    plt.title("Problem 2 Top-10 Feature Importance")
    plt.xlabel("Importance")
    plt.ylabel("Feature")
    plt.tight_layout()
    plt.savefig(figures_dir / "problem2_top10_feature_importance.png", dpi=150)
    plt.close()

    y_true = risk_df["hyperlipidemia_label"].astype(int)
    y_score = risk_df["risk_probability"]
    fpr, tpr, _ = roc_curve(y_true, y_score)
    roc_auc = auc(fpr, tpr)

    plt.figure(figsize=(6, 5))
    plt.plot(fpr, tpr, label=f"AUC={roc_auc:.3f}")
    plt.plot([0, 1], [0, 1], linestyle="--")
    plt.title("Problem 2 ROC Curve")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig(figures_dir / "problem2_roc_curve.png", dpi=150)
    plt.close()

    return {
        "risk_table": tables_dir / "problem2_risk_level_table.csv",
        "rules_table": tables_dir / "problem2_top_rules_table.csv",
        "risk_fig": figures_dir / "problem2_risk_level_counts.png",
        "fi_fig": figures_dir / "problem2_top10_feature_importance.png",
        "roc_fig": figures_dir / "problem2_roc_curve.png",
    }


def build_problem3_artifacts(output_dir: Path) -> dict[str, Path]:
    figures_dir = output_dir / "figures"
    tables_dir = output_dir / "tables"
    _ensure_dir(figures_dir)
    _ensure_dir(tables_dir)

    all_plan_df = pd.read_csv(output_dir / "problem3_all_phlegm_patients_best_plan.csv")
    id_plan_df = pd.read_csv(output_dir / "problem3_id_1_2_3_best_plan.csv")

    all_plan_df["score_drop_ratio"] = (
        (all_plan_df["baseline_score"] - all_plan_df["final_score"]) / all_plan_df["baseline_score"]
    ).round(4)

    plan_summary = (
        all_plan_df.groupby(["intensity", "frequency"], as_index=False)
        .agg(
            patient_count=("sample_id", "count"),
            mean_cost=("total_cost", "mean"),
            mean_drop_ratio=("score_drop_ratio", "mean"),
        )
        .sort_values(["patient_count", "mean_drop_ratio"], ascending=[False, False])
    )
    plan_summary.to_csv(tables_dir / "problem3_plan_summary_table.csv", index=False, encoding="utf-8-sig")

    agegroup_table = (
        all_plan_df.groupby(["age_group", "intensity", "frequency"], as_index=False)
        .agg(
            patient_count=("sample_id", "count"),
            mean_cost=("total_cost", "mean"),
            mean_drop_ratio=("score_drop_ratio", "mean"),
        )
        .sort_values(["age_group", "patient_count"], ascending=[True, False])
    )
    agegroup_table.to_csv(tables_dir / "problem3_agegroup_plan_table.csv", index=False, encoding="utf-8-sig")

    plt.figure(figsize=(7, 4))
    sns.histplot(all_plan_df["total_cost"], bins=20, kde=True)
    plt.title("Problem 3 Cost Distribution")
    plt.xlabel("Total cost (6 months)")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(figures_dir / "problem3_cost_distribution.png", dpi=150)
    plt.close()

    plt.figure(figsize=(7, 4))
    sns.histplot(all_plan_df["score_drop_ratio"], bins=20, kde=True)
    plt.title("Problem 3 Score Drop Ratio Distribution")
    plt.xlabel("Drop ratio")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(figures_dir / "problem3_score_drop_ratio_distribution.png", dpi=150)
    plt.close()

    heat_df = (
        all_plan_df.groupby(["intensity", "frequency"], as_index=False)
        .agg(patient_count=("sample_id", "count"))
        .pivot(index="intensity", columns="frequency", values="patient_count")
        .fillna(0)
    )
    plt.figure(figsize=(10, 4))
    sns.heatmap(heat_df, cmap="YlGnBu", annot=True, fmt=".0f")
    plt.title("Problem 3 Intensity-Frequency Heatmap")
    plt.xlabel("Frequency per week")
    plt.ylabel("Intensity level")
    plt.tight_layout()
    plt.savefig(figures_dir / "problem3_intensity_frequency_heatmap.png", dpi=150)
    plt.close()

    id_plan_df.to_csv(tables_dir / "problem3_id_1_2_3_table.csv", index=False, encoding="utf-8-sig")
    return {
        "id_table": tables_dir / "problem3_id_1_2_3_table.csv",
        "summary_table": tables_dir / "problem3_plan_summary_table.csv",
        "agegroup_table": tables_dir / "problem3_agegroup_plan_table.csv",
        "cost_fig": figures_dir / "problem3_cost_distribution.png",
        "drop_fig": figures_dir / "problem3_score_drop_ratio_distribution.png",
        "heatmap_fig": figures_dir / "problem3_intensity_frequency_heatmap.png",
    }


def build_key_results_markdown(output_dir: Path) -> Path:
    summary_json = json.loads((output_dir / "problem1_top_summary.json").read_text(encoding="utf-8"))
    p1_imp = pd.read_csv(output_dir / "problem1_feature_importance.csv")
    p1_or = pd.read_csv(output_dir / "problem1_constitution_or.csv")

    p2_risk_table = pd.read_csv(output_dir / "tables" / "problem2_risk_level_table.csv")
    p2_rules_table = pd.read_csv(output_dir / "tables" / "problem2_top_rules_table.csv")

    p3_id_table = pd.read_csv(output_dir / "tables" / "problem3_id_1_2_3_table.csv")
    p3_summary = pd.read_csv(output_dir / "tables" / "problem3_plan_summary_table.csv")

    lines = [
        "# MathorCup C题 结果汇总（问题1-3）",
        "",
        "## 1) 问题一：关键指标与体质贡献",
        "",
        f"- Top特征（综合评分）：{', '.join(summary_json['top_features'][:10])}",
        f"- OR贡献Top3体质：{', '.join(summary_json['top_constitution_or'])}",
        f"- SHAP贡献Top3体质：{', '.join(summary_json['top_constitution_shap'])}",
        "",
        "**问题一 Top-10 特征综合评分表**",
        "",
        _df_to_markdown(p1_imp[["feature", "score"]], max_rows=10),
        "",
        "**问题一 体质OR前10表**",
        "",
        _df_to_markdown(p1_or[["constitution", "odds_ratio"]], max_rows=10),
        "",
        "## 2) 问题二：风险分层、可视化与规则",
        "",
        "**风险分层统计表**",
        "",
        _df_to_markdown(p2_risk_table, max_rows=10),
        "",
        "**高风险关联规则 Top-10**",
        "",
        _df_to_markdown(p2_rules_table, max_rows=10),
        "",
        "![Problem2 Risk Counts](figures/problem2_risk_level_counts.png)",
        "",
        "![Problem2 ROC](figures/problem2_roc_curve.png)",
        "",
        "![Problem2 Top Features](figures/problem2_top10_feature_importance.png)",
        "",
        "## 3) 问题三：干预优化、可视化与表格",
        "",
        "**ID=1,2,3 最优方案表**",
        "",
        _df_to_markdown(
            p3_id_table[
                [
                    "sample_id",
                    "baseline_score",
                    "target_score",
                    "intensity",
                    "frequency",
                    "final_score",
                    "total_cost",
                    "meets_target",
                ]
            ],
            max_rows=10,
        ),
        "",
        "**全体痰湿患者方案汇总表（Top-10）**",
        "",
        _df_to_markdown(p3_summary, max_rows=10),
        "",
        "![Problem3 Cost Distribution](figures/problem3_cost_distribution.png)",
        "",
        "![Problem3 Drop Ratio Distribution](figures/problem3_score_drop_ratio_distribution.png)",
        "",
        "![Problem3 Intensity Frequency Heatmap](figures/problem3_intensity_frequency_heatmap.png)",
        "",
    ]

    report_path = output_dir / "problem1_3_key_results.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path

