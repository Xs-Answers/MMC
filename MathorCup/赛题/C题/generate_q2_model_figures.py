from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib import text as mtext
import numpy as np
import shap
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import auc, roc_curve
from sklearn.model_selection import train_test_split


FONT_CANDIDATES = [
    Path("C:/Windows/Fonts/msyh.ttc"),
    Path("C:/Windows/Fonts/simhei.ttf"),
    Path("C:/Windows/Fonts/simsun.ttc"),
]

FEATURE_LABELS = {
    "balanced_score": "平和质积分",
    "qi_deficiency_score": "气虚质积分",
    "yang_deficiency_score": "阳虚质积分",
    "yin_deficiency_score": "阴虚质积分",
    "phlegm_score": "痰湿质积分",
    "damp_heat_score": "湿热质积分",
    "non_hdl": "non-HDL-C",
    "tg_log1p": "log(1+TG)",
    "uric_acid_log1p": "log(1+血尿酸)",
    "ldl_w": "截尾后的 LDL-C",
    "glucose_w": "截尾后的空腹血糖",
    "bmi_w": "截尾后的 BMI",
    "blood_stasis_score": "血瘀质积分",
    "yin_deficiency_score": "阴虚质积分",
    "qi_stagnation_score": "气郁质积分",
    "special_diathesis_score": "特禀质积分",
    "constitution_top_score": "最大体质积分",
    "constitution_margin": "体质优势差值",
    "adl_total": "ADL总分",
    "iadl_total": "IADL总分",
    "activity_limited_count": "活动受限计数",
    "bmi_w": "截尾后的 BMI",
    "age_group": "年龄组",
    "sex": "性别",
    "smoke": "吸烟史",
    "drink": "饮酒史",
}

TEXT_REPLACEMENTS = {
    "Feature value": "特征取值",
    "Low": "低",
    "High": "高",
    "SHAP value (impact on model output)": "SHAP 值（对正类概率的影响）",
    "Model output value": "模型输出概率",
    "base value": "基准概率",
    "higher": "更高",
    "lower": "更低",
}


def configure_chinese_font() -> fm.FontProperties:
    for font_path in FONT_CANDIDATES:
        if font_path.exists():
            fm.fontManager.addfont(str(font_path))
            font_prop = fm.FontProperties(fname=str(font_path))
            plt.rcParams["font.family"] = [font_prop.get_name()]
            plt.rcParams["axes.unicode_minus"] = False
            return font_prop
    raise FileNotFoundError("Could not find a usable Chinese font in C:/Windows/Fonts.")


