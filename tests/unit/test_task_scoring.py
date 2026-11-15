from app.modules.productivity.scoring import completion_xp


def test_completion_xp_uses_blueprint_formula() -> None:
    assert completion_xp(3, 4) == 45
