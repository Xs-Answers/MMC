from __future__ import annotations

import ast
import json
from pathlib import Path


INTRO_TEXT = """# C题脚本逐段拆解 Notebook

这份 notebook 是根据 `c_problem_starter.py` 自动生成的学习版。

当前脚本采用 `pandas` + `DataFrame` 的组织方式，最值得你重点观察的是：

1. Excel 直接通过 `pandas.read_excel()` 读取；
2. 后续切片主要靠“列名”而不是列号；
3. 问题 1 / 2 / 3 的核心建模逻辑围绕同一张 `DataFrame` 展开。

推荐学习顺序：

- 先跑通 `load_dataframe()`；
- 再看问题 1 的指标筛选；
- 再看问题 2 的双层风险模型；
- 最后看问题 3 的干预优化。"""


STRUCTURE_TEXT = """## 这份 notebook 怎么看

这份 notebook 会按脚本原始顺序展开：

- 导入依赖
- 常量和列名映射
- 数据结构
- 数据读取
- 问题 1
- 问题 2
- 问题 3
- 命令行入口

我在关键函数后额外补了三类内容：

- `函数签名`
- `学习提示`
- `试运行`

这样你可以一边对照源码，一边看实际输出。"""


SECTION_TEXT = {
    "__imports__": """## 1. 导入依赖

这部分是当前脚本的基础环境。

这里会直接导入 `pandas`，说明它已经是这份脚本的默认依赖。""",
    "__constants__": """## 2. 常量、列名映射和字段分组

这一段是当前脚本的“坐标系”。

最重要的几组信息是：

- `RAW_TO_ENGLISH`：把 Excel 中文列名映射成英文列名；
- `CONSTITUTION_SCORE_COLS`：九种体质积分列；
- `ACTIVITY_LAB_COLS`：活动能力和检验指标；
- `EARLY_WARNING_COLS` / `ALL_FEATURE_COLS`：问题 2 不同模型使用的列组。""",
    "PlanResult": """## 3. 干预方案的数据结构

这里使用 `PlanResult` 数据类来统一保存问题 3 的优化结果。""",
    "MonthlyAction": """## 4. 月度动作的数据结构

这个数据类把“某个月采取什么动作”拆成了清晰字段：

- 强度；
- 每周频次；
- 对应的月度降幅；
- 对应的训练成本。""",
    "MonthlyRecord": """## 5. 月度执行记录的数据结构

这个数据类用来保存动态规划恢复出来的逐月路径明细。""",
    "find_default_xlsx": """## 6. 自动寻找样例数据

这个函数会在当前项目目录里寻找 C 题的 `.xlsx` 样例文件。""",
    "load_dataframe": """## 7. 读取 Excel 为 DataFrame

这里直接使用 `pd.read_excel()`：

1. 读取 Excel；
2. 校验字段是否齐全；
3. 把中文列名改成英文列名；
4. 统一转成数值列。

从这里开始，后面所有建模操作都建立在 `DataFrame` 之上。""",
    "summarize_problem_1": """## 8. 问题 1：关键指标筛选与体质贡献分析

这一段的实现方式很接近数据分析常见写法：

- 候选变量直接用列名选择；
- 结果也更多地组织成 `DataFrame`；
- 排序和汇总会更适合后续转表格。""",
    "build_feature_matrix": """## 9. 诊断型模型特征矩阵

这个函数返回用于诊断型模型的特征矩阵。

这一步非常直观：直接用列名列表从 `df` 中取列。""",
    "build_early_warning_matrix": """## 10. 早预警模型特征矩阵

这一段依然体现“双层模型”思想：

- 诊断型模型保留直接血脂指标；
- 早预警模型去掉直接血脂指标。""",
    "fit_risk_models": """## 11. 问题 2：训练双层风险模型

这是问题 2 的核心函数。

因为输入是 `DataFrame`，所以：

- 特征更容易按名称解释；
- 重要特征结果也更容易整理成表。""",
    "lipid_abnormal_count": """## 12. 统计血脂异常项数

这个函数会根据题目给定的临床阈值，计算单个患者有多少项血脂异常。""",
    "build_early_warning_row": """## 13. 构造单个样本的早预警输入

这里把一个 `Series` 重新包装成单行 `DataFrame`，这样就能直接喂给 sklearn 模型。""",
    "assign_risk_level": """## 14. 低中高风险分层

这里依然采用“规则 + 模型”的融合思路：

- 先看血脂异常项数；
- 再看痰湿积分和活动能力；
- 最后结合模型概率。""",
    "summarize_risk_levels": """## 15. 汇总风险等级分布

这个函数会遍历整张表，为每个样本分层，然后统计低、中、高风险的样本量。""",
    "tcm_level": """## 16. 中医调理等级映射

根据痰湿积分，把患者映射到 1 / 2 / 3 级调理方案。""",
    "allowed_intensities": """## 17. 可选活动强度约束

这一段把题目里的年龄约束和活动能力约束写成代码。""",
    "activity_monthly_drop": """## 18. 月度降分比例

这一段把题目里的“强度提升”和“频次增加”对痰湿积分的影响翻译成公式。""",
    "available_monthly_actions": """## 19. 生成非劣月度动作集合

这个函数会先把所有允许动作列出来，再剔除“降幅相同但成本更高”的动作。""",
    "simulate_action_sequence": """## 20. 模拟一条月度路径

给定一串按月动作，这个函数会逐月模拟痰湿积分变化和成本变化。""",
    "optimize_intervention": """## 21. 问题 3：搜索最优干预方案

这一步不再固定 6 个月都用同一方案，而是把“月份 + 当前积分”作为状态，用动态规划求最小总成本。""",
    "collect_problem_3_results": """## 22. 批量收集问题 3 结果

这个函数会对指定样本列表逐个求解最优方案。""",
    "export_problem_outputs": """## 23. 导出三道题结果

这个函数会把问题 1 / 2 / 3 的核心结果自动写入 `赛题/outputs/`。""",
    "print_problem_1": """## 24. 问题 1 输出函数

把问题 1 的核心结果打印得更清晰。""",
    "print_problem_2": """## 25. 问题 2 输出函数

把问题 2 的模型表现、重要特征和分层结果集中打印出来。""",
    "print_problem_3": """## 26. 问题 3 输出函数

把指定样本的最优方案和逐月明细打印出来。""",
    "main": """## 27. 命令行入口

如果你在终端里直接运行 `c_problem_starter.py`，就是从这里开始执行。""",
    "__main_block__": """## 28. 入口判断

这一段是标准 Python 脚本入口判断，在 notebook 里一般不会直接依赖，但保留有助于理解脚本结构。""",
}


