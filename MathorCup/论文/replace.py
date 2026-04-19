import re
with open('c_report.tex', 'r', encoding='utf-8') as f:
    text = f.read()

old1 = r'为便于展示三位样本在六个月内的积分变化轨迹与成本累积趋势，图 \\ref\{fig:q3_patient_paths\} 预留了三位患者的干预执行轨迹图位。需要特别说明的是，该图当前仍沿用队友按“六个月固定同一方案”口径制作的旧版示意，因此仅作为版式占位；正式提交前，应按本文动态规划得到的阶段性最优方案重新绘制并替换。\s*\\begin\{figure\}\[H\]\s*\\centering\s*\\includegraphics\[width=0\.98\\textwidth\]\{Figures/q3_patient_paths_placeholder\.png\}\s*\\caption\{三位样本六个月干预轨迹与成本变化示意（当前为旧版口径占位图，待按动态规划结果更新）\}\\label\{fig:q3_patient_paths\}\s*\\end\{figure\}'

new1 = r'''为直观展示三位高痰湿基线样本在六个月最优干预周期内的积分降轨与成本演化，本文绘制了动态轨迹组合图，如图 \ref{fig:q3_patient_paths} 所示。此干预动态轨迹组合图追踪了三位典型的高危（高痰湿）病患在 6 个月调理期内的得分与累计成本交互变化趋势。曲线部分（左侧 Y 轴）表明各样本痰湿积分平稳下探，均在终点前成功越过红色警戒线（即降低基线分值的 10\% 预定目标）；柱状图部分（右侧 Y 轴）则呈现相应月度的累进干预花费。此外，背景的三色阈值跨越带可视化了这三位病患从中医学的极重度（红色区域）调理成功降级至平稳或轻度（绿色区域）的心路历程，完美实现了临床显著降分与边际经济成本的平衡。
		\begin{figure}[H]
			\centering
			\includegraphics[width=0.98\textwidth]{Figures/4_1_trajectory.png}
			\caption{三位典型病患的动态干预轨迹与成本追踪演化图}\label{fig:q3_patient_paths}
		\end{figure}'''

old2 = r'图 \\ref\{fig:q3_strategy_heatmap\} 给出了一个“患者特征--干预策略”的速查图位，用于后续展示初始痰湿积分区间、活动能力区间与推荐策略之间的对应关系。由于该图当前仍使用旧版固定方案口径下的预估成本标注，因此此处先作为占位保留，待队友按动态规划结果重绘后即可直接替换同名图片文件。\s*\\begin\{figure\}\[H\]\s*\\centering\s*\\includegraphics\[width=0\.82\\textwidth\]\{Figures/q3_strategy_heatmap_placeholder\.png\}\s*\\caption\{患者特征与干预策略速查图（当前为旧版口径占位图，待按动态规划结果更新）\}\\label\{fig:q3_strategy_heatmap\}\s*\\end\{figure\}'

new2 = r'''图 \ref{fig:q3_strategy_heatmap} 补充绘制了“患者特征匹配策略速查图”，将前述三级风险分层与多阶段动态规划理论沉淀为行动矩阵。此图表专为快速落地检索而设计，将三级基线模型计算出的繁复数据转为了“临床直查卡片”。结合患者横轴（初始活动受限分级）与纵轴（基础痰湿等级）截面状态，热图底色标出了对应人群达成 10\% 降线目标的内在门槛难度；而每个自适应大小的信息卡明示了达成该降分所需设定的预估成本预算（卡片尺寸越大说明成本越高），并以文字直接传达模型核算出的最优化方案（包括推荐干预强度及干预频次）。该速查表为一线的体质预警与行为干预开出了便捷科学的“量体裁衣行动处方”。
		\begin{figure}[H]
			\centering
			\includegraphics[width=0.88\textwidth]{Figures/4_2_heatmap.png}
			\caption{患者特征与匹配策略气泡速查热力图}\label{fig:q3_strategy_heatmap}
		\end{figure}'''

text = re.sub(old1, new1.replace('\\', '\\\\'), text)
text = re.sub(old2, new2.replace('\\', '\\\\'), text)

with open('c_report.tex', 'w', encoding='utf-8') as f:
    f.write(text)
print('Replacement applied.')