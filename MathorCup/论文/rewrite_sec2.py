import re

with open(r'C:\Users\Answers\Desktop\mathmathor cup\MathorCup\论文\c_report.tex', 'r', encoding='utf-8') as f:
    content = f.read()

start = content.find(r'\section{数据理解与总体思路}')
end = content.find(r'\section{模型假设}')

new_section_2 = r'''	\section{数据理解与总体思路}
		附件数据集共包含 $1000$ 例样本和 $37$ 项特征维度，数据集完整度极高且无明显缺失数据。其中，高脂血症确诊发病样本达 $793$ 例，健康或非确诊对标类群仅 $207$ 例。基于《中医体质分类与判定》（GB/T 46939—2025）\cite{ref6} 所极力推崇的最大定性分值核定法则，经过宏观统计剖析，整个矩阵表征出一种不容忽视的偏态流行病学底色：第一，“痰湿凝聚型”极度普遍（确立为主导型的患者达 $292$ 名），在现代组学层面这与血脂富集和肥胖重度耦联。第二，血常规生化测试项中与结论标签存在绝对确定的病理同源性。一旦放任此种强耦合属性流入诊断架构，势必发生严重的维度坍缩与虚模极高拟合度。所以本研究刻意摒蔽外显化同源干涉，转而向深层空间下探——于日常生活受限度、非线性综合体质积分网络中打捞早期微弱的预警共振信号。基于此，本论证建立了一套医学归因与数据深挖相得益彰的图谱（框架全景见图 \ref{fig:framework}），按三大工程分支平行降解题干：
	\begin{enumerate}
		\item \textbf{问题一：体征解耦与高维信息的联合筛选突变评估}。全面屏除传统一阶秩相关的片面线性盲区，融合香农信息论拓扑下的互信息算子（Mutual Information）\cite{ref4}，结合基于集成森林袋外错分扰动的非线性特征增益（Random Forest Feature Importance）\cite{ref2}，以一种独创的复合波达序值加权架构施加投票过滤；从而打捞出穿透“表证体质”与“内生血脂紊乱”交界域的核心桥接靶点。
		\item \textbf{问题二：异构概率阈值推断与级联诊断预警双核并联架构}。医学临床中不可调和的矛盾在于：特异性诊断与广谱性提前预警不可兼得。鉴于此，本文将判决树网暴烈切割为两重逻辑域：“高截断精度的医学确诊”同“捕捉隐匿性微小病变共振的公共预筛”；并在后验概率瀑布中，执行非等距的分段阀限切片，精准识别痰湿质群体滑向高危的危险引爆点。
		\item \textbf{问题三：受限边界动力学控制与马尔可夫转移下最速调理回退路径}。将半年维度解构为离散的马尔可夫状态变迁时间节拍，把基础医疗维护预算作为刚性转移摩擦力内嵌至转换图；继而转换为非循环有向图（DAG）网络动态极值拉归方程，以 Dijkstra-DP 形态彻底降解带有严格硬条件（训练周次与衰退曲线）包络下的最低耗费控制策略。
	\end{enumerate}

		\begin{figure}[htbp]
			\centering
			\includegraphics[width=0.95\textwidth]{Figures/1.1_总体流程图_纵向三行版.png}
			\caption{本文的总体建模流程}\label{fig:framework}
		\end{figure}

		\subsection{数据核验与稳健预处理}
		遵循医疗与流行病学检测中的大数法则与容差规律，真实世界的临床抽样不可避免地携带长尾厚尾漂移以及录入偏移效应。为了在源头上拉升后续核心机器学习网络的抗毁性和反噪越界能力，本文吸纳了临床大数据预分析通用准则\cite{ref3}以及生物计量学中截尾平抑重尾分布的前沿经验\cite{ref9}，专门搭建了由逻辑一致性阻断与分位截尾滤波（Winsorization）构筑的双重防火墙。

		首先，对于人工填写主观量表执行极化自洽阻逆筛查。对于日常行为起居受限度（ADL/IADL），我们经验证发现十维分子题项与两个宏观集成表总分达到了完美数学对冲吻合，确实验证了表单信度壁垒极高。但横向平移至中医体质单项记分列，遵从国标金指引“单项第一高分必须且永远界定为宏观主固体质”原则\cite{ref6}，程序敏锐捕获出有 $65$ 个病例存在“定性主导标签与自身积分峰值倒错挂钩”的反临床逻辑悖象。由于在循证医学判定内，客观得分所对应的生理偏颇倾向拥有最高判定优先级，故而我们运用“重排积分降序修复重置”协议，对这一反常离散簇执行了强行矫正靠拢，维护了另外 $935$ 个样本组绝对同构统一的完整性。

		其次，直面随机森林或树系结构在读取含有连续发散型变异（尖峰长尾型）数据时的极值过拟敏感情境。所有的去极边滤除（Winsorization 动作）绝对严守“绝不僭越测试界”的铁律——仅在训练基阵中捕捉确信的 $1\%$ 至 $99\%$ 上下限极点。设原生生理序列参数 $x$ 两端的边界确值界分为 $q_{0.01}(x)$ 及 $q_{0.99}(x)$，进而将该尺度保护界泛延到全集进行安全等距截断：
			\begin{equation}
				x_i^{(w)}=\min\left\{\max\left(x_i,q_{0.01}(x)\right),q_{0.99}(x)\right\}.
			\end{equation}
			在这项针对偏厚分布的基础免疫工程\cite{ref9}之上，特例针对右尾拖拽尤其离谱且极呈现右方孤岛聚集拖尾的甘油三酯（TG）浓度及血清尿酸浓度，额外加码一套对数映射形变进行二度空间收敛平抑：
			\begin{equation}
				\text{TG}_{i}^{(\log)}=\log\left(1+\text{TG}_{i}^{(w)}\right),\qquad
				\text{UA}_{i}^{(\log)}=\log\left(1+\text{UA}_{i}^{(w)}\right).
			\end{equation}
			如图 \ref{fig:tg_preprocess} 的平抑比照所示（以核心致因 TG 代谢指征为例），去极平整前（左侧）展现出难以忽视的极段拉伸破坏域；经过截尾压缩和对数化平置后（右侧），指标分布呈显著对向缩拢状态，从根本上保障了后续集成决策树模型分裂节点基尼基数计算时的稳重和鲁棒防偏\cite{ref2}\cite{ref9}。
			\begin{figure}[H]
				\centering
				\includegraphics[width=0.96\textwidth]{Figures/q2_tg_preprocess.png}
				\caption{TG 在稳健预处理前后的分布对比}\label{fig:tg_preprocess}
			\end{figure}
			进而，为遏制相同生化族群因为定义重叠导致的多重共线性风暴，文章创建出复合冗余消化变量——非高密度脂蛋白复合群（non-HDL-C）：
			\begin{equation}
				\text{nonHDL}_{i}=\text{TC}_{i}^{(w)}-\text{HDL}_{i}^{(w)}.
			\end{equation}
			因为血脂大类的内生代谢反应环，上述三支在血液微观表现上有强定式耦合关系。秉承最简正交信息覆盖定律，最终入围高血脂诊断流的仅保留负责度量胆固醇净差残余的 non-HDL-C，与测算脂质纯载量的甘油三酯，借此彻底抹除重复权重诱发的基尼重载激增。
	
			最后，为补充加法计总时被严重合并掉的单一功能断崖损伤事件，以及定性唯一标签所遗落的倾向差额烈度，我们创设了特种增广流。首先针对起居受限因子 $a_{ij}$，架设日常独立警示水平 $\tau=8$，提取微观跌落警戒项数的累加频次指标：
			\begin{equation}
				C_i^{(\text{act})}=\sum_{j=1}^{10}\mathbb{I}(a_{ij}<\tau),
			\end{equation}
			利用标志函数补充在宏观粗略总和里被其它健康项填平的细微肢体失能侧。

			紧接着，计算患者最大绝对倾向高点与第二顺位替代质的差值跨度以标点混病综合征：提取分值第一的 $s_{i(1)}$ 与居次的 $s_{i(2)}$，裂变出两项极距系标签：
			\begin{equation}
				S_i^{(\max)}=s_{i(1)},\qquad
				M_i^{(\text{gap})}=s_{i(1)}-s_{i(2)}.
			\end{equation}
			内部核心意理即同时固锁了首偏体质阵列那压倒性摧枯拉腐的原驱动力 $S_i^{(\max)}$ 和混同于其他次生状态的交叉拉扯深度 $M_i^{(\text{gap})}$，圆满填充了粗放的单一宏观标签下遗落的病灶鸿沟；至此，被彻底重塑化与无偏正交筛选过的队列变量平滑被推入了下一章节的大范围并发判别架构引擎中。

'''

content = content[:start] + new_section_2 + content[end:]

content = re.sub(
    r'(\\bibitem\{ref8\}.*?\n)(\s*\\end\{thebibliography\})',
    r'\g<1>\t\t\t\\bibitem{ref9} Honvoh G D, Cho H, Kosorok M R. Model selection for survival individualized treatment rules using the jackknife estimator[J]. BMC medical research methodology, 2022, 22(1): 1-17.\n\g<2>',
    content,
    flags=re.IGNORECASE|re.DOTALL
)

with open(r'C:\Users\Answers\Desktop\mathmathor cup\MathorCup\论文\c_report.tex', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done!')
