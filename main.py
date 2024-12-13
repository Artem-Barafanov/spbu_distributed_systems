import tkinter as tk
import robots
import graphics
import zmq
import threading
import queue
import time
import random

board_width = 20
board_height = 20
cell_size = 40
graphic = graphics.Graphics(800, 800, cell_size)

update_queue = queue.Queue()

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

robot_ports = [5555, 5556, 5557, 5558, 5559, 5560, 5561, 5562]

gossip_interval = 2 # секунды

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
            print(f"Robot on port {port} received gossip and updated map")
        else:
            socket.send_json({'status': 'unknown task'})

def robot_client(target_ip, target_port, task):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://{target_ip}:{target_port}")
    socket.send_json(task)
    return socket.recv_json()

def robot_behavior(robot, port, robot_id):
    server_thread = threading.Thread(target=robot_server, args=(robot, port))
    server_thread.daemon = True
    server_thread.start()

    # Gossip
    def gossip():
        random_peer_port = random.choice([p for p in robot_ports if p != port])
        try:
            robot_client("127.0.0.1", random_peer_port, {"task": "gossip", "map": robot.local_map})
            print(f"Robot {robot_id} sent gossip to port {random_peer_port}")
        except Exception as e:
            print(f"Failed to send gossip to port {random_peer_port}: {e}")
        threading.Timer(gossip_interval, gossip).start()

    gossip()

    while True:
        neighbors = robot.get_neighbors()
        unpainted_neighbors = [neighbor for neighbor in neighbors if robot.board.field[neighbor[1]][neighbor[0]] == 0]

        if unpainted_neighbors:
            direction = random.choice(unpainted_neighbors)
        else:
            direction = random.choice(neighbors)

        robot.walk(direction, 1)
        robot.paint()
        update_queue.put((robot.coordinates[0], robot.coordinates[1], "robot", robot_id))

        time.sleep(0.5)

def run_graphic_update():
    robot_markers = {}

    while True:
        update = update_queue.get()
        if update is None:
            break
        x, y, tag, *extra = update
        if tag == "robot":
            robot_id = extra[0]
            if robot_id in robot_markers:
                graphic.canvas.delete(robot_markers[robot_id])
            robot_markers[robot_id] = graphic.draw_robot(x, y, robot_id)
            graphic.update_cells(x, y, color="blue")

if __name__ == "__main__":
    for i, robot in enumerate(robots_list):
        thread = threading.Thread(target=robot_behavior, args=(robot, robot_ports[i], i))
        thread.daemon = True
        thread.start()

    graphic_thread = threading.Thread(target=run_graphic_update)
    graphic_thread.daemon = True
    graphic_thread.start()

    try:
        graphic.root.mainloop()
    except KeyboardInterrupt:
        print("Program terminated by user")
    finally:
        update_queue.put(None)