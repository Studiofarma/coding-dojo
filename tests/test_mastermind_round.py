from mastermind import evaluate_mastermind

import pytest


@pytest.mark.parametrize(
    "guess, combination, expected_result",
    [
        (["blue"], ["blue"], (1, 0)),
        (["red"], ["blue"], (0, 0)),
        (["red", "blue"], ["red", "blue"], (2, 0)),
        (["red", "yellow"], ["red", "blue"], (1, 0)),
        (["red", "yellow"], ["yellow", "red"], (0, 2)),
        (["blue", "yellow"], ["yellow", "red"], (0, 1)),
        (["red", "blue"], ["red", "red"], (1, 0)),
        (["red", "red", "red"], ["red", "red", "red"], (3, 0)),
        (["red", "yellow", "blue"], ["red", "blue", "green"], (1, 1)),
    ],
)
def test_mastermind(
    guess: list[str], combination: list[str], expected_result: tuple[int, int]
) -> None:
    combination_result = evaluate_mastermind(guess, combination)
    assert combination_result == expected_result
