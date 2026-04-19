from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import font_manager as fm


FONT_CANDIDATES = [
    Path("C:/Windows/Fonts/msyh.ttc"),
    Path("C:/Windows/Fonts/simhei.ttf"),
    Path("C:/Windows/Fonts/simsun.ttc"),
]

NAME_MAP = {
    "Balanced": "平和质",
    "Qi_deficiency": "气虚质",
    "Yang_deficiency": "阳虚质",
    "Yin_deficiency": "阴虚质",
    "Phlegm_dampness": "痰湿质",
    "Damp_heat": "湿热质",
    "Blood_stasis": "血瘀质",
    "Qi_stagnation": "气郁质",
    "Special_diathesis": "特禀质",
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


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    csv_path = root / "赛题" / "outputs" / "problem1" / "问题一_体质边际效应贡献.csv"
    figure_dir = root / "论文" / "Figures"
    figure_dir.mkdir(parents=True, exist_ok=True)
    out_path = figure_dir / "q1_constitution_ame_visual.png"

    df = pd.read_csv(csv_path)
    df["name_cn"] = df["name"].map(NAME_MAP).fillna(df["name"])
    df = df.sort_values("ame", ascending=True).reset_index(drop=True)

    plt.style.use("seaborn-v0_8-whitegrid")
    font_prop = configure_chinese_font()
    fig, ax = plt.subplots(figsize=(11.5, 6.8), constrained_layout=True)

    positive = "#d97706"
    negative = "#2b6cb0"
    neutral = "#6b7280"
    colors = [
        positive if ame > 1e-4 else negative if ame < -1e-4 else neutral
        for ame in df["ame"].tolist()
    ]

    y_positions = list(range(len(df)))
    ax.axvline(0.0, color="#9ca3af", lw=1.6, ls="--", zorder=1)

    for y, ame, color in zip(y_positions, df["ame"], colors):
        ax.hlines(y=y, xmin=0, xmax=ame, color=color, lw=3.2, zorder=2)

    ax.scatter(df["ame"], y_positions, s=250, c=colors, edgecolors="white", linewidths=1.8, zorder=3)

    for y, ame, share in zip(y_positions, df["ame"], df["share"]):
        pct = share * 100
        if ame >= 0:
            x = ame + 0.0008
            ha = "left"
        else:
            x = ame - 0.0008
            ha = "right"
        label = f"{ame:+.4f}\n({pct:.1f}%)"
        ax.text(
            x,
            y,
            label,
            va="center",
            ha=ha,
            fontsize=10.5,
            fontproperties=font_prop,
            color="#374151",
        )

    max_abs = float(max(abs(df["ame"].min()), abs(df["ame"].max())))
    pad = max(0.003, max_abs * 0.22)
    ax.set_xlim(float(df["ame"].min()) - pad, float(df["ame"].max()) + pad)
    ax.set_yticks(y_positions)
    ax.set_yticklabels(df["name_cn"], fontproperties=font_prop, fontsize=13)
    ax.set_xlabel("模型化边际效应 AME（正值提高风险，负值降低风险）", fontsize=13, fontproperties=font_prop)
    ax.set_title("九种体质模型化边际效应（AME）与贡献占比", fontsize=18, fontproperties=font_prop, pad=12)
    ax.grid(axis="x", linestyle="--", alpha=0.25)
    ax.grid(axis="y", visible=False)

    note = "点旁标注为 AME 数值与贡献占比"
    ax.text(
        0.99,
        0.02,
        note,
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=10.5,
        fontproperties=font_prop,
        color="#4b5563",
    )

    fig.savefig(out_path, dpi=260, bbox_inches="tight")
    plt.close(fig)
    print(out_path)


if __name__ == "__main__":
    main()
