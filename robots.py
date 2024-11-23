import random
import time
import heapq

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
        self.local_map = [[0] * board.width for _ in range(board.height)]
        self.leader = None

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
        self.local_map[self.coordinates[1]][self.coordinates[0]] = 1
        print(
            f"Robot painted cell at ({self.coordinates[0]}, {self.coordinates[1]})"
        ) 

    def random_direction(self):
        return random.choice(["left", "right", "up", "down"])

    def is_valid_move(self, direction):
        x, y = self.coordinates
        match direction:
            case "left":
                x -= 1
            case "right":
                x += 1
            case "up":
                y -= 1
            case "down":
                y += 1
        return 0 <= x < self.board.width and 0 <= y < self.board.height and self.board.field[y][x] == 0

    def obstacle_avoidance(self, target):
        # Реализация алгоритма A* для обхода препятствий
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        start = tuple(self.coordinates)
        goal = tuple(target)
        frontier = []
        heapq.heappush(frontier, (0, start))
        came_from = {start: None}
        cost_so_far = {start: 0}

        while frontier:
            _, current = heapq.heappop(frontier)

            if current == goal:
                break

            for next in self.neighbors(current):
                new_cost = cost_so_far[current] + 1
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + heuristic(goal, next)
                    heapq.heappush(frontier, (priority, next))
                    came_from[next] = current

        path = []
        current = goal
        while current != start:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path

    def neighbors(self, pos):
        x, y = pos
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results

    def in_bounds(self, pos):
        x, y = pos
        return 0 <= x < self.board.width and 0 <= y < self.board.height

    def passable(self, pos):
        x, y = pos
        return self.board.field[y][x] == 0 or self.board.field[y][x] == 1

    def exchange_information(self, other_robot):
        # Обмен информацией о местоположении и локальной карте
        self.local_map = self.merge_maps(self.local_map, other_robot.local_map)
        other_robot.local_map = self.merge_maps(other_robot.local_map, self.local_map)

    def merge_maps(self, map1, map2):
        merged_map = [row[:] for row in map1]
        for y in range(len(map2)):
            for x in range(len(map2[y])):
                if map2[y][x] == 1:
                    merged_map[y][x] = 1
        return merged_map

    def elect_leader(self, robots):
        self.leader = min(robots, key=lambda r: r.coordinates[0] + r.coordinates[1])

    def consensus(self, robots):
        for robot in robots:
            robot.local_map = self.leader.local_map
    
    def detect_collision(self, other_robot):
        # Обнаружение столкновений и изменение маршрута
        if abs(self.coordinates[0] - other_robot.coordinates[0]) < 2 and abs(self.coordinates[1] - other_robot.coordinates[1]) < 2:
            self.coordinates[0] += random.choice([-1, 1])
            self.coordinates[1] += random.choice([-1, 1])
            other_robot.coordinates[0] += random.choice([-1, 1])
            other_robot.coordinates[1] += random.choice([-1, 1])
    