import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 300

def create_lollipop_chart():
    # 模拟 9 种体质的边际效应数据和贡献占比
    data = {
        '体质': ['气虚质', '平和质', '血瘀质', '湿热质', '阳虚质', '阴虚质', '气郁质', '特禀质', '痰湿质'],
        '边际效应(AME)': [0.28, 0.22, -0.19, -0.14, 0.09, 0.06, -0.05, 0.04, -0.02],
        '贡献占比': ['25%', '20%', '18%', '12%', '8%', '6%', '5%', '4%', '2%']
    }
    df = pd.DataFrame(data)
    
    # 颜色映射：根据正负区分
    colors = ['#D35400' if x > 0 else '#2980B9' for x in df['边际效应(AME)']]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 画棒棒糖图的“棍子”（水平线）
    ax.hlines(y=df['体质'], xmin=0, xmax=df['边际效应(AME)'], color=colors, alpha=0.8, linewidth=3)
    
    # 画棒棒糖图的“糖头”（散点）
    # 使用散点大小反映稍微一点视觉差异或统一大小
    scatter = ax.scatter(df['边际效应(AME)'], df['体质'], s=150, color=colors, zorder=3)
    
    # 添加数据标签
    for i, row in df.iterrows():
        # 根据正负决定文字偏向
        if row['边际效应(AME)'] > 0:
            ha = 'left'
            x_offset = 0.015
        else:
            ha = 'right'
            x_offset = -0.015
            
        ax.text(row['边际效应(AME)'] + x_offset, i, 
                f"{row['边际效应(AME)']}\n({row['贡献占比']})", 
                va='center', ha=ha, fontsize=10, color='#333333', fontweight='bold')
    
    # 中心零轴线
    ax.axvline(x=0, color='gray', linestyle='--', linewidth=1.5, alpha=0.7)
    
    # 图表标题与坐标轴美化
    ax.set_title('图 2.2：九种体质模型化边际效应(AME)与风险贡献占比对比', fontsize=15, pad=20, weight='bold')
    ax.set_xlabel('模型化边际效应 (AME - 正为高风险，负为保护因素)', fontsize=12, weight='bold')
    ax.set_xlim(-0.35, 0.40) # 预留文字空间
    
    # 去掉上下右边框，左边框保留给标签
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_linewidth(1.5)
    ax.spines['bottom'].set_bounds(-0.3, 0.3)
    
    # 优化网格与Y轴标签
    ax.grid(axis='x', linestyle=':', alpha=0.6)
    ax.tick_params(axis='y', length=0, labelsize=12)
    
    # 反转Y轴，使最高贡献排在最上
    plt.gca().invert_yaxis()
    
    plt.tight_layout()
    
    # 保存路径
    save_path = os.path.join(os.path.dirname(__file__), '2.2_九种体质贡献度对比.png')
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    
    print(f"[成功] 棒棒糖图生成于: {save_path}")

if __name__ == '__main__':
    create_lollipop_chart()