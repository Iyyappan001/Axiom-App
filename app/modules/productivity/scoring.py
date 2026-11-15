"""Task XP rules from the product blueprint."""


def completion_xp(difficulty: int, importance: int) -> int:
    if not 1 <= difficulty <= 5 or not 1 <= importance <= 5:
        raise ValueError("difficulty and importance must be between 1 and 5")
    return 10 + 5 * difficulty + 5 * importance
