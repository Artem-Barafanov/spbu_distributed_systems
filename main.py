import robots
import graphics


board = robots.Board(20, 20)
graphic = graphics.Graphics(800, 800, 40)
robot = robots.Robot(1,1, [10, 10], board, graphic)
robot.graphic.grid_data = robot.board.field


robot.free_walk()
robot.graphic.stop_cadre()