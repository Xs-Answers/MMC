from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

import pandas as pd

from mm_c.config import TCM_MONTHLY_COST, TRAIN_UNIT_COST


@dataclass
class PlanResult:
    sample_id: int
    age_group: int
    activity_total: float
    baseline_score: float
    target_score: float
    intensity: int
    frequency: int
    final_score: float
    total_cost: float
    meets_target: bool


def tcm_level(score: float) -> int:
    if score <= 58:
        return 1
    if score <= 61:
        return 2
    return 3


def allowed_intensities(age_group: int, activity_total: float) -> list[int]:
    if age_group <= 2:
        age_allowed = {1, 2, 3}
    elif age_group <= 4:
        age_allowed = {1, 2}
    else:
        age_allowed = {1}

    if activity_total < 40:
        score_allowed = {1}
    elif activity_total < 60:
        score_allowed = {1, 2}
    else:
        score_allowed = {1, 2, 3}

    return sorted(age_allowed & score_allowed)


def monthly_drop_rate(intensity: int, frequency: int) -> float:
    if frequency < 5:
        return 0.0
    # 每提升一级强度，月下降约3%；每周增加1次频率，月下降约1%
    return 0.03 * (intensity - 1) + 0.01 * (frequency - 5)


def simulate_6m_plan(baseline_score: float, intensity: int, frequency: int, months: int = 6) -> tuple[float, float]:
    score = float(baseline_score)
    total_cost = 0.0
    drop = monthly_drop_rate(intensity, frequency)

    for _ in range(months):
        level = tcm_level(score)
        total_cost += TCM_MONTHLY_COST[level] + TRAIN_UNIT_COST[intensity] * frequency * 4
        score = score * (1 - drop)

    return score, total_cost


def optimize_patient(row: pd.Series, target_ratio: float = 0.90, budget: float = 2000.0) -> PlanResult:
    baseline = float(row["phlegm_dampness"])
    target = baseline * target_ratio
    age_group = int(row["age_group"])
    activity_total = float(row["activity_total"])

    candidates: list[PlanResult] = []
    for intensity in allowed_intensities(age_group, activity_total):
        for frequency in range(1, 11):
            final_score, cost = simulate_6m_plan(baseline, intensity, frequency)
            meets = final_score <= target and cost <= budget
            candidates.append(
                PlanResult(
                    sample_id=int(row["sample_id"]),
                    age_group=age_group,
                    activity_total=activity_total,
                    baseline_score=baseline,
                    target_score=target,
                    intensity=intensity,
                    frequency=frequency,
                    final_score=final_score,
                    total_cost=cost,
                    meets_target=meets,
                )
            )

    # 优先满足目标与预算，其次成本低，再其次终点评分低
    candidates.sort(key=lambda x: (not x.meets_target, x.total_cost, x.final_score, -x.frequency))
    return candidates[0]


def run_problem3(df: pd.DataFrame, output_dir: Path, sample_ids: tuple[int, ...] = (1, 2, 3), budget: float = 2000.0, target_ratio: float = 0.90) -> pd.DataFrame:
    output_dir.mkdir(parents=True, exist_ok=True)

    phlegm_df = df[df["constitution_tag"] == 5].copy()
    results = []

    for sid in sample_ids:
        target_rows = phlegm_df[phlegm_df["sample_id"] == sid]
        if target_rows.empty:
            fallback = df[df["sample_id"] == sid]
            if fallback.empty:
                continue
            row = fallback.iloc[0]
        else:
            row = target_rows.iloc[0]

        result = optimize_patient(row, target_ratio=target_ratio, budget=budget)
        results.append(asdict(result))

    all_results = []
    for _, row in phlegm_df.iterrows():
        all_results.append(asdict(optimize_patient(row, target_ratio=target_ratio, budget=budget)))

    id_df = pd.DataFrame(results)
    all_df = pd.DataFrame(all_results)

    id_df.to_csv(output_dir / "problem3_id_1_2_3_best_plan.csv", index=False, encoding="utf-8-sig")
    all_df.to_csv(output_dir / "problem3_all_phlegm_patients_best_plan.csv", index=False, encoding="utf-8-sig")
    return id_df

