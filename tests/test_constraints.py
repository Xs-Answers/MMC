from __future__ import annotations

from mm_c.problem3_optimize import allowed_intensities


def test_allowed_intensity_by_age_and_score() -> None:
    assert allowed_intensities(5, 70) == [1]
    assert allowed_intensities(4, 50) == [1, 2]
    assert allowed_intensities(2, 80) == [1, 2, 3]

