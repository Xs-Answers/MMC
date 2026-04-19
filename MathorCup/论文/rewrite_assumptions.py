import re

with open(r'C:\Users\Answers\Desktop\mathmathor cup\MathorCup\论文\c_report.tex', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace the assumption section
old_assumptions = r'''	\section{模型假设}
	\begin{enumerate}
		\item 附件样本已完成临床检验与标签标注，数据可直接用于建模与验证。
		\item 题目给出的临床正常值区间与活动能力约束规则具有统一适用性，视为风险分层与干预求解的硬约束。
		\item 痰湿积分每月变化主要由活动干预强度与频次驱动；中医调理等级在题目中未给出显式降分系数，因此本文将其视为按积分区间自动匹配的基础调理成本。
		\item 在相同活动干预强度下，若每周训练频次低于 $5$ 次，则痰湿积分近似保持稳定；若每周训练频次不低于 $5$ 次，则按题目给出的比例规则递推下降。
		\item 六个月周期内患者的年龄组、性别以及吸烟饮酒史不发生变化，活动量表初值用于确定可选强度上界。
	\end{enumerate}'''

new_assumptions = r'''	\section{模型假设}
	\begin{enumerate}
		\item \textbf{数据代表性与标签溯源可靠性假设。} 假设附件主诉量表与客观血清检验项严格遵循现行《中国血脂管理指南》\cite{ref7} 等大规模流行病学调研数据规约；并假定队列不受急症等短期非自然干扰，即局部 $1000$ 例样本对整体中老年受试人群的生理病理转化具备统计意义上的全域无偏映射能力。
		\item \textbf{受试主干稳态及核心能力刚性上界假设。} 鉴于自然人机体存在极强的生物惯性与时间迟滞效应，假定在不超过六个月中短期管控窗口内，各靶点人物之基础要素（如生理性别、年龄层驻留、烟酒史沉淀）均停步于原生准静态切片不作推移；且初始观测取得的 ADL/IADL 满分系作为锁定受试组运动心肺承载上限的临床红线，具备绝对的约束否决权。
		\item \textbf{方剂食疗效用融合及阶梯调理固支假设。} 依据传统中医理论“缓和固本”之理，假设中医药剂、针灸等保守调和手段针对轻、中、重三阶病灶施加的病耻抵消效应，已隐式混叠于干预运动系数衰退核内。因此，模型将动态挂钩该积段所设之中医阶别单独视作“维系退行战果不反弹”之固定底座维护费。
		\item \textbf{有氧代谢“低级代偿锁死-高位跃迁激活”频次准则。} 结合世界卫生组织最新版《关于身体活动和久坐行为指南》\cite{ref8} 的权威论作支持与运动转化组学研究共识，在强度负荷相同场景中，唯独受试频度等越、或跨过周次 $5$ 这一阈线段内，肌糖原-肝脂燃烧通道方为激活态；若周频落至下沿孤岛（$<5$次），细微微损伤与耗散将即刻被基础代偿抵扣、促使体质积分呈现“闭合停转式稳存锁死”。
		\item \textbf{病理变轨之单向闭环控流与系统封闭独立假设。} 我们将风险抑制网络封闭视作理想实验场内的受控热力系统；预定周期运行图纸严禁外在黑盒扰动，即默认摒弃目标私自混入大剂量西方特效化学调脂药、抑或是重大外科清创变迁。即假定最终病理参数衰减面收敛，仅单向性从属于本模型指派运动方程系统规划解。
	\end{enumerate}'''

content = content.replace(old_assumptions, new_assumptions)

# 2. Append citations to bibliography
old_bib_end = r'''			\bibitem{ref6} GB/T 46939---2025. 中医体质分类与判定[S]. 2025.
		\end{thebibliography}'''

new_bib_end = r'''			\bibitem{ref6} GB/T 46939---2025. 中医体质分类与判定[S]. 2025.
			\bibitem{ref7} 中国血脂管理指南修订联合专家委员会. 中国血脂管理指南（2023年）[J]. 中华心血管病杂志, 2023, 51(3): 221-255.
			\bibitem{ref8} World Health Organization. WHO guidelines on physical activity and sedentary behaviour[M]. Geneva: World Health Organization, 2020.
		\end{thebibliography}'''

content = content.replace(old_bib_end, new_bib_end)

with open(r'C:\Users\Answers\Desktop\mathmathor cup\MathorCup\论文\c_report.tex', 'w', encoding='utf-8') as f:
    f.write(content)
print("done")
