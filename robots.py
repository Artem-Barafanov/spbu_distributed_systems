import random


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        board = []
        for i in range(height):
            board.append([0]*width)
        self.field = board


class Robot:
    def __init__(self, speed: int, size: int, coordinates: list[int], board: Board):
        self.speed: int = speed
        self.size: int = size
        self.coordinates: list[int] = coordinates
        self.board = board

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

    def free_walk(self):
        for i in range(10):
            direction = random.choice(["left", "right", "up", "down"])
            self.walk(direction, 1)
            self.paint()


