import tkinter as tk


class Graphics:
    def __init__(self, width, height, cell_size, grid_data=[]):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        self.root = tk.Tk()
        self.root.title("Сетка 100x100")

        self.canvas = tk.Canvas(
            self.root, width=self.width, height=self.height, bg="white"
        )
        self.canvas.pack()

        self.grid_data = [
            [0] * (width // cell_size) for _ in range(height // cell_size)
        ]
        self.draw_grid()

    def draw_grid(self):
        for x in range(0, self.width, self.cell_size):
            self.canvas.create_line(x, 0, x, self.height, fill="black")
        for y in range(0, self.height, self.cell_size):
            self.canvas.create_line(0, y, self.width, y, fill="black")

    def draw_cells(self):
        for row in range(len(self.grid_data)):
            for col in range(len(self.grid_data[row])):
                if self.grid_data[row][col] == 1:
                    x1 = col * self.cell_size
                    y1 = row * self.cell_size
                    x2 = x1 + self.cell_size
                    y2 = y1 + self.cell_size
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2, fill="red", outline="", tags="cell"
                    )

    def update_cells(self, x, y):
        self.grid_data[y][x] = 1
        self.draw_cells()
        self.root.update()

    def stop_cadre(self):
        self.root.mainloop()
