# MathorCup C 题详细总结报告（中西医融合建模）

> 项目：中老年人群高血脂症风险预警及干预方案优化  
> 数据来源：`mathmathor-cup-c/附件1：样例数据.xlsx`（经清洗后输出至 `outputs/step1_cleaned_dataset.csv`）  
> 报告时间：2026-04-17

---

## 1. 研究背景与问题定义

### 1.1 背景意义
高血脂症是中老年心脑血管事件的重要上游风险因素。传统西医筛查更多依赖血脂生化指标（TC、TG、LDL-C、HDL-C），而中医体质学强调“痰湿内蕴”与代谢异常之间的内在关联。本课题采用“中医体质 + 活动能力 + 代谢指标 + 行为习惯”的多维建模思路，实现：

1. 风险关键特征识别；
2. 个体风险等级预警；
3. 以成本-疗效为导向的个体化干预优化。

### 1.2 需解决的三类核心问题
- **问题1（解释型）**：找出能表征痰湿严重程度且可预警高血脂风险的核心指标；量化九种体质贡献差异。
- **问题2（预测型）**：构建低/中/高三级风险预警模型，给出阈值依据并提取高危特征组合。
- **问题3（决策型）**：针对痰湿体质患者，优化6个月干预方案，在预算约束下实现积分改善。

---

## 2. 数据与预处理

### 2.1 数据结构
清洗前后数据围绕以下维度构建：
- 中医体质：主标签 + 九种体质积分（0-100）；
- 活动能力：ADL、IADL及总分（0-100）；
- 生化指标：TC、TG、LDL、HDL、血糖、尿酸、BMI；
- 诊断信息：高血脂二分类标签；
- 基础信息：年龄组、性别、吸烟、饮酒。

### 2.2 预处理策略
对应代码：`mm_c/preprocess.py`
- 数值列统一转换，缺失值按中位数插补；
- 连续变量采用 IQR 截尾（winsorize）控制极端值；
- 按参考范围构造异常标记（如 `tg_high`、`hdl_low`）；
- 生成总异常计数 `lipid_abnormal_count`，用于后续规则和分层。

主要输出：
- `outputs/step1_cleaned_dataset.csv`
- `outputs/step1_clean_report.json`

---

## 3. 方法体系与建模路径

### 3.1 整体技术路线
- **统计筛选**：Spearman、T检验、Mann-Whitney U；
- **特征筛选**：LASSO + Logistic 系数 + XGBoost 重要性融合打分；
- **解释归因**：OR（优势比）+ SHAP（树模型可解释）；
- **风险分层**：随机森林概率 + 规则判别 + CART阈值树；
- **关联规则**：Apriori 挖掘“高危组合”；
- **干预优化**：基于年龄/活动约束的强度-频率离散搜索，目标为“达标优先 + 低成本 + 更低终点评分”。

### 3.2 可复现脚本
- 问题1：`scripts/run_step2_problem1.py`
- 问题2：`scripts/run_step3_problem2.py`
- 问题3：`scripts/run_step4_problem3.py`
- 汇总可视化：`scripts/run_step5_report.py`

---

## 4. 问题一结果：关键指标与体质贡献

### 4.1 核心指标识别结果
来自 `outputs/problem1_top_summary.json` 的 Top 特征：

`tg, tc, uric_acid, ldl, hdl, adl_eat, iadl_cook, adl_dress, glucose, bmi`

说明：
- 血脂四项（TG/TC/LDL/HDL）是最直接且最稳定的高风险信号；
- 尿酸、血糖、BMI体现代谢共病特征；
- ADL/IADL 子项进入Top，说明功能状态与风险存在真实耦合关系。

### 4.2 体质贡献（OR 与 SHAP）
- OR Top3：`qi_deficiency`, `balanced`, `yang_deficiency`
- SHAP Top3：`blood_stasis`, `qi_stagnation`, `damp_heat`

解释建议：
- OR 与 SHAP排名不完全一致，反映“线性可解释”与“非线性交互”视角差异；
- 在中医语义下，可将“痰湿-瘀阻-郁滞”作为综合机制链路来解释异质性。

### 4.3 问题一结论
- 风险识别不应仅限单一血脂指标，应采用“代谢 + 活动 + 体质”联合建模；
- 体质变量具有显著解释价值，尤其适合用于早筛和分层管理。

---

## 5. 问题二结果：风险预警与分层规则

### 5.1 预测性能
来自 `outputs/problem2_summary.json`：
- **AUC = 0.8182**
- **Accuracy = 0.7800**

结论：模型具有较好的区分能力，适合用于基层慢病管理场景中的预警筛查。

### 5.2 风险分层分布
- Medium：709（70.9%）
- Low：169（16.9%）
- High：122（12.2%）

解读：
- 数据呈“中风险占主体”的典型慢病谱结构；
- 高风险比例约1/8，适合优先投入个体化干预资源。

### 5.3 CART 阈值依据（简化）
来自 `cart_rules`：
- `tg <= 1.69` 且 `tc <= 6.19` 倾向低风险；
- `tg > 1.69` 或 `tc > 6.19` 倾向高风险。

这与医学常识一致，增强了模型可解释性和业务可信度。

