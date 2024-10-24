import robots

board = robots.Board(20, 20)
robot = robots.Robot(1,1, [10, 10], board)

robot.free_walk()
