import tkinter as tk

def draw_grid(canvas, width, height, cell_size):
    for x in range(0, width, cell_size):
        canvas.create_line(x, 0, x, height, fill='black')
    for y in range(0, height, cell_size):
        canvas.create_line(0, y, width, y, fill='black')

def draw_cells(canvas, grid, cell_size):
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == 1:
                x1 = col * cell_size
                y1 = row * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                canvas.create_rectangle(x1, y1, x2, y2, fill='red', outline='')

def main():
    width = 750
    height = 750
    cell_size = 50 
    root = tk.Tk()
    root.title("Сетка 100x100")

    canvas = tk.Canvas(root, width=width, height=height, bg='white') 
    canvas.pack()

    draw_grid(canvas, width, height, cell_size)

    # Пример двумерного массива
    grid = [
        [0, 1, 0, 0, 1],
        [1, 0, 0, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 1, 0, 1, 1],
        [1, 0, 0, 0, 0]
    ]

    draw_cells(canvas, grid, cell_size)

    root.mainloop()

if __name__ == "__main__":
    main()


