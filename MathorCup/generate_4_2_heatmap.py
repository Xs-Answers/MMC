import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

import matplotlib.patches as patches

def generate_heatmap():
    plt.rcParams["font.sans-serif"] = ["SimHei"]
    plt.rcParams["axes.unicode_minus"] = False
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    activity = ["<40 严重受限", "40~60 中度", ">=60 优良"]
    phlegm = ["三级 (极高)", "二级 (中度)", "一级 (轻度)"]
    
    difficulty = np.array([
        [0.9, 0.7, 0.5],
        [0.8, 0.6, 0.4],
        [0.6, 0.4, 0.2]
    ])
    
    strategies = [
        ["强烈(u5)\n频次5", "强干预(u4)\n频次4", "中干预(u3)\n频次4"],
        ["强干预(u4)\n频次5", "中强(u3)\n频次3", "常规(u2)\n频次3"],
        ["中强(u3)\n频次3", "常规(u2)\n频次2", "轻微(u1)\n频次1"]
    ]
    costs = [
        [1800, 1500, 1200],
        [1600, 1200, 900],
        [1200, 900, 500]
    ]
    
    sns.heatmap(difficulty, annot=False, cmap="YlOrRd", cbar_kws={"label": "达标难度指标"}, ax=ax)
    
    for i in range(3):
        for j in range(3):
            # 将气泡换为带有圆角的方形（类似 drawio 中的动态大小卡片）
            ratio = (costs[i][j] - 500) / 1300
            shape_w = 0.6 + ratio * 0.3    # 宽度范围 0.6~0.9
            shape_h = 0.4 + ratio * 0.25   # 高度范围 0.4~0.65
            
            x_corner = j + 0.5 - shape_w/2
            y_corner = i + 0.5 - shape_h/2
            
            rect = patches.FancyBboxPatch(
                (x_corner, y_corner), shape_w, shape_h,
                boxstyle="round,pad=0.02,rounding_size=0.08",
                linewidth=1.2, edgecolor="#6c8ebf", facecolor="#dae8fc", alpha=0.95
            )
            ax.add_patch(rect)
            
            ax.text(j + 0.5, i + 0.45, strategies[i][j], ha="center", va="center", fontsize=11, color="black", fontweight="bold")
            ax.text(j + 0.5, i + 0.62, f"(预估总成本: {costs[i][j]}元)", ha="center", va="center", fontsize=9, color="#444444")

    ax.set_xticks(np.arange(len(activity)) + 0.5)
    ax.set_yticks(np.arange(len(phlegm)) + 0.5)
    ax.set_xticklabels(activity)
    ax.set_yticklabels(phlegm)
    ax.set_xlabel("活动总分评价区间", fontsize=14, labelpad=10)
    ax.set_ylabel("初始痰湿积分区间", fontsize=14, labelpad=10)
    ax.set_title("患者特征匹配干预策略速查热力矩阵", fontsize=16, pad=15)
    
    plt.tight_layout()
    plt.savefig("4_2_患者特征匹配策略速查图.png", dpi=300, bbox_inches="tight")

    print("Heatmap generated.")

if __name__ == "__main__":
    generate_heatmap()