### 5.4 高风险特征组合（关联规则）
高 lift 规则显示：
- `tg_high + phlegm_high -> risk_high`
- `tc_high + phlegm_high -> risk_high`

说明：
- “脂质异常 + 痰湿偏高”是高危识别主通路；
- 中医体质信息对风险识别具有增益作用。

### 5.5 配套可视化
见 `outputs/figures/`：
- `problem2_risk_level_counts.png`
- `problem2_roc_curve.png`
- `problem2_top10_feature_importance.png`

---

## 6. 问题三结果：干预优化与个案方案

### 6.1 优化目标与约束
- 目标：达标优先（积分降至目标以下）+ 成本最小 + 终点评分尽量低；
- 约束：年龄可选强度、活动评分可选强度、频率1-10次/周、预算建议≤2000元。

### 6.2 ID=1/2/3 个案最优方案
数据来自 `outputs/problem3_id_1_2_3_best_plan.csv`。

| sample_id | baseline_score | target_score | intensity | frequency | final_score | total_cost | meets_target |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | 64.0 | 57.6 | 1 | 10 | 47.0459 | 1050 | True |
| 2 | 58.0 | 52.2 | 1 | 7 | 51.3789 | 684 | True |
| 3 | 59.0 | 53.1 | 1 | 7 | 52.2647 | 734 | True |

补充量化（由结果推导）：
- ID1 降幅约 **26.49%**；
- ID2 降幅约 **11.42%**；
- ID3 降幅约 **11.42%**；
- 3例平均总成本约 **822.67 元**。

### 6.3 全体痰湿患者策略分布
`outputs/tables/problem3_plan_summary_table.csv` 显示：
- 主流策略集中在 **1级强度 + 每周7次**（患者数最多，均衡成本与疗效）；
- 更高频次（8-10次/周）覆盖较少，但可获得更大降分幅度。

### 6.4 配套可视化
见 `outputs/figures/`：
- `problem3_cost_distribution.png`
- `problem3_score_drop_ratio_distribution.png`
- `problem3_intensity_frequency_heatmap.png`

---

## 7. 业务落地建议（可直接用于论文“建议”章节）

### 7.1 分层干预策略
- **高风险组**：优先实施高频管理（周8-10次）+ 严格随访；
- **中风险组**：以周6-8次中低强度为主，动态观察血脂与痰湿积分；
- **低风险组**：以维持性运动和饮食管理为主，防止风险上迁。

### 7.2 中西医融合管理框架
- 西医侧：TG/TC/LDL/HDL + 血糖/尿酸/BMI 的动态监测；
- 中医侧：体质评分（尤其痰湿相关）定期复评；
- 功能侧：ADL/IADL 同步纳入风险迭代模型。

### 7.3 管理流程建议
1. 首次筛查：一次性采集体质、活动、代谢、行为信息；
2. 自动分层：模型输出低/中/高风险；
3. 方案推荐：根据年龄和活动能力自动约束干预强度；
4. 月度复评：按积分变化和成本预算动态调参。

---

## 8. 局限性与后续优化方向

### 8.1 当前局限
- 训练数据为样例数据，外推前需做外部验证；
- 部分规则阈值来源于样本分布，跨地区/跨机构可能需重标定；
- 目前优化模型以静态规则为主，未引入长期依从性随机扰动。

### 8.2 下一步提升方向
- 引入时间序列随访数据，构建动态风险模型；
- 加入因果推断或倾向评分方法，提高“干预有效性”解释力度；
- 增加公平性与稳健性评估（年龄、性别亚组）。

---

## 9. 交付物清单（本次已生成）

### 9.1 核心报告
- `outputs/MathorCup_C_详细总结报告.md`（本文件）
- `outputs/problem1_3_key_results.md`（图表版摘要）

### 9.2 图表
- `outputs/figures/problem2_risk_level_counts.png`
- `outputs/figures/problem2_roc_curve.png`
- `outputs/figures/problem2_top10_feature_importance.png`
- `outputs/figures/problem3_cost_distribution.png`
- `outputs/figures/problem3_score_drop_ratio_distribution.png`
- `outputs/figures/problem3_intensity_frequency_heatmap.png`

### 9.3 表格
- `outputs/tables/problem2_risk_level_table.csv`
- `outputs/tables/problem2_top_rules_table.csv`
- `outputs/tables/problem3_id_1_2_3_table.csv`
- `outputs/tables/problem3_plan_summary_table.csv`
- `outputs/tables/problem3_agegroup_plan_table.csv`

---

## 10. 结论

本项目已形成可复现的“**解释-预警-优化**”完整建模闭环：
- 在解释层面识别了与高血脂风险紧密相关的关键代谢和活动指标；
- 在预测层面实现了可解释的三级风险分层并达到较好判别性能；
- 在决策层面产出了满足约束、可执行、可量化评估的个体化干预方案。

从比赛提交角度，本方案具备：
- **理论完整性**（中西医融合 + 数理统计 + 机器学习 + 优化决策）；
- **工程可复现性**（脚本化分步骤执行 + 结构化输出）；
- **结果可展示性**（图表、表格、个案方案齐全）。