LEARNING_TEXT = {
    "load_dataframe": """### 学习提示

这一段是整份脚本最值得先跑通的地方。

重点关注：

1. 为什么这里直接用 `pd.read_excel()` 就够了？
2. `RAW_TO_ENGLISH` 为什么很重要？
3. 为什么这里要把所有保留列统一转成数值？

自测问题：

1. 如果 Excel 列名和预期不一致，这段代码会在哪里报错？
2. 如果某一列里混入了非数值字符串，会在哪里报错？""",
    "summarize_problem_1": """### 学习提示

问题 1 的建模逻辑重点在“数据组织方式”。

重点关注：

1. `x_candidates = df[ACTIVITY_LAB_COLS]` 为什么足够直观；
2. 为什么结果最后要整理成 `DataFrame`；
3. 这样做对后续写论文表格有什么好处。 """,
    "fit_risk_models": """### 学习提示

这是问题 2 最关键的函数。

建议你重点看：

1. 诊断型模型和早预警模型的输入列有什么差别；
2. 为什么重要特征这里会被整理成带列名的表；
3. 这种写法对后续出表和解释结论有什么帮助。""",
    "assign_risk_level": """### 学习提示

这里体现的是“模型不是唯一依据”。

最终风险分层同时依赖：

- 血脂异常项数；
- 痰湿积分；
- 活动能力；
- 模型概率。

你可以边看代码边回答：为什么高风险不只看概率？""",
    "optimize_intervention": """### 学习提示

问题 3 的优化逻辑重点已经变成“状态设计 + 动态规划”。

建议你关注：

1. 这里输入为什么选择 `pd.Series`；
2. 状态为什么只保留“当前月份 + 当前积分”就够了；
3. 为什么要先剔除同降幅高成本的动作。""",
    "export_problem_outputs": """### 学习提示

这一段很适合用来学习“研究脚本如何落地成可交付结果”。

重点看：

1. 为什么每一道题都单独建子目录；
2. 为什么有的结果适合保存成 `csv`，有的适合保存成 `json/txt`；
3. 图像结果是怎样从论文目录复制到 `outputs` 的。""",
    "main": """### 学习提示

你可以把 `main()` 当成整份脚本的“流程图”来看。

如果你只想研究某一问，其实不一定要跑它；你可以直接在 notebook 中单独调用对应函数。""",
}


