# MathorCup C 题分步骤建模代码

本项目根据 `mathmathor-cup-c/C题_数学建模思路与方案解析.md` 第五部分 `Next Steps` 拆分实现为多个独立脚本。

## 目录结构

- `mm_c/config.py`：全局配置、字段映射、阈值和成本常量
- `mm_c/data_io.py`：读取 Excel 并标准化字段
- `mm_c/preprocess.py`：数据清洗、异常值处理、异常标记
- `mm_c/problem1_analysis.py`：问题一（相关性、显著性检验、LASSO/XGBoost、OR、SHAP）
- `mm_c/problem2_risk.py`：问题二（风险预警模型、三级分层、CART阈值）
- `mm_c/problem2_rules.py`：问题二（Apriori 关联规则）
- `mm_c/problem3_optimize.py`：问题三（6个月干预优化）
- `mm_c/reporting.py`：问题2/3可视化、汇总表与问题1-3 Markdown报告
- `scripts/run_step1_preprocess.py`：步骤1执行脚本
- `scripts/run_step2_problem1.py`：步骤2执行脚本
- `scripts/run_step3_problem2.py`：步骤3执行脚本
- `scripts/run_step4_problem3.py`：步骤4执行脚本
- `scripts/run_step5_report.py`：步骤5执行脚本（图表+表格+汇总MD）
- `scripts/run_all.py`：一键执行全部步骤

## 环境

已提供：
- `environment.yml`
- `requirements.txt`

创建环境：

```powershell
conda env create -f environment.yml
conda activate mm-c
```

## 运行

分步骤：

```powershell
python scripts/run_step1_preprocess.py
python scripts/run_step2_problem1.py
python scripts/run_step3_problem2.py
python scripts/run_step4_problem3.py
python scripts/run_step5_report.py
```

一键运行：

```powershell
python scripts/run_all.py
```

## 输出结果

所有结果输出到 `outputs/`，包括：
- `step1_cleaned_dataset.csv`
- `problem1_*.csv`
- `problem2_*.csv`
- `problem3_*.csv`
- `problem1_3_key_results.md`
- `figures/*.png`
- `tables/*.csv`

