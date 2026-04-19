import re

with open(r'C:\Users\Answers\Desktop\mathmathor cup\MathorCup\论文\c_report.tex', 'r', encoding='utf-8') as f:
    content = f.read()

# find Q1, Q2, Q3
start = content.find(r'\section{问题一：关键指标筛选与体质贡献分析}')
end = content.find(r'\section{模型检验与结果讨论}')

new_text = r'''	\section{问题一：体质与生化的双向解耦及核心标志物筛选}
		\subsection{高阶互信息与特征多维降维评估矩阵}
				在传统流行病学与预防医学的定量筛选中，仅依赖单一 Pearson 或 Spearman 秩相关往往因忽视非线性拓扑而错失隐含关联\cite{ref11}。第一问的本质，是要求从带有极强共线性的血常规测试池与主观起居表单（ADL/IADL）中，分离出既能精准刻画“痰湿累积深度”，又能作为高血脂爆发“导火索”的特异性标志物群。为了保证后续的医学独立性，我们强力阻断了总分域的跨层共振重叠：将派生叠加的高层活动量表总分予以冷藏，仅提取基础 ADL 总分与 IADL 总分进行基质探查。主分析候选空间严密锁定在 $9$ 个维度：
			\begin{equation}
				\begin{aligned}
					X=\{&\text{ADL总分、IADL总分、HDL-C、LDL-C、TG、TC},\\
					&\text{空腹血糖、血尿酸、BMI}\}.
				\end{aligned}
			\end{equation}
		对特征集 $X$ 体系内的每一独立因子 $x_j$、中医靶向标签痰湿度 $P$ 及发病标签 $y$，本研究架设起三轨异构的并行评测雷达阵列：

		第一轨，非线性熵约束评估：借助香农信息论中的信息增益（Mutual Information），量测独立变量削减全集不确定度所贡献的纯净信息比特量：
		\begin{equation}
			M_j^{(1)}=I(x_j;P)=\iint p(x_j, P)\log\frac{p(x_j, P)}{p(x_j)p(P)}\,\mathrm{d}x_j\mathrm{d}P, \qquad M_j^{(2)}=I(x_j;y).
		\end{equation}
		第二轨，集成模型袋外重要度（OOB Permutation Importance）\cite{ref2}：分别锻造针对 $P$ 的并联回归森林与针对 $y$ 的随机诊断森林。以特征错乱下基尼（Gini）信息熵和均方残差（MSE）暴增的恶化幅值，锁定核心解释力边界：提取出 $F_j^{(1)}$ 与 $F_j^{(2)}$。
		第三轨，宏观单调性刻画：采用 Spearman 等秩相关 $|R_j|=|\rho_s(x_j,P)|$ 作为基底防线，以防强相关正交项被森林深度节点掩埋。
		
		这五组带有强烈量纲异质性的标量通过一种名为“反域波达序分加权（Borda Count）”的无监督融合框架实现等权合并。令 $\mathrm{rank}_j^{(m)}$ 为第 $j$ 项在第 $m$ 轨观测中的正向名次（越优名次越小），则全局抗扰动波达复合度定义为：
			\begin{equation}
				S_j=\sum_{m=1}^{5}\left(9-\mathrm{rank}_j^{(m)}+1\right).
			\end{equation}
			波达投影法则在极值鲁棒性上超越了粗糙线性组合，它无视了原始计算空间的度量歧义，强力保留了在各个测度维度上名列前茅的公约数指标。结果高度证实，血脂代谢簇（TC, TG, BMI, HDL-C）位列宏观序列阵列榜首。虽然作为功能度量的 ADL 总计弱于脂质化学项，但其在痰湿非线性判别阵列里却长期霸榜前置，充分佐证了受限起居网络对于亚健康中医证型判断起到了不亚于生化穿刺的诊断效能。

		\subsection{体质病理下沉：基于 AME 的概率边际效应剥离}
		如何定量剥离不同体制所贡献的病理动能差，是传统相关度算法的死区。为了精准测谎，本文搭建了一座控制基础人口学背景（年龄、抽烟、饮酒史及性别向量 $W_i$）的偏极大似然逻辑网络（Logistic Regression），将体质积分矩阵 $X$ 作出无量纲正则收敛（$z_{ik}$），并强行摒除直接诱发高血脂的 TC、TG 生化直观因子，严防同源混杂泄露：
		\begin{equation}
			\Pr(Y_i=1)=\left[1+\exp\left(-\beta_0-\sum_{k=1}^{9}\beta_k z_{ik}-\gamma^\top W_i\right)\right]^{-1}.
		\end{equation}
		在此平滑超平面上，引入微观计量经济学核心算法“平均边际效应（Average Marginal Effect, AME）”求其全域平均偏导，彻底破解 Logistic 参数不可直接解释概率增量的死结：
			\begin{equation}
				C_k=\frac{1}{n}\sum_{i=1}^{n}\frac{\partial \Pr(Y_i=1)}{\partial z_{ik}}=\frac{1}{n}\sum_{i=1}^{n}\hat{p}_i(1-\hat{p}_i)\beta_k,\quad G_k=\frac{|C_k|}{\sum_{j=1}^{9}|C_j|}.
			\end{equation}
		演算结果呈现出极度偏离经验直觉却又严密吻合代谢规律的病理图像：气虚质（AME $0.0193$，占比 $31.2\%$）和平和质（AME $0.0142$，占比 $22.9\%$）成为了直接正向推动未病滑向高危的隐形黑手；而相反，湿热质与血瘀质则展现出某种对冲压制属性（AME 呈现 $-0.0092$）。
		\begin{figure}[H]
			\centering
			\includegraphics[width=0.90\textwidth]{Figures/q1_constitution_ame_visual.png}
			\caption{九种体质局部平均边际效应 (AME) 解析全景}
		\end{figure}


	\section{问题二：基于 TreeSHAP 融合的异构诊断--早筛级联网络}
		\subsection{双核并联架构与 SHAP 微观归因图谱}
		诊断面临两种不可同框的极端困境：高特异性带来的精准定损（医院端确诊），以及高灵敏度附带的前置嗅探（基层社区防筛）。若将核心生化指标倾囊投入单一网络，高权重的 TG、TC 必然霸占分裂根节点，导致防筛模型彻底崩塌为简单的生化裁决器。因而，本部分架构被生生切割为两个无交叉子网：
		\begin{enumerate}
			\item \textbf{诊断证实基座：}囊括截尾对数转换后的所有临床测试（包含强穿透的 non-HDL-C 及 TG），目标指向当前静态下的高准确度拟合（AUC 达 $1.000$）。
			\item \textbf{前置弱预警哨兵：}强制抽离脂类直接标记，残存血尿酸、空腹血糖、身体起居和边缘病理质等弱关联点，作为未来滑向深渊的拓扑预测眼（AUC $0.828$）。
		\end{enumerate}

		纯黑盒诊断因阻绝了人类逻辑的透视而面临巨大临床责诘。为此，系统内嵌了诺奖级博弈算法分解理论衍生的解释引擎——TreeSHAP (Shapley Additive exPlanations)\cite{ref10}。针对高维度联合博弈，SHAP 为每一位患者的诊断输出概率赋予了完美的附加闭环加和：
		\begin{equation}
			\hat{p}_i=\phi_0+\sum_{j=1}^{d}\phi_{ij},\qquad \phi_{ij}=\sum_{S\subseteq N\setminus \{j\}}\frac{|S|!(|N|-|S|-1)!}{|N|!}\left[v(S\cup\{j\})-v(S)\right].
		\end{equation}
	\begin{figure}[H]
		\centering
		\includegraphics[width=0.82\textwidth]{Figures/q2_ew_shap_beeswarm.png}
		\caption{弱预警哨兵的 TreeSHAP 全局敏感性蜂群图}
	\end{figure}

		从特征点云蜂聚中可一探究竟：强诊断树完全被 non-HDL-C 主宰；但弱哨兵网络则显露出了真正造就防筛墙的血尿酸（UA）、空腹血糖与气郁质联合。瀑布效应证明，哨兵模型并非聚焦单指标极高突变，而是对微小的代谢与体态偏移做了非线性综合倍率放大，完美实现了亚临床期防未病。

	\subsection{时空瀑布切片：三级预先动态风控体系}
	将多重特征投射入实战落地，需要一层抗噪极高的确定性漏斗。定义核心超标数为 $A$，主导预警得分为 $\hat{p}$，首位体质分与身心受限度为 $P, Q$。本文开出三级筛分断代方程：
	\begin{equation}
		R=
		\begin{cases}
			\text{高危期}, & (A\ge 1 \land P\ge 60)\ \lor\ (A=0 \land P\ge 80 \land Q<40)\ \lor\ \hat{p}\ge 0.80,\\
			\text{中段预警}, & A\ge 1\ \lor\ P\ge 60\ \lor\ (\hat{p}\ge 0.45 \land Q<60),\\
			\text{低敏监测}, & \text{余下全部拓扑覆盖域}.
		\end{cases}
	\end{equation}
		运用关联分析提升度定则（Lift \& Confidence），在划入高危深渊的 $649$ 名群落里，抽取到了如“高血脂异常 + 尿酸飙高 + 肢体活动力丧落”这类极端并发协同效应模式，其先验信度（Conf）飙升至 $0.945$，对冲倍率提升（Lift）跃至 $1.456$。这雄辩地证实，高危的本质不是某一生化的超标，而是“生化防线告破 + 脏器活动塌陷 + 负面行为生活作息”的矩阵风暴共振。
		\begin{figure}[H]
			\centering
			\includegraphics[width=0.96\textwidth]{Figures/q2_risk_sankey.png}
			\caption{三级概率下落的桑基流量漏斗}
		\end{figure}

	\section{问题三：马尔可夫决策深度包络下的个体最优干预}
		\subsection{刚性约束状态图解与最优控制贝尔曼方程}
			将问题三的时间连续域坍缩为一个 $T=6$ 的离散序列马尔可夫演替系统（Markov Decision Process, MDP）\cite{ref12}。患者每经历 1 个月的洗礼流转到初态 $x_m$，可利用外界施加在动作场里的有氧约束算子 $u_m$（限定在生理年龄受限库 $\mathcal{I}(\text{Age},Q)$）与阻力频次 $f_m$。降压效应 $r(u,f)$ 被非连续突变点分割——低于临界每周激荡（$f<5$）时彻底失效锁归零，突破该下限后才展现一阶非线性微小正向导数：
		\begin{equation}
				r(u,f)=
				\begin{cases}
				0, & f<5\\
				0.03(u-1)+0.01(f-5), & f\ge 5.
			\end{cases}
		\end{equation}
		总资本开销则由刚性累加固定中医配比成本 $c_{\text{tcm}}(\cdot)$ 和动能动作损耗 $4f c_u$ 同构：
		\begin{equation}
			C=\sum_{m=1}^{6}\left[c_{\text{tcm}}(s_{m-1})+4f_m\,c_{u_m}\right]\le 2000.
		\end{equation}
		这并非传统线性求解器的辖区（因为非平滑跌落和高度离散嵌套）。借助运筹递归贝尔曼方程（Bellman Equation）和网络非循环无图（DAG）寻路\cite{ref12}，将末端 6 个月后的底线达标界定为吸收态无穷边界：
		\begin{equation}
			V_m(x)=\min_{u\in\mathcal{I},\,f\in[1,10]}
			\left\{
			c_{\text{tcm}}(x)+4f c_u+V_{m+1}\bigl(x(1-r(u,f))\bigr)\right\},\quad 
			V_7(x)=
			\begin{cases}
				0, & x\le 0.9s_0\\
				+\infty, & x>0.9s_0.
			\end{cases}
		\end{equation}
		
	\subsection{核心轨迹求解与降轨演化特性剖析}
		将离散精度推至 $0.001$，我们破解了高并发穷举陷阱，精确回溯出指定的 1，2，3 号患者群的降分抛物线（图 \ref{fig:q3_patient_paths}）。
	\begin{table}[H]
		\centering
		\caption{利用 MDP 后向图解获得的核心样本最快降压策略网络}\label{tab:q3_samples}
		\small
			\begin{tabularx}{0.96\textwidth}{c c c c X X}
				\toprule
				患者组 ID & 启始积分 & 阻击界线 & 行动局限分 & 强力最优干预时点演进拓扑 (月分发) & 总消粍定额 / 收尾留存分\\
				\midrule
				1 & 64.0 & 57.6 & 38 & 前两月暴火压制 $(1,10)$；3月极缓过渡 $(1,6)$；随后滑归静态维持 $(1,1)$ & 678 元 / 57.18 \\
				2 & 58.0 & 52.2 & 40 & 第一月最高限突击 $(2,8)$；次月降档追击 $(1,10)$；4 个月低端养护 $(1,1)$ & 508 元 / 51.79 \\
				3 & 59.0 & 53.1 & 63 & 同 2 号位点，执行初月强压 $(2,8)$；双月降压 $(1,10)$ 与 4月静态修缮 $(1,1)$ & 558 元 / 52.69 \\
				\bottomrule
			\end{tabularx}
		\end{table}

		MDP 给出的非直观完美解答是：“脉冲突刺接驳低耗休眠法”。因为中医基础调度的花费梯队极为严苛，前期集中消耗高昂运动资金拼命将分数砸过低位边界，不仅将断绝了长达 5 个月的惩罚性基础药剂天价支出，更提前将受试者拉回安全健康内稳态（经济效用比实现了完美越迁）。在此范式下生成的个体化医学辅助药方（图 \ref{fig:q3_strategy_heatmap}），为社区工作提供了毋庸置疑的最强理论工具支持极赋实用。
'''

content = content[:start] + new_text + content[end:]

# Add refs 10, 11, 12 to bibliography
bib_replacement = r'''\bibitem{ref9} Honvoh G D, Cho H, Kosorok M R. Model selection for survival individualized treatment rules using the jackknife estimator[J]. BMC medical research methodology, 2022, 22(1): 1-17.
			\bibitem{ref10} Lundberg S M, Erion G, Chen H, et al. From local explanations to global understanding with explainable AI for trees[J]. Nature machine intelligence, 2020, 2(1): 56-67.
			\bibitem{ref11} Esteva A, Robicquet A, Ramsundar B, et al. A guide to deep learning in healthcare[J]. Nature medicine, 2019, 25(1): 24-29.
			\bibitem{ref12} Sutton R S, Barto A G. Reinforcement learning: An introduction[M]. MIT press, 2018.
		\end{thebibliography}'''

content = re.sub(
    r'\\bibitem\{ref9\}.*?\\end\{thebibliography\}',
    bib_replacement,
    content,
    flags=re.IGNORECASE|re.DOTALL
)

with open(r'C:\Users\Answers\Desktop\mathmathor cup\MathorCup\论文\c_report.tex', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done!')
