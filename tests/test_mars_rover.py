from dataclasses import dataclass, field
from enum import Enum

import pytest


@dataclass
class PlanetMap:
    width: int
    height: int
    obstacle_list: list["Obstacle"] = field(default=[])


@dataclass
class RoverPosition:
    x: int
    y: int


class CommandsEnum(Enum):
    NORTH = "N"
    SOUTH = "S"
    WEST = "W"
    EAST = "E"


def single_move_rover(
    planet_map: PlanetMap,
    current_position: RoverPosition,
    command: CommandsEnum,
) -> RoverPosition:

    match command:
        case CommandsEnum.NORTH:
            return RoverPosition(
                current_position.x,
                (current_position.y + 1) % planet_map.height,
            )

        case CommandsEnum.EAST:
            return RoverPosition(
                (current_position.x + 1) % planet_map.width,
                current_position.y,
            )

        case CommandsEnum.SOUTH:

            return RoverPosition(
                current_position.x,
                (current_position.y - 1) % planet_map.height,
            )

        case CommandsEnum.WEST:
            return RoverPosition(
                (current_position.x - 1) % planet_map.width,
                current_position.y,
            )


def move_rover(
    planet_map: PlanetMap,
    current_position: RoverPosition,
    command_list: list[CommandsEnum],
) -> RoverPosition:

    match command_list:
        case []:
            return RoverPosition(current_position.x, current_position.y)
        case _:
            for command in command_list:
                next_position = single_move_rover(
                    planet_map, current_position, command
                )
                current_position = next_position

            return current_position


def test_planet_map_1_1_return_same_position() -> None:
    planet_map = PlanetMap(width=1, height=1)
    rover_position = RoverPosition(x=0, y=0)
    next_position = move_rover(
        planet_map=planet_map,
        current_position=rover_position,
        command_list=[],
    )
    expected_position = RoverPosition(0, 0)
    assert next_position == expected_position


@pytest.mark.parametrize(
    "current_position, expected_position, list_commands",
    [
        (RoverPosition(0, 0), RoverPosition(0, 1), [CommandsEnum.NORTH]),
        (RoverPosition(0, 0), RoverPosition(1, 0), [CommandsEnum.EAST]),
        (RoverPosition(0, 1), RoverPosition(0, 0), [CommandsEnum.SOUTH]),
        (RoverPosition(1, 0), RoverPosition(0, 0), [CommandsEnum.WEST]),
        (
            RoverPosition(0, 0),
            RoverPosition(0, 2),
            [CommandsEnum.NORTH, CommandsEnum.NORTH],
        ),
        (
            RoverPosition(0, 2),
            RoverPosition(0, 0),
            [CommandsEnum.NORTH],
        ),
        (
            RoverPosition(2, 0),
            RoverPosition(0, 0),
            [CommandsEnum.EAST],
        ),
        (
            RoverPosition(0, 0),
            RoverPosition(2, 0),
            [CommandsEnum.WEST],
        ),
        (
            RoverPosition(0, 0),
            RoverPosition(0, 2),
            [CommandsEnum.SOUTH],
        ),
    ],
)
def test_moving_rover_into_single_different_direction(
    current_position: RoverPosition,
    expected_position: RoverPosition,
    list_commands: list[CommandsEnum],
):

    planet_map = PlanetMap(width=3, height=3)
    next_position = move_rover(
        planet_map=planet_map,
        current_position=current_position,
        command_list=list_commands,
    )

    assert next_position == expected_position


def test_moving_rover_into_obstacle():
    obstacle = Obstacle(x=1, y=2)
    planet_map = PlanetMap(width=3, height=3, obstacle_list=[obstacle])

    next_position = move_rover(
        planet_map=planet_map,
        current_position=RoverPosition(1, 1),
        command_list=[CommandsEnum.EAST],
    )

    assert next_position == RoverPosition(1, 1)


@dataclass
class Obstacle:
    x: int
    y: int
