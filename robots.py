import random
import time


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.field = [[0] * width for _ in range(height)]

    def __len__(self):
        return len(self.field)


class Robot:
    def __init__(self, speed: int, size: int, coordinates: list[int], board: Board):
        self.speed: int = speed
        self.size: int = size
        self.coordinates: list[int] = coordinates
        self.board = board

    def walk(self, direction: str, distance: int):
        print(direction)
        match direction:
            case "left":
                self.coordinates[0] -= distance
            case "right":
                self.coordinates[0] += distance
            case "up":
                self.coordinates[1] -= distance
            case "down":
                self.coordinates[1] += distance

        # Проверка, чтобы робот не выходил за пределы доски
        self.coordinates[0] = max(0, min(self.coordinates[0], self.board.width - 1))
        self.coordinates[1] = max(0, min(self.coordinates[1], self.board.height - 1))

    def paint(self):
        self.board.field[self.coordinates[1]][self.coordinates[0]] = 1
        print(
            f"Robot painted cell at ({self.coordinates[0]}, {self.coordinates[1]})"
        )  # Отладочный вывод

    def random_direction(self):
        return random.choice(["left", "right", "up", "down"])
