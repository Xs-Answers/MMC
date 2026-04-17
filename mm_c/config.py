from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_XLSX = ROOT / "mathmathor-cup-c" / "附件1：样例数据.xlsx"
OUTPUT_DIR = ROOT / "outputs"

CONSTITUTION_NAMES = [
    "balanced",
    "qi_deficiency",
    "yang_deficiency",
    "yin_deficiency",
    "phlegm_dampness",
    "damp_heat",
    "blood_stasis",
    "qi_stagnation",
    "special_diathesis",
]

ACTIVITY_LAB_NAMES = [
    "adl_toilet",
    "adl_eat",
    "adl_walk",
    "adl_dress",
    "adl_bath",
    "adl_total",
    "iadl_shop",
    "iadl_cook",
    "iadl_finance",
    "iadl_transport",
    "iadl_medication",
    "iadl_total",
    "activity_total",
    "hdl",
    "ldl",
    "tg",
    "tc",
    "glucose",
    "uric_acid",
    "bmi",
]

BASE_COLUMNS = [
    "sample_id",
    "constitution_tag",
    *CONSTITUTION_NAMES,
    *ACTIVITY_LAB_NAMES,
    "hyperlipidemia_label",
    "lipid_subtype",
    "age_group",
    "sex",
    "smoke",
    "drink",
]

IDX = {name: i for i, name in enumerate(BASE_COLUMNS)}

LIPID_NORMAL_RANGES = {
    "tc": (3.1, 6.2),
    "tg": (0.56, 1.7),
    "ldl": (2.07, 3.1),
    "hdl": (1.04, 1.55),
    "glucose": (3.9, 6.1),
    "bmi": (18.5, 23.9),
}

TCM_MONTHLY_COST = {1: 30, 2: 80, 3: 130}
TRAIN_UNIT_COST = {1: 3, 2: 5, 3: 8}

