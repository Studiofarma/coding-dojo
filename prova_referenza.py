from dataclasses import dataclass


@dataclass
class Coord:
    x: int
    y: int


c = Coord(0, 0)


def f1(c: Coord) -> Coord:
    c.x += 1
    return c


def f2(c: Coord) -> None:
    c.y += 1


c1 = f1(c)
c2 = f2(c)

print(c1)
print(c2)