def load_module(script_path: Path):
    spec = importlib.util.spec_from_file_location("c_problem_starter", script_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def feature_label(name: str) -> str:
    return FEATURE_LABELS.get(name, name.replace("_score", "积分").replace("_", " "))


def translate_figure_text(fig, font_prop: fm.FontProperties) -> None:
    for text_obj in fig.findobj(mtext.Text):
        current = text_obj.get_text()
        if current in TEXT_REPLACEMENTS:
            text_obj.set_text(TEXT_REPLACEMENTS[current])
        text_obj.set_fontproperties(font_prop)


def to_positive_class_explanation(
    shap_output: shap.Explanation, feature_frame
) -> shap.Explanation:
    values = shap_output.values
    base_values = shap_output.base_values
    if values.ndim == 3:
        values = values[:, :, 1]
        base_values = base_values[:, 1]
    return shap.Explanation(
        values=values,
        base_values=base_values,
        data=feature_frame.to_numpy(),
        feature_names=[feature_label(name) for name in feature_frame.columns.tolist()],
    )


def make_shap_beeswarm_figure(
    explanation: shap.Explanation,
    title: str,
    out_path: Path,
    font_prop: fm.FontProperties,
    max_display: int = 10,
) -> None:
    plt.style.use("default")
    fig = plt.figure(figsize=(10.2, 7.2))
    shap.plots.beeswarm(explanation, max_display=max_display, show=False)
    ax = plt.gca()
    ax.set_title(title, fontsize=18, fontproperties=font_prop, pad=12)
    ax.set_xlabel("SHAP 值（对高血脂正类概率的影响）", fontsize=14, fontproperties=font_prop)
    ax.tick_params(axis="both", labelsize=12)
    for tick in ax.get_xticklabels() + ax.get_yticklabels():
        tick.set_fontproperties(font_prop)
    translate_figure_text(fig, font_prop)
    fig.savefig(out_path, dpi=240, bbox_inches="tight")
    plt.close(fig)


def make_shap_waterfall_figure(
    explanation_row: shap.Explanation,
    title: str,
    out_path: Path,
    font_prop: fm.FontProperties,
    max_display: int = 10,
) -> None:
    plt.style.use("default")
    fig = plt.figure(figsize=(10.8, 7.0))
    shap.plots.waterfall(explanation_row, max_display=max_display, show=False)
    ax = plt.gca()
    ax.set_title(title, fontsize=18, fontproperties=font_prop, pad=12)
    ax.tick_params(axis="both", labelsize=12)
    for tick in ax.get_xticklabels() + ax.get_yticklabels():
        tick.set_fontproperties(font_prop)
    translate_figure_text(fig, font_prop)
    fig.savefig(out_path, dpi=240, bbox_inches="tight")
    plt.close(fig)


def shap_top_features(explanation: shap.Explanation, top_n: int = 5):
    mean_abs = np.abs(explanation.values).mean(axis=0)
    order = np.argsort(mean_abs)[::-1][:top_n]
    return [(explanation.feature_names[idx], float(mean_abs[idx])) for idx in order]


def representative_ew_case(test_df, probabilities) -> tuple[int, str]:
    candidate = test_df.copy()
    candidate["ew_prob"] = probabilities
    candidate["lipid_abnormal_count"] = candidate.apply(
        lambda row: int(
            (row["tc"] > 6.2)
            + (row["tg"] > 1.7)
            + (row["ldl"] > 3.1)
            + (row["hdl"] < 1.04)
        ),
        axis=1,
    )
    without_direct_lipid = candidate[candidate["lipid_abnormal_count"] == 0]
    if not without_direct_lipid.empty:
        idx = int(without_direct_lipid["ew_prob"].idxmax())
        return idx, "无直接血脂异常且早预警概率最高的测试样本"
    idx = int(candidate["ew_prob"].idxmax())
    return idx, "早预警概率最高的测试样本"


def local_shap_summary(explanation_row: shap.Explanation, top_n: int = 5):
    values = np.asarray(explanation_row.values)
    order = np.argsort(np.abs(values))[::-1][:top_n]
    rows = []
    for idx in order:
        rows.append(
            (
                explanation_row.feature_names[idx],
                float(values[idx]),
                float(explanation_row.data[idx]),
            )
        )
    return rows


def make_roc_figure(
    fpr_diag,
    tpr_diag,
    auc_diag: float,
    fpr_ew,
    tpr_ew,
    auc_ew: float,
    out_path: Path,
    font_prop: fm.FontProperties,
) -> None:
    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(8.6, 6.6), constrained_layout=True)
    ax.plot(fpr_diag, tpr_diag, lw=3.0, color="#c94f3d", label=f"诊断型模型 AUC = {auc_diag:.4f}")
    ax.plot(fpr_ew, tpr_ew, lw=3.0, color="#2a6f97", label=f"早预警模型 AUC = {auc_ew:.4f}")
    ax.plot([0, 1], [0, 1], "--", color="0.65", lw=1.2)
    ax.set_title("两类风险模型的 ROC 曲线", fontsize=18, fontproperties=font_prop)
    ax.set_xlabel("假阳性率", fontsize=14, fontproperties=font_prop)
    ax.set_ylabel("真阳性率", fontsize=14, fontproperties=font_prop)
    ax.tick_params(axis="both", labelsize=12)
    legend = ax.legend(frameon=True, fontsize=12, loc="lower right", prop=font_prop)
    for text in legend.get_texts():
        text.set_fontproperties(font_prop)
    fig.savefig(out_path, dpi=240, bbox_inches="tight")
    plt.close(fig)