DEMO_AFTER = {
    "load_dataframe": {
        "title": "### 试运行：读取 DataFrame",
        "code": """workbook = find_default_xlsx(Path.cwd())
df = load_dataframe(workbook)
print(f"Workbook: {workbook}")
print(df.shape)
print(df.head(3))
print(list(df.columns[:10]))""",
        "observe": """### 运行后你应该观察什么

重点检查：

1. DataFrame 行列数是否正确；
2. 列名是不是已经从中文变成英文；
3. 前几行数据看起来是不是正常数值。""",
    },
    "print_problem_1": {
        "title": "### 试运行：问题 1",
        "code": """problem_1 = summarize_problem_1(df)
print_problem_1(problem_1)
print(problem_1["consensus"].head())""",
        "observe": """### 运行后你应该观察什么

重点看：

1. 共识排序前几名是谁；
2. `consensus` 已经是 DataFrame，这对后面导出表格非常方便。""",
    },
    "print_problem_2": {
        "title": "### 试运行：问题 2",
        "code": """problem_2 = fit_risk_models(df)
print_problem_2(problem_2, df)
print(problem_2["diagnostic_importance"].head())""",
        "observe": """### 运行后你应该观察什么

重点看：

1. 两套模型效果差多少；
2. 重要特征表是否已经带有清晰列名；
3. 风险等级统计是否符合预期。""",
    },
    "print_problem_3": {
        "title": "### 试运行：问题 3",
        "code": """print_problem_3(df, [1, 2, 3], target_ratio=0.90, budget=2000.0)""",
        "observe": """### 运行后你应该观察什么

重点看：

1. DataFrame 版在读取单个患者属性时是不是更直观；
2. 三个样本的最终方案是否满足目标并控制在预算内。""",
    },
}


def md_cell(text: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in text.strip().splitlines()],
    }


def code_cell(text: str) -> dict:
    text = text.rstrip() + "\n"
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": text.splitlines(keepends=True),
    }


def start_lineno(node: ast.AST) -> int:
    if hasattr(node, "decorator_list") and getattr(node, "decorator_list"):
        return min(deco.lineno for deco in node.decorator_list)
    return node.lineno


def source_from_lines(lines: list[str], start: int, end: int) -> str:
    return "".join(lines[start - 1 : end])


def render_signature(node: ast.AST) -> str:
    if isinstance(node, ast.FunctionDef):
        return f"`def {node.name}({ast.unparse(node.args)})`"
    if isinstance(node, ast.ClassDef):
        return f"`class {node.name}`"
    return "`unknown`"


def generic_hint(node: ast.AST) -> str:
    kind = "函数" if isinstance(node, ast.FunctionDef) else "类"
    return f"""### 学习提示

这段是一个{kind}定义。

建议你先回答：

1. 它的输入是什么？
2. 它的输出是什么？
3. 它在整个脚本流程里属于哪一步？

函数签名：

{render_signature(node)}"""


