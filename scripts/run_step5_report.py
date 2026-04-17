from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mm_c.config import OUTPUT_DIR
from mm_c.reporting import build_key_results_markdown, build_problem2_artifacts, build_problem3_artifacts


def main() -> None:
    build_problem2_artifacts(OUTPUT_DIR)
    build_problem3_artifacts(OUTPUT_DIR)
    report_path = build_key_results_markdown(OUTPUT_DIR)
    print(f"Step5 done -> {report_path}")


if __name__ == "__main__":
    main()

