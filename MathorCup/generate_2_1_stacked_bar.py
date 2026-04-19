import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# 设置中文字体 (Windows 默认黑体: SimHei)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 300

def create_stacked_bar():
    # 模拟数据：各位维度的重要度得分 (Score_k,j)
    features = ['HDL-C', '血尿酸', 'TC', '活动受限总分', 'BMI', 'TG']
    
    # 构建数据字典 (五种评价视角)
    data = {
        'Spearman 相关系数': [0.06, 0.08, 0.12, 0.15, 0.18, 0.20],
        'MI-回归 (互信息)':   [0.07, 0.09, 0.11, 0.13, 0.16, 0.17],
        'MI-分类 (互信息)':   [0.05, 0.07, 0.10, 0.14, 0.14, 0.15],
        'RF-回归重要度':     [0.10, 0.12, 0.15, 0.16, 0.15, 0.22],
        'RF-分类重要度':     [0.08, 0.09, 0.13, 0.15, 0.18, 0.16]
    }
    
    df = pd.DataFrame(data, index=features)
    
    # 颜色配置 (高级配色)
    colors = ['#4B74B1', '#E18942', '#A1A0A0', '#F3C144', '#5E99C9']
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 累计起点 (bottom)
    left = np.zeros(len(df))
    
    for i, col in enumerate(df.columns):
        ax.barh(df.index, df[col], left=left, color=colors[i], label=col, height=0.6, edgecolor='white', linewidth=0.5)
        left += df[col]
        
    # 添加数据标签和美化
    for i, (idx, total) in enumerate(zip(df.index, left)):
        # 凸显排名靠前的变量总分 (红色+加粗)
        color, weight = ('#C00000', 'bold') if total > 0.7 else ('#333333', 'normal')
        ax.text(total + 0.01, i, f'{total:.2f}', va='center', ha='left', color=color, weight=weight, fontsize=11)
        
    # 轴和网格美化
    ax.set_xlabel('综合得分 $S_j$', fontsize=12, weight='bold')
    ax.set_title('图 2.1：候选指标多维度特征重要度展示与综合得分 ($S_j$) 分布', fontsize=14, weight='bold', pad=15)
    
    # 去除多余的边框
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_alpha(0.5)
    ax.spines['left'].set_alpha(0.5)
    
    # 添加背景垂直网格线
    ax.xaxis.grid(True, linestyle='--', alpha=0.6, color='grey')
    ax.set_axisbelow(True) # 网格置于柱体下方
    
    # 图例设置 (放置在底部或图的外侧)
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=3, frameon=False, fontsize=10)
    
    # 调整边距以适应图例
    plt.tight_layout()
    
    # 动态保存路径
    save_path = os.path.join(os.path.dirname(__file__), '2.1_多维度指标重要度展示.png')
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    
    print(f"[成功] 图表已生成并保存至: {save_path}")

if __name__ == '__main__':
    create_stacked_bar()