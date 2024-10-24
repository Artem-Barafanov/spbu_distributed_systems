import tkinter as tk


class Graphics:
    def __init__(self, width, height, cell_size, grid_data=[]):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Инициализация главного окна
        self.root = tk.Tk()
        self.root.title("Сетка 100x100")

        # Создание холста
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg='white')
        self.canvas.pack()

        # Рисование сетки и инициализация пустого двумерного массива
        self.grid_data = []
        self.draw_grid()

    def draw_grid(self):
        # Отрисовка сетки
        for x in range(0, self.width, self.cell_size):
            self.canvas.create_line(x, 0, x, self.height, fill='black')
        for y in range(0, self.height, self.cell_size):
            self.canvas.create_line(0, y, self.width, y, fill='black')

    def draw_cells(self, grid):
        # Отрисовка закрашенных ячеек
        self.canvas.delete('cell')  # Удаляем старые ячейки
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                if grid[row][col] == 1:
                    x1 = col * self.cell_size
                    y1 = row * self.cell_size
                    x2 = x1 + self.cell_size
                    y2 = y1 + self.cell_size
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='red', outline='', tags='cell')

    def update_cells(self, new_grid):
        # Обновление состояния ячеек
        self.grid_data = new_grid
        self.draw_cells(self.grid_data)
        self.root.after(1000)
        self.root.update()

    def stop_cadre(self):
        # Запуск главного цикла
        self.root.mainloop()


