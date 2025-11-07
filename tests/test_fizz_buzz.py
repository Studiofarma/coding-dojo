from abc import ABC, abstractmethod
from typing import Any, Protocol

import pytest


@pytest.mark.parametrize(
    "value,expected",
    [
        (1, "1"),
        (2, "2"),
        (3, "FizzFizz"),
        (4, "4"),
        (5, "Buzz"),
        (6, "Fizz"),
        (7, "Banana"),
        (10, "Buzz"),
        (15, "FizzBuzz"),
        (21, "FizzBanana"),
        (35, "FizzBuzzBanana"),
        (104, "104"),
        (105, "FizzBuzzBanana"),
    ],
)
def test_fizz_buzz(value: int, expected: str) -> None:
    assert fizz_buzz(value) == expected


class ConversionRule(ABC):

    @abstractmethod
    def convert(self, value: int) -> str:
        pass


class DivisibileByConversion(ConversionRule):
    def __init__(self, divisor: int, str_value: str) -> None:
        self.divisor = divisor
        self.str_value = str_value

    def convert(self, value: int) -> str:
        if is_divisible_by(value, self.divisor):
            return self.str_value
        return ""


class ContainsConversion(ConversionRule):
    def __init__(self, check_value: str, str_value: str) -> None:
        self.check_value = check_value
        self.str_value = str_value

    def convert(self, value: int) -> str:
        if contains(value, self.check_value):
            return self.str_value
        return ""


class ContainsAsterisk(ConversionRule):
    def convert(self, value: int) -> str:
        return contains_asterisk(value)


class FizzBuzz:
    def __init__(self, conversion_rules: list[ConversionRule]):
        self.conversion_rules = conversion_rules

    def run(self, value: int) -> str:
        return_string = ""
        for rule in self.conversion_rules:
            return_string += rule.convert(value)

        if return_string == "":
            return_string = str(value)

        return return_string


def fizz_buzz(x: int) -> str:
    conversions_rules = [
        ContainsConversion("3", "Fizz"),
        DivisibileByConversion(3, "Fizz"),
        DivisibileByConversion(5, "Buzz"),
        DivisibileByConversion(7, "Banana"),
        ContainsAsterisk(),
    ]

    fizzbuzz = FizzBuzz(conversions_rules)
    return fizzbuzz.run(x)


def contains(value: int, check_value: str):
    return check_value in str(value)


def is_divisible_by(value: int, divisor: int) -> bool:
    return value % divisor == 0


def test_contains_asterisk():
    assert ContainsAsterisk().convert(0) == "*"
    assert ContainsAsterisk().convert(1) == ""
    assert ContainsAsterisk().convert(2) == ""
    assert ContainsAsterisk().convert(10) == "*"
    assert ContainsAsterisk().convert(100) == "**"


def contains_asterisk(value: int) -> str:
    str_value = str(value)
    num_of_zero = str_value.count("0")
    if num_of_zero > 0:
        return "*" * num_of_zero

    return ""
