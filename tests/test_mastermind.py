from dataclasses import dataclass
from enum import Enum

import pytest

from tests import test_mastermind_round


class GameStatusEnum(Enum):
    Win = 0
    Lose = 1
    Continue = 2


@dataclass
class GameResult:
    result: tuple[int, int]
    remaning_attempts: int
    game_status: "GameStatusEnum"


@pytest.mark.parametrize(
    "guess_input, max_attempts, effective_combination, expected_result",
    [
        ([], 0, [], GameResult((0, 0), 0, GameStatusEnum.Lose)),
        (["red"], 1, ["red"], GameResult((1, 0), 0, GameStatusEnum.Win)),
        (
            ["blue", "red"],
            1,
            ["blue", "yellow"],
            GameResult((1, 0), 0, GameStatusEnum.Lose),
        ),
        (
            ["blue", "red"],
            2,
            ["blue", "yellow"],
            GameResult((1, 0), 1, GameStatusEnum.Continue),
        ),
    ],
)
def test_mastermind(
    guess_input: list[str],
    max_attempts: int,
    effective_combination: list[str],
    expected_result: "GameResult",
):
    output: GameResult = Game(
        guess_input, max_attempts, effective_combination
    )
    assert output == expected_result


def Game(
    guess_input: list[str],
    max_attempts: int,
    effective_combination: list[str],
) -> "GameResult":
    evaluate = test_mastermind_round.evaluate_mastermind(
        guess_input, effective_combination
    )
    win = len(guess_input) == evaluate[0]

    if win and max_attempts > 0:
        return GameResult(evaluate, max_attempts - 1, GameStatusEnum.Win)
    elif not win and max_attempts > 0:
        return GameResult(evaluate, 1, GameStatusEnum.Continue)
    return GameResult(evaluate, 0, GameStatusEnum.Lose)
