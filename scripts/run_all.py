from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.run_step1_preprocess import main as step1
from scripts.run_step2_problem1 import main as step2
from scripts.run_step3_problem2 import main as step3
from scripts.run_step4_problem3 import main as step4
from scripts.run_step5_report import main as step5


if __name__ == "__main__":
    step1()
    step2()
    step3()
    step4()
    step5()
    print("All steps finished. Check outputs/ directory.")
