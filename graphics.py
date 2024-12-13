import tkinter as tk

class Graphics:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.root = tk.Tk()
        self.canvas = tk.Canvas(
            self.root, width=self.width, height=self.height, bg="white"
        )
        self.canvas.pack()
        self.obstacles = []

    def set_obstacles(self, obstacles):
        self.obstacles = obstacles
        for x, y in obstacles:
            self._draw_cell(x, y, "black")

    def update_cells(self, x, y, color="blue"):
        self._draw_cell(x, y, color)

    def draw_robot(self, x, y, robot_id):
        """Рисует маркер робота на клетке."""
        x1 = x * self.cell_size
        y1 = y * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        # Рисуем круг и текст с номером робота поверх закрашенной клетки
        marker = self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill="red")
        self.canvas.create_text(x1 + self.cell_size // 2, y1 + self.cell_size // 2, text=str(robot_id), fill="white")
        return marker

    def highlight_interaction(self, x1, y1, x2, y2):
        """Draw a line or marker to indicate interaction between robots."""
        x1_center = x1 * self.cell_size + self.cell_size // 2
        y1_center = y1 * self.cell_size + self.cell_size // 2
        x2_center = x2 * self.cell_size + self.cell_size // 2
        y2_center = y2 * self.cell_size + self.cell_size // 2
        self.canvas.create_line(
            x1_center, y1_center, x2_center, y2_center, fill="red", width=2
        )
        self.root.update()

    def _draw_cell(self, x, y, color):
        x1 = x * self.cell_size
        y1 = y * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
        self.root.update()