def make_importance_figure(
    data,
    title: str,
    color: str,
    out_path: Path,
    font_prop: fm.FontProperties,
) -> None:
    labels = [feature_label(name) for name in data["name"].tolist()]
    values = data["importance"].tolist()

    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(9.4, 6.8), constrained_layout=True)
    ax.barh(labels, values, color=color, edgecolor="none")
    ax.set_title(title, fontsize=18, fontproperties=font_prop)
    ax.set_xlabel("特征重要度", fontsize=14, fontproperties=font_prop)
    ax.tick_params(axis="x", labelsize=12)
    ax.tick_params(axis="y", labelsize=13)
    for tick in ax.get_yticklabels():
        tick.set_fontproperties(font_prop)
    fig.savefig(out_path, dpi=240, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    script_path = Path(__file__).resolve().with_name("c_problem_starter.py")
    report_dir = root / "论文"
    figure_dir = report_dir / "Figures"
    figure_dir.mkdir(parents=True, exist_ok=True)

    font_prop = configure_chinese_font()
    mod = load_module(script_path)
    workbook = mod.find_default_xlsx(root)
    df = mod.load_dataframe(workbook)

    y = df["label"].astype(int)
    train_df, test_df, y_train, y_test = train_test_split(
        df, y, test_size=0.25, stratify=y, random_state=42
    )
    preprocessor = mod.fit_model_preprocessor(train_df)

    x_diag_train, _ = mod.build_feature_matrix(train_df, preprocessor)
    x_diag_test, _ = mod.build_feature_matrix(test_df, preprocessor)
    diag_model = RandomForestClassifier(n_estimators=500, min_samples_leaf=5, random_state=42)
    diag_model.fit(x_diag_train, y_train)
    p_diag = diag_model.predict_proba(x_diag_test)[:, 1]
    fpr_diag, tpr_diag, _ = roc_curve(y_test, p_diag)
    auc_diag = auc(fpr_diag, tpr_diag)

    x_ew_train, _ = mod.build_early_warning_matrix(train_df, preprocessor)
    x_ew_test, _ = mod.build_early_warning_matrix(test_df, preprocessor)
    ew_model = RandomForestClassifier(n_estimators=500, min_samples_leaf=5, random_state=42)
    ew_model.fit(x_ew_train, y_train)
    p_ew = ew_model.predict_proba(x_ew_test)[:, 1]
    fpr_ew, tpr_ew, _ = roc_curve(y_test, p_ew)
    auc_ew = auc(fpr_ew, tpr_ew)

    diag_explainer = shap.Explainer(diag_model, x_diag_train)
    ew_explainer = shap.Explainer(ew_model, x_ew_train)
    diag_shap = to_positive_class_explanation(
        diag_explainer(x_diag_test, silent=True), x_diag_test
    )
    ew_shap = to_positive_class_explanation(ew_explainer(x_ew_test, silent=True), x_ew_test)

    summary = mod.fit_risk_models(df)
    diag_imp = summary["diagnostic_importance"].head(5).iloc[::-1]
    ew_imp = summary["ew_importance"].head(5).iloc[::-1]

    make_roc_figure(
        fpr_diag,
        tpr_diag,
        auc_diag,
        fpr_ew,
        tpr_ew,
        auc_ew,
        figure_dir / "q2_roc_curve.png",
        font_prop,
    )
    make_importance_figure(
        diag_imp,
        "诊断型模型前五重要特征",
        "#c94f3d",
        figure_dir / "q2_diag_importance.png",
        font_prop,
    )
    make_importance_figure(
        ew_imp,
        "早预警模型前五重要特征",
        "#2a6f97",
        figure_dir / "q2_ew_importance.png",
        font_prop,
    )
    make_shap_beeswarm_figure(
        diag_shap,
        "诊断型随机森林的 SHAP 全局解释",
        figure_dir / "q2_diag_shap_beeswarm.png",
        font_prop,
    )
    make_shap_beeswarm_figure(
        ew_shap,
        "早预警随机森林的 SHAP 全局解释",
        figure_dir / "q2_ew_shap_beeswarm.png",
        font_prop,
    )

    ref_idx, ref_desc = representative_ew_case(test_df, p_ew)
    ref_pos = test_df.index.get_loc(ref_idx)
    make_shap_waterfall_figure(
        ew_shap[ref_pos],
        "代表性高风险样本的早预警 SHAP 分解",
        figure_dir / "q2_ew_shap_waterfall.png",
        font_prop,
    )

    print(figure_dir / "q2_roc_curve.png")
    print(figure_dir / "q2_diag_importance.png")
    print(figure_dir / "q2_ew_importance.png")
    print(figure_dir / "q2_diag_shap_beeswarm.png")
    print(figure_dir / "q2_ew_shap_beeswarm.png")
    print(figure_dir / "q2_ew_shap_waterfall.png")
    print("DIAG_SHAP_TOP =", shap_top_features(diag_shap))
    print("EW_SHAP_TOP =", shap_top_features(ew_shap))
    print(
        "EW_REF =",
        {
            "sample_id": int(test_df.loc[ref_idx, "sample_id"]),
            "label": int(test_df.loc[ref_idx, "label"]),
            "ew_prob": float(p_ew[ref_pos]),
            "selection": ref_desc,
            "top_contrib": local_shap_summary(ew_shap[ref_pos]),
        },
    )


if __name__ == "__main__":
    main()
