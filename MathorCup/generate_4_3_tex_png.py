import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import platform
import os

# Config font for Chinese characters
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(11, 13), dpi=300) # Suitable for A4 roughly
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

def add_box(x, y, w, h, text, facecolor='white', edgecolor='#333333', 
            boxstyle='round,pad=0.3,rounding_size=0.5', fontsize=11, fontweight='normal', text_color='black', text_ha='center'):
    fancy_box = mpatches.FancyBboxPatch((x, y), w, h,
                                        boxstyle=boxstyle,
                                        facecolor=facecolor,
                                        edgecolor=edgecolor,
                                        linewidth=1.2,
                                        zorder=2)
    ax.add_patch(fancy_box)
    
    # calculate text pos
    cx = x + w / 2 if text_ha == 'center' else x + 1.5
    cy = y + h / 2
    ax.text(cx, cy, text, ha=text_ha, va='center', fontsize=fontsize, fontweight=fontweight, color=text_color, zorder=3)

def draw_arrow(x1, y1, x2, y2):
    ax.annotate("",
                xy=(x2, y2), xycoords='data',
                xytext=(x1, y1), textcoords='data',
                arrowprops=dict(arrowstyle="->", color="#333333", lw=1.5),
                zorder=1)

def draw_line(x1, y1, x2, y2):
    ax.plot([x1, x2], [y1, y2], color='#333333', lw=1.5, zorder=1)

# 1. Title
ax.text(50, 96, "中年人群高血脂症与痰湿体质综合风险评估流程图", 
        ha='center', va='center', fontsize=19, fontweight='bold', color="#1a1a1a")

# 2. Start
add_box(35, 87, 30, 5, "初筛：中老年评估及干预体检总人群", facecolor='#f5f5f5', fontsize=13, fontweight='bold')

# 3. Diamond
diamond = mpatches.Polygon(xy=[(50, 84), (65, 79), (50, 74), (35, 79)], closed=True, 
                           facecolor='#eef5ff', edgecolor='#333333', lw=1.2, zorder=2)
ax.add_patch(diamond)
ax.text(50, 79, "是否存在较严重的合并病史？\n(如严重冠心病、缺血性脑卒中等)", ha='center', va='center', fontsize=11, fontweight='bold')

draw_arrow(50, 87, 50, 84)

# 4. Branches
# Left Branch (Secondary)
draw_line(35, 79, 25, 79)
draw_arrow(25, 79, 25, 72)
ax.text(30, 80, "是", ha='center', va='bottom', fontsize=13, fontweight='bold', color='#c00000')

add_box(10, 52, 30, 19, "【极高危干预分流】\n\n符合下列任意条件者直接纳入极危预警：\n\n① 近期心肌梗死或重大脑血管病史\n② 极度高胆固醇 (LDL-C ≥4.9 mmol/L)\n③ 满级重度痰湿伴日常活动完全受限\n④ 不可逆的器官靶向病变", 
        facecolor='#fff0f0', text_ha='left', boxstyle='round,pad=0.5,rounding_size=1', fontsize=11)
        
# Right Branch (Primary)
draw_line(65, 79, 75, 79)
draw_arrow(75, 79, 75, 72)
ax.text(70, 80, "否", ha='center', va='bottom', fontsize=13, fontweight='bold', color='#2ca02c')

add_box(55, 64, 40, 8, "不符合上方左侧各项危重症指标者，\n进入常规队列，综合下列表格确立危险等级", facecolor='#f0faef', fontsize=12, fontweight='bold')

# Arrow to matrix
draw_arrow(75, 64, 75, 55)

# Matrix Table (x: 10 to 96, y: 15 to 55)
# Background Box for Matrix Title
add_box(10, 51, 86, 4, "多维特征交叉预警与发病层级评估矩阵", facecolor='#e6f0ff', fontsize=13, fontweight='bold', text_color="#003380")

y_header = 45
h_row = 5.2

# Draw main matrix grid
x_c1 = 10
x_c2 = 23
x_c3 = 39
x_c4 = 58
x_c5 = 77
x_end = 96

