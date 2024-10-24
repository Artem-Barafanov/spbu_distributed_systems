import random
from graphics import Graphics


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        board = []
        for i in range(height):
            board.append([0]*width)
        self.field = board

    def __len__(self):
        return len(self.field)


class Robot:
    def __init__(self, speed: int, size: int, coordinates: list[int], board: Board, graphic: Graphics):
        self.speed: int = speed
        self.size: int = size
        self.coordinates: list[int] = coordinates
        self.board = board
        self.graphic = graphic

    def walk(self, direction: str, distance: int):
        match direction:
            case "left":
                self.coordinates[0] += distance
            case "right":
                self.coordinates[0] -= distance
            case "up":
                self.coordinates[1] += distance
            case "down":
                self.coordinates[1] -= distance

    def paint(self):
        self.board.field[self.coordinates[1]][self.coordinates[0]] = 1
        self.graphic.update_cells(self.board.field)


    def free_walk(self):
        for i in range(100):
            direction = random.choice(["left", "right", "up", "down"])
            self.walk(direction, 1)
            self.paint()


