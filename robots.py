import random

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.field = [[0 for _ in range(width)] for _ in range(height)]

class Robot:
    def __init__(self, speed, size, coordinates, board):
        self.speed = speed
        self.size = size
        self.coordinates = coordinates
        self.board = board
        self.local_map = [[0 for _ in range(board.width)] for _ in range(board.height)]
        self.update_local_map()

    def update_local_map(self):
        x, y = self.coordinates
        self.local_map[y][x] = 1

    def get_neighbors(self):
        """Возвращает список соседних клеток."""
        x, y = self.coordinates
        neighbors = [
            (x + dx, y + dy)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
            if 0 <= x + dx < self.board.width and 0 <= y + dy < self.board.height
        ]
        return neighbors

    def is_valid_move(self, direction):
        x, y = direction
        return self.board.field[y][x] == 0

    def walk(self, direction, steps):
        dx, dy = direction
        for _ in range(steps):
            if self.is_valid_move((dx, dy)):
                self.coordinates[0] = dx
                self.coordinates[1] = dy
                self.update_local_map()

    def paint(self):
        x, y = self.coordinates
        self.board.field[y][x] = 1

    def exchange_information(self, other_robot):
        """Merge local maps between robots."""
        for y in range(self.board.height):
            for x in range(self.board.width):
                self.local_map[y][x] = max(
                    self.local_map[y][x], other_robot.local_map[y][x]
                )

    def exchange_information_with_map(self, received_map):
        """Обновляет локальную карту на основе полученной карты от другого робота."""
        for y in range(self.board.height):
            for x in range(self.board.width):
                self.local_map[y][x] = max(self.local_map[y][x], received_map[y][x])

    def update_map(self, updated_map):
        """Обновляет локальную карту на основе полученной карты от другого робота."""
        for y in range(self.board.height):
            for x in range(self.board.width):
                self.local_map[y][x] = max(self.local_map[y][x], updated_map[y][x])

    def process_incoming_data(self, data):
        """Process incoming map data from another robot."""
        for y in range(len(data)):
            for x in range(len(data[y])):
                self.local_map[y][x] = max(self.local_map[y][x], data[y][x])

    def send_data(self):
        """Prepare local map data for transmission."""
        return self.local_map