# Headers
add_box(x_c1, y_header, x_c3-x_c1, h_row, "核心血脂状态 | 日常活动受限量级", facecolor='#f8f9fa', fontsize=11, fontweight='bold')
add_box(x_c3, y_header, x_c4-x_c3, h_row, "无或轻度痰湿\n(0≤积分<60)", facecolor='#f8f9fa', fontsize=11, fontweight='bold')
add_box(x_c4, y_header, x_c5-x_c4, h_row, "中度痰湿阶段\n(60≤积分<80)", facecolor='#f8f9fa', fontsize=11, fontweight='bold')
add_box(x_c5, y_header, x_end-x_c5, h_row, "重度痰湿预警\n(≥80分)", facecolor='#f8f9fa', fontsize=11, fontweight='bold')

y_curr = y_header

# Data
acts = ["活动能力良好\n(分数≥60)", "轻度活动受限\n(40≤分数<60)", "显著活动受限\n(分数<40)"]
g_col = '#d4edd9' # Lighter green
y_col = '#ffebb3' # Lighter orange
r_col = '#ffd1cf' # Lighter red

def get_cell(val):
    if val == 'G': return g_col, "低危人群 (<5%)", "#1a6b29"
    if val == 'Y': return y_col, "中危界定 (5-9%)", "#996b00"
    if val == 'R': return r_col, "高危突变 (≥10%)", "#9e1511"

matrix_data = [
    ['G', 'G', 'G'],
    ['G', 'G', 'Y'],
    ['Y', 'R', 'R'],
    ['Y', 'Y', 'R'],
    ['Y', 'R', 'R'],
    ['R', 'R', 'R'],
]

for r in range(6):
    y_curr -= h_row
    
    # Row headers Left col 1 (spans 3 rows)
    if r == 0:
        add_box(x_c1, y_curr - 2*h_row, x_c2-x_c1, h_row*3, "未确诊高血脂\n且各项生化指标\n无异常溢出", facecolor='#ffffff')
    elif r == 3:
        add_box(x_c1, y_curr - 2*h_row, x_c2-x_c1, h_row*3, "已确诊高血脂\n或某项靶向指标\n发生显著异常", facecolor='#fcfcfc')
        
    # Row headers Col 2
    add_box(x_c2, y_curr, x_c3-x_c2, h_row, acts[r%3], facecolor='#ffffff', fontsize=10)
    
    # Cells
    c1, t1, t_col1 = get_cell(matrix_data[r][0])
    c2, t2, t_col2 = get_cell(matrix_data[r][1])
    c3, t3, t_col3 = get_cell(matrix_data[r][2])
    
    add_box(x_c3, y_curr, x_c4-x_c3, h_row, t1, facecolor=c1, text_color=t_col1, fontweight='bold')
    add_box(x_c4, y_curr, x_c5-x_c4, h_row, t2, facecolor=c2, text_color=t_col2, fontweight='bold')
    add_box(x_c5, y_curr, x_end-x_c5, h_row, t3, facecolor=c3, text_color=t_col3, fontweight='bold')

# Footnotes
note_text = ("【 理论融合说明 】\n"
             "- 血脂异常识别阻断：遵循赛题核心指标与预警诊断要求，任意单项生化边界极端异常，无条件降级入下半层警戒组。\n"
             "- 特征耦合非线性预设：矩阵划界高度契合前述随机森林(Random Forest)的 Gini 权重排序及互信息(MI)非线性评估结论。\n"
             "  例如：“重期痰湿伴严重活动障碍”即使处于血脂正常组，仍表现出高位(红色)共线性致病倾向，实现无缝隐匿预警。\n"
             "- 与运筹模型耦合机制：红黄绿危阶直通下文最优化干预模型，作为划定干预强度、限制月度成本(≤2000元)的核心参量。")

# Use a text bound box
fancy_box = mpatches.FancyBboxPatch((10, 2), 86, 9,
                                    boxstyle='round,pad=0.5,rounding_size=0.5',
                                    facecolor='#fcfcfc',
                                    edgecolor='#cccccc',
                                    linewidth=1,
                                    zorder=1)
ax.add_patch(fancy_box)
ax.text(12, 6.5, note_text, ha='left', va='center', fontsize=10.5, linespacing=1.8, color="#444444")

plt.savefig('5_1_高质预警决策流程图_Tex专用.png', bbox_inches='tight', dpi=400)
print("PNG generated successfully.")