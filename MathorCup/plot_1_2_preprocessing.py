import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def create_preprocessing_plot():
    # 设置支持中文的字体 (Windows通常自带微软雅黑)
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
    plt.rcParams['axes.unicode_minus'] = False 

    # 1. 模拟生成带有严重右偏态和长尾极端值的大样本数据 (以 TG 甘油三酯为例)
    np.random.seed(42)
    # 对数正态分布模拟主体正常人群
    base_tg = np.random.lognormal(mean=0.5, sigma=0.6, size=980) 
    # 均匀分布模拟部分极端异常高值人群
    outliers = np.random.uniform(5, 15, size=20) 
    raw_tg = np.concatenate([base_tg, outliers])

    df = pd.DataFrame({'TG_Raw': raw_tg})

    # 2. 稳健预处理操作
    # (1) 分位截尾处理 (削弱极端值): 以 1% 和 99% 分位数对数据进行掐尾
    q_low = df['TG_Raw'].quantile(0.01)
    q_high = df['TG_Raw'].quantile(0.99)
    df['TG_Clipped'] = df['TG_Raw'].clip(lower=q_low, upper=q_high)

    # (2) 偏态变量对数变换 log(1+x) (拉回正态)
    df['TG_Processed'] = np.log1p(df['TG_Clipped'])

    # 3. 绘制双子图分布对比 (直方图 + KDE 密度曲线图)
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), facecolor='#FAFAFA')

    # 子图1：左侧原始数据展示
    sns.histplot(df['TG_Raw'], kde=False, ax=axes[0], color='#F28E2B', bins=40, stat='density', alpha=0.6, edgecolor='white')
    sns.kdeplot(df['TG_Raw'], color='#E15759', ax=axes[0], linewidth=2.5, fill=True, alpha=0.1)
    axes[0].set_title('预处理前：原始 TG (甘油三酯) 数据分布\n(呈现显著的右偏态与长尾极端值)', fontsize=15, pad=15, fontweight='bold', color='#333333')
    axes[0].set_xlabel('TG 原始检测浓度', fontsize=13)
    axes[0].set_ylabel('分布密度 (Density)', fontsize=13)
    axes[0].grid(axis='y', linestyle='--', alpha=0.5)
    axes[0].spines['top'].set_visible(False)
    axes[0].spines['right'].set_visible(False)

    # 子图2：右侧预处理后数据展示
    sns.histplot(df['TG_Processed'], kde=False, ax=axes[1], color='#59A14F', bins=30, stat='density', alpha=0.6, edgecolor='white')
    sns.kdeplot(df['TG_Processed'], color='#3B6B35', ax=axes[1], linewidth=2.5, fill=True, alpha=0.1)
    axes[1].set_title('预处理后：1%分位截尾 + $\\log(1+x)$变换\n(长尾极值被有效削弱，使其近似正态分布)', fontsize=15, pad=15, fontweight='bold', color='#333333')
    axes[1].set_xlabel('稳健处理后的 TG 特征值', fontsize=13)
    axes[1].set_ylabel('分布密度 (Density)', fontsize=13)
    axes[1].grid(axis='y', linestyle='--', alpha=0.5)
    axes[1].spines['top'].set_visible(False)
    axes[1].spines['right'].set_visible(False)

    # 整体布局美化与保存
    plt.tight_layout()
    output_path = os.path.join(os.path.dirname(__file__), '1.2_预处理前后对比图.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ 图表已成功生成并保存至: {output_path}")

if __name__ == "__main__":
    create_preprocessing_plot()