def build_notebook(script_path: Path, output_path: Path) -> None:
    source = script_path.read_text(encoding="utf-8")
    lines = source.splitlines(keepends=True)
    tree = ast.parse(source)

    cells: list[dict] = [md_cell(INTRO_TEXT), md_cell(STRUCTURE_TEXT)]
    nodes = tree.body
    i = 0
    while i < len(nodes):
        node = nodes[i]

        if isinstance(node, (ast.Import, ast.ImportFrom)):
            start = start_lineno(node)
            end = node.end_lineno
            j = i + 1
            while j < len(nodes) and isinstance(nodes[j], (ast.Import, ast.ImportFrom)):
                end = nodes[j].end_lineno
                j += 1
            cells.append(md_cell(SECTION_TEXT["__imports__"]))
            cells.append(code_cell(source_from_lines(lines, start, end)))
            cells.append(
                md_cell(
                    """### 学习提示

这里可以顺手记住：`pandas` 已经是这份脚本的默认依赖。

所以你后面阅读和运行时，都可以把 `DataFrame` 当作主线来理解。"""
                )
            )
            i = j
            continue

        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            start = start_lineno(node)
            end = node.end_lineno
            j = i + 1
            while j < len(nodes) and isinstance(nodes[j], (ast.Assign, ast.AnnAssign)):
                end = nodes[j].end_lineno
                j += 1
            cells.append(md_cell(SECTION_TEXT["__constants__"]))
            cells.append(code_cell(source_from_lines(lines, start, end)))
            cells.append(
                md_cell(
                    """### 学习提示

当前脚本的核心设计之一，就体现在这里。

这里更强调“列名分组”，而不是散落在各处的整数列号。

建议你重点看：

1. `RAW_TO_ENGLISH` 是如何把中文列名统一成英文列名的；
2. `CONSTITUTION_SCORE_COLS / ACTIVITY_LAB_COLS` 这些列组为什么后面会反复复用。"""
                )
            )
            i = j
            continue

        if isinstance(node, ast.ClassDef):
            cells.append(md_cell(SECTION_TEXT.get(node.name, f"## 类：{node.name}")))
            cells.append(code_cell(source_from_lines(lines, start_lineno(node), node.end_lineno)))
            cells.append(md_cell(f"### 函数/类签名\n\n{render_signature(node)}"))
            cells.append(md_cell(LEARNING_TEXT.get(node.name, generic_hint(node))))
            i += 1
            continue

        if isinstance(node, ast.FunctionDef):
            cells.append(md_cell(SECTION_TEXT.get(node.name, f"## 函数：`{node.name}`")))
            cells.append(code_cell(source_from_lines(lines, start_lineno(node), node.end_lineno)))
            cells.append(md_cell(f"### 函数签名\n\n{render_signature(node)}"))
            cells.append(md_cell(LEARNING_TEXT.get(node.name, generic_hint(node))))
            if node.name in DEMO_AFTER:
                cells.append(md_cell(DEMO_AFTER[node.name]["title"]))
                cells.append(code_cell(DEMO_AFTER[node.name]["code"]))
                cells.append(md_cell(DEMO_AFTER[node.name]["observe"]))
            i += 1
            continue

        if isinstance(node, ast.If):
            cells.append(md_cell(SECTION_TEXT["__main_block__"]))
            cells.append(code_cell(source_from_lines(lines, start_lineno(node), node.end_lineno)))
            cells.append(
                md_cell(
                    """### 学习提示

脚本模式下会从这里触发 `main()`；
而在 notebook 中，你通常会更喜欢逐段调用前面的函数。"""
                )
            )
            i += 1
            continue

        i += 1

    cells.append(
        md_cell(
            """## 结束说明

这份 notebook 适合你按“读数据 -> 做筛选 -> 做预警 -> 做优化”的顺序反复回看。

如果你之后继续修改 `c_problem_starter.py`，重新运行本目录下的 `build_step_by_step_notebook.py` 即可自动重建 notebook。"""
        )
    )

    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "version": "3.11",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    output_path.write_text(json.dumps(notebook, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    script_path = Path(__file__).with_name("c_problem_starter.py")
    output_path = Path(__file__).with_name("c_problem_starter_step_by_step.ipynb")
    build_notebook(script_path, output_path)
    print(f"Notebook written to: {output_path}")


if __name__ == "__main__":
    main()
