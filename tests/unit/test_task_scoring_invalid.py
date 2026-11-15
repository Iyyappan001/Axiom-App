import pytest

from app.modules.productivity.scoring import completion_xp


def test_completion_xp_rejects_out_of_range_inputs() -> None:
    with pytest.raises(ValueError):
        completion_xp(0, 3)
