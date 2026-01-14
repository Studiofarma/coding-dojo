from abc import ABC, abstractmethod
from typing import Optional

import pytest


@pytest.mark.parametrize(
    "expression,expected",
    [
        ("1", 1),
        ("2", 2),
        ("1 2 +", 3),
        ("4 2 + 3 +", 9),
        ("4 2 3 + +", 9),
        ("1 4 + 2 3 + +", 10),
        ("6 5 + 1 4 + 2 3 + + +", 21),
        ("1 2 + 6 5 + + 1 4 + 2 3 + + +", 24),
    ],
)
def test_rpn(expression: str, expected: float):
    assert rpn(expression) == expected


def rpn(expression: str) -> float:
    tokens = split(expression)
    if len(tokens) == 1:
        return float(tokens[0])
    result = check_token(tokens[0])
    for token in tokens[1:]:
        operand = check_token(token)
        result.append(operand)

    return result.execute()


def test_split() -> None:
    assert split("1 2       +") == ["+", "2", "1"]
    assert split("1 2 +") == ["+", "2", "1"]
    assert split("4 2 + 3 -") == ["-", "3", "+", "2", "4"]


def split(expression: str) -> list[str]:
    expression_tokens = expression.split()
    expression_tokens.reverse()
    return expression_tokens


def check_token(token: str) -> "Operand":
    print(f"current token is {token}")
    if token == "+":
        return Sum()
    else:
        return Digit(token)


class Operand(ABC):
    @abstractmethod
    def execute(self) -> float:
        pass

    @abstractmethod
    def append(self, operand: "Operand") -> bool:
        pass


class Digit(Operand):

    def __init__(self, value: str):
        self.value = float(value)

    def execute(self) -> float:
        return self.value

    def append(self, operand: "Operand") -> bool:
        return False


class Sum(Operand):

    def __init__(self):
        self.x = None
        self.y = None

    def execute(self) -> float:
        return self.x.execute() + self.y.execute()

    def append(self, operand: "Operand") -> bool:
        if self.x == None:
            self.x = operand
            return True
        if self.y == None:
            self.y = operand
            return True

        if not self.x.append(operand):
            return self.y.append(operand)

        return True
