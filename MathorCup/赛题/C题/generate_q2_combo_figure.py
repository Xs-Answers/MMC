from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager as fm


LABEL_MAP = {
    "lipid_abnormal": "血脂异常",
    "uric_high": "尿酸偏高",
    "glucose_high": "血糖偏高",
    "bmi_high": "BMI偏高",
    "smoke_yes": "吸烟史",
    "drink_yes": "饮酒史",
    "phlegm_high": "痰湿积分高",
    "activity_low": "低活动量",
}
FONT_CANDIDATES = [
    Path("C:/Windows/Fonts/msyh.ttc"),
    Path("C:/Windows/Fonts/simhei.ttf"),
    Path("C:/Windows/Fonts/simsun.ttc"),
]


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


def format_pattern(label: str) -> str:
    parts = label.split(" + ")
    pretty = [LABEL_MAP.get(part, part.replace("_", " ")) for part in parts]
    return "\n+ ".join(pretty)


def plot_panel(ax, data, title: str, cmap_name: str, font_prop: fm.FontProperties) -> None:
    lifts = data["lift"].to_numpy()
    counts = data["count_high"].to_numpy()
    confs = data["confidence"].to_numpy()
    labels = [format_pattern(label) for label in data["pattern_label"].tolist()]

    cmap = plt.get_cmap(cmap_name)
    vmin = float(lifts.min())
    vmax = float(lifts.max()) if float(lifts.max()) > vmin else vmin + 1e-6
    colors = [cmap(0.35 + 0.55 * (val - vmin) / (vmax - vmin)) for val in lifts]

    bars = ax.barh(labels, counts, color=colors, edgecolor="none")
    ax.set_title(title, fontsize=15, fontproperties=font_prop)
    ax.set_xlabel("覆盖的高风险样本数", fontsize=13, fontproperties=font_prop)
    ax.tick_params(axis="x", labelsize=11)
    ax.tick_params(axis="y", labelsize=11)
    ax.grid(axis="x", linestyle="--", alpha=0.25)
    for tick in ax.get_yticklabels():
        tick.set_fontproperties(font_prop)

    xmax = float(counts.max()) * 1.42
    ax.set_xlim(0, xmax)

    for bar, count, conf, lift in zip(bars, counts, confs, lifts):
        x = bar.get_width()
        y = bar.get_y() + bar.get_height() / 2
        text = f"高风险={int(count)}\n置信度={conf:.3f}\n提升度={lift:.3f}"
        ax.text(
            x + xmax * 0.02,
            y,
            text,
            va="center",
            ha="left",
            fontsize=11,
            fontproperties=font_prop,
            bbox={"boxstyle": "round,pad=0.2", "facecolor": "white", "alpha": 0.8, "edgecolor": "none"},
        )


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    script_path = Path(__file__).resolve().with_name("c_problem_starter.py")
    report_dir = root / "论文"
    figure_dir = report_dir / "Figures"
    figure_dir.mkdir(parents=True, exist_ok=True)

    mod = load_module(script_path)
    workbook = mod.find_default_xlsx(root)
    df = mod.load_dataframe(workbook)
    summary = mod.fit_risk_models(df)

    pairs = summary["combo_pairs"].copy().iloc[::-1]
    triples = summary["combo_triples"].copy().iloc[::-1]

    plt.style.use("seaborn-v0_8-whitegrid")
    font_prop = configure_chinese_font()
    fig, axes = plt.subplots(1, 2, figsize=(16.2, 7.4), constrained_layout=True)

    plot_panel(axes[0], pairs, "高风险二项组合", "OrRd", font_prop)
    plot_panel(axes[1], triples, "高风险三项组合", "Blues", font_prop)

    fig.suptitle("高风险特征组合识别结果", fontsize=18, fontproperties=font_prop)
    out_path = figure_dir / "q2_combo_patterns.png"
    fig.savefig(out_path, dpi=240, bbox_inches="tight")
    print(out_path)


if __name__ == "__main__":
    main()
