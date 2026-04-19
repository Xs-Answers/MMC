import matplotlib.pyplot as plt
import pandas as pd
from upsetplot import UpSet, from_memberships
import matplotlib
import os

# 设置中文字体，保证图表正常显示中文
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 构造模拟交集数据（针对血脂异常、尿酸偏高、吸烟史/饮酒史、低活动量、痰湿积分高）
memberships = [
    # 单一特征
    ['血脂异常'], ['尿酸偏高'], ['痰湿积分高'], ['低活动量'], ['吸烟史/饮酒史'],
    # 两两交集
    ['血脂异常', '尿酸偏高'], 
    ['血脂异常', '痰湿积分高'], 
    ['痰湿积分高', '低活动量'],
    ['尿酸偏高', '吸烟史/饮酒史'],
    # 三特征交集
    ['痰湿积分高', '血脂异常', '低活动量'],
    ['血脂异常', '尿酸偏高', '痰湿积分高'],
    ['尿酸偏高', '痰湿积分高', '低活动量'],
    # 四特征及以上交集
    ['血脂异常', '尿酸偏高', '吸烟史/饮酒史', '痰湿积分高'],
    ['血脂异常', '尿酸偏高', '低活动量', '痰湿积分高'],
    ['血脂异常', '尿酸偏高', '吸烟史/饮酒史', '低活动量', '痰湿积分高']
]

# 对应的模拟人数数据
data = [
    180, 150, 200, 110, 95,   # 单一
    120, 135, 90, 80,         # 双交集
    145, 115, 70,             # 三交集
    60, 50,                   # 四交集
    40                        # 五交集
]

# 转化为 upsetplot 能识别的数据集
example_data = from_memberships(memberships, data=data)

# 绘图
fig = plt.figure(figsize=(12, 7))
upset = UpSet(example_data, 
              subset_size='count', 
              intersection_plot_elements=4, 
              show_counts=True,
              facecolor='darkblue', 
              other_dots_color='lightgray')

upset.plot(fig=fig)

plt.suptitle('3.1 高风险核心特征组合覆盖规模 (UpSet)', fontsize=16, y=1.05)
output_path = os.path.join(os.path.dirname(__file__), '3.1_高风险核心特征组合.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"图表已生成并保存到: {output_path}")