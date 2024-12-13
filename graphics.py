import tkinter as tk

class Graphics:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="white")
        self.canvas.pack()
        self.obstacles = []
        self.robot_markers = {}
        self.board_state = [[0 for _ in range(self.width // self.cell_size)] for _ in range(self.height // self.cell_size)]  # Состояние карты

    def draw_grid(self):
        """Рисует сетку на холсте."""
        for x in range(0, self.width, self.cell_size):
            self.canvas.create_line(x, 0, x, self.height, fill='black')
        for y in range(0, self.height, self.cell_size):
            self.canvas.create_line(0, y, self.width, y, fill='black')

    def set_obstacles(self, obstacles):
        """Устанавливает препятствия на карте."""
        self.obstacles = obstacles
        for x, y in obstacles:
            self._draw_cell(x, y, "black")

    def update_cells(self, x, y, color="blue"):
        """Обновляет клетки на холсте."""
        self.board_state[y][x] = 1
        self._draw_cell(x, y, color)

    def draw_robot(self, x, y, robot_id):
        """Рисует маркер робота на клетке."""
        x1 = x * self.cell_size
        y1 = y * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        marker = self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill="red")
        self.canvas.create_text(x1 + self.cell_size // 2, y1 + self.cell_size // 2, text=str(robot_id), fill="white")
        return marker

    def update_robot_position(self, robot_id, x, y):
        """Обновляет координаты робота на холсте."""
        if robot_id in self.robot_markers:
            self.canvas.coords(
                self.robot_markers[robot_id],
                x * self.cell_size + 5,
                y * self.cell_size + 5,
                (x + 1) * self.cell_size - 5,
                (y + 1) * self.cell_size - 5
            )
        else:
            self.robot_markers[robot_id] = self.draw_robot(x, y, robot_id)

    def refresh(self):
        """Обновляет все роботов и карту, вызывается через событие Tkinter."""
        self.canvas.update_idletasks()
        self.canvas.update()

    def _draw_cell(self, x, y, color):
        """Отображает клетку на экране."""
        x1 = x * self.cell_size
        y1 = y * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

    def mark_painted(self, painted_cells):
        """Закрашивает клетки на карте."""
        for x, y in painted_cells:
            if self.board_state[y][x] == 0:
                self.update_cells(x, y, "green")
                self.root.after(500, lambda x=x, y=y: self._draw_cell(x, y, "red"))

    def stop_cadre(self):
        """Запускает главный цикл Tkinter."""
        self.root.mainloop()