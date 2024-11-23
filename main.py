import robots
import graphics
from dask.distributed import Client, as_completed
import threading
import queue
import time
import matplotlib.pyplot as plt
import random

board_width = 20
board_height = 20
graphic = graphics.Graphics(800, 800, 40)

update_queue = queue.Queue()
plot_queue = queue.Queue()

board = robots.Board(board_width, board_height)

obstacles = [(5, 5), (10, 10), (15, 15)]
for obstacle in obstacles:
    board.field[obstacle[1]][obstacle[0]] = 2

graphic.set_obstacles(obstacles)

robots_data = [
    {"speed": 1, "size": 1, "coordinates": [8, 3]},
    {"speed": 1, "size": 1, "coordinates": [8, 9]},
    {"speed": 1, "size": 1, "coordinates": [8, 16]},
    {"speed": 1, "size": 1, "coordinates": [12, 16]},
    {"speed": 1, "size": 1, "coordinates": [2, 16]},
    {"speed": 1, "size": 1, "coordinates": [7, 10]},
    {"speed": 1, "size": 1, "coordinates": [7, 20]},
    {"speed": 1, "size": 1, "coordinates": [13, 20]},
]

robots = [
    robots.Robot(data["speed"], data["size"], data["coordinates"], board)
    for data in robots_data
]

def free_walk_with_update(robot):
    direction = robot.random_direction()
    while not robot.is_valid_move(direction):
        direction = robot.random_direction()
    robot.walk(direction, 1)
    robot.paint()
    time.sleep(2)
    return robot.coordinates[0], robot.coordinates[1]

def run_robots(update_queue, plot_queue):
    client = Client()
    scattered_robots = client.scatter(robots)  # Распространение роботов

    futures = []
    try:
        while True:
            for robot in scattered_robots:
                future = client.submit(free_walk_with_update, robot)
                futures.append(future)

            for future in as_completed(futures):
                x, y = future.result()  # Обработка результата
                update_queue.put((x, y))  # Помещение координат в очередь

                # Добавление данных для графика
                plot_queue.put(
                    (time.time(), str(future))
                )  # Время и идентификатор задачи

            futures.clear()

            # Обмен информацией между роботами
            for i in range(len(robots)):
                for j in range(i + 1, len(robots)):
                    robots[i].exchange_information(robots[j])

            # Выбор лидера
            for robot in robots:
                robot.elect_leader(robots)

            # Консенсус
            for robot in robots:
                robot.consensus(robots)

            # Обнаружение столкновений
            for i in range(len(robots)):
                for j in range(i + 1, len(robots)):
                    robots[i].detect_collision(robots[j])

    except Exception as e:
        print(f"Error in run_robots: {e}")
    finally:
        update_queue.put(None)
        plot_queue.put(None)
        client.close()

def run_graphic_update(graphic, update_queue):
    try:
        while True:
            update = update_queue.get()
            if update is None:
                break
            x, y = update
            graphic.update_cells(x, y)
    except Exception as e:
        print(f"Error in run_graphic_update: {e}")

def update_plot(plot_queue):
    plt.ion()  # Включение интерактивного режима
    fig, ax = plt.subplots(figsize=(10, 6))
    while True:
        data = plot_queue.get()
        if data is None:
            break
        time_stamp, task_id = data
        ax.scatter(time_stamp, task_id, c="blue", s=10)
        ax.set_title("Dask Task Stream")
        ax.set_xlabel("Time")
        ax.set_ylabel("Task")
        plt.draw()
        plt.pause(0.1)
    plt.ioff()
    plt.show()

if __name__ == "__main__":
    robot_thread = threading.Thread(target=run_robots, args=(update_queue, plot_queue))
    robot_thread.daemon = True
    robot_thread.start()

    graphic_thread = threading.Thread(
        target=run_graphic_update, args=(graphic, update_queue)
    )
    graphic_thread.daemon = True
    graphic_thread.start()

    '''
    plot_thread = threading.Thread(target=update_plot, args=(plot_queue,))
    plot_thread.daemon = True
    plot_thread.start()
    '''

    try:
        graphic.root.mainloop()
    except KeyboardInterrupt:
        print("Program terminated by user")
    finally:
        update_queue.put(None)
        plot_queue.put(None)
        robot_thread.join()
        graphic_thread.join()