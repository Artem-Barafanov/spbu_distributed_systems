import robots
import graphics
import zmq
import threading
import queue
import time
import random
import tkinter as tk

board_width = 20
board_height = 20
cell_size = 40
graphic = graphics.Graphics(800, 800, cell_size)

update_queue = queue.Queue()
message_queue = queue.Queue()

board = robots.Board(board_width, board_height)

obstacles = [(random.randint(0, board_width - 1), random.randint(0, board_height - 1)) for _ in range(10)]
for obstacle in obstacles:
    board.field[obstacle[1]][obstacle[0]] = 2

graphic.set_obstacles(obstacles)

robots_data = [
    {"speed": 1, "size": 1, "coordinates": [random.randint(0, board_width - 1), random.randint(0, board_height - 1)]}
    for _ in range(8)
]

robots_list = [
    robots.Robot(data["speed"], data["size"], data["coordinates"], board)
    for data in robots_data
]

robot_ports = [5555, 5563, 5557, 5558, 5559, 5560, 5561, 5562]

gossip_interval = 2  # секунды

def robot_server(robot, port):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://*:{port}")

    while True:
        message = socket.recv_json()
        task = message['task']
        if task == "exchange_map":
            received_map = message['map']
            robot.exchange_information_with_map(received_map)
            socket.send_json({'status': 'success', 'updated_map': robot.local_map})
        elif task == "gossip":
            received_map = message['map']
            robot.update_map(received_map)
            socket.send_json({'status': 'success'})
            log_message(f"Robot on port {port} received gossip and updated map")
        else:
            socket.send_json({'status': 'unknown task'})

def robot_client(target_ip, target_port, task):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://{target_ip}:{target_port}")
    socket.send_json(task)
    return socket.recv_json()

def robot_behavior(robot, port, robot_id):
    """
    Управляет поведением робота, обновляет его координаты и передает их для отображения.
    """
    server_thread = threading.Thread(target=robot_server, args=(robot, port))
    server_thread.daemon = True
    server_thread.start()

    def gossip():
        random_peer_port = random.choice([p for p in robot_ports if p != port])
        try:
            robot_client("127.0.0.1", random_peer_port, {"task": "gossip", "map": robot.local_map})
            log_message(f"Robot {robot_id} sent gossip to port {random_peer_port}")
        except Exception as e:
            log_message(f"Failed to send gossip to port {random_peer_port}: {e}")
        threading.Timer(gossip_interval, gossip).start()

    gossip()

    while True:
        neighbors = robot.get_neighbors()
        unpainted_neighbors = [neighbor for neighbor in neighbors if robot.board.field[neighbor[1]][neighbor[0]] == 0]

        try:
            direction = random.choice(unpainted_neighbors)
        except IndexError:
            direction = random.choice(neighbors)

        robot.walk(direction, 1)
        robot.paint()

        x, y = robot.coordinates
        update_queue.put((x, y, "robot", robot_id))

        time.sleep(0.5)

def run_graphic_update():
    def update_robots():
        for robot_id, coordinates in robot_positions.items():
            x, y = coordinates
            graphic.update_robot_position(robot_id, x, y)

        painted_cells = []
        for y in range(board_height):
            for x in range(board_width):
                if board.field[y][x] == 1:
                    painted_cells.append((x, y))

        graphic.mark_painted(painted_cells)
        graphic.refresh()

    robot_positions = {}

    def get_updates():
        while True:
            update = update_queue.get()
            if update is None:
                break
            x, y, tag, robot_id = update
            robot_positions[robot_id] = (x, y)
            graphic.root.after(0, update_robots)

    threading.Thread(target=get_updates, daemon=True).start()

def update_message_window():
    message_window = tk.Toplevel(graphic.root)
    message_window.title("Messages")
    message_text = tk.Text(message_window, wrap=tk.WORD, width=50, height=20)
    message_text.pack()

    def get_messages():
        while True:
            message = message_queue.get()
            if message is None:
                break
            message_text.insert(tk.END, message + "\n")
            message_text.see(tk.END)

    threading.Thread(target=get_messages, daemon=True).start()

def log_message(message):
    message_queue.put(message)

if __name__ == "__main__":
    for i, robot in enumerate(robots_list):
        thread = threading.Thread(target=robot_behavior, args=(robot, robot_ports[i], i))
        thread.daemon = True
        thread.start()

    graphic_thread = threading.Thread(target=run_graphic_update)
    graphic_thread.daemon = True
    graphic_thread.start()

    update_message_window()

    try:
        graphic.root.mainloop()
    except KeyboardInterrupt:
        print("Program terminated by user")
    finally:
        update_queue.put(None)
        message_queue.put(None)