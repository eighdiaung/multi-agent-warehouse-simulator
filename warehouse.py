import numpy as np
import robot

EMPTY = 0
OBSTACLE = 1
PICKUP = 2
DROPOFF = 3
ROBOT = 4

class Warehouse:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = np.full((rows, cols), EMPTY,dtype=int)
        self.robots = []
        self.obstacles = []

    def add_robot(self, robot):
        row, col = robot.position
        self.validate_free_cell(row, col, label="robot")
        self.robots.append(robot)

    def add_obstacle(self, obstacle_positions):
        for row, col in obstacle_positions:
            self.grid[row, col] = OBSTACLE
            self.obstacles.append((row, col))

    def add_pickup(self, pickup_positions):
        for row, col in pickup_positions:
            self.validate_free_cell(row, col, label="pickup")
            self.grid[row, col] = PICKUP

    def add_dropoff(self, dropoff_positions):
        for row, col in dropoff_positions:
            self.validate_free_cell(row, col, label="dropoff")
            self.grid[row, col] = DROPOFF

    def display(self):
        display_grid = self.grid.copy() # we are copying the static grid to a new variable so that we can
        #add the robots to it without modifying the original grid

        # the robots are dynamic and can move, so we need to add them to the display grid separately
        for robot in self.robots:
            row, col = robot.position
            display_grid[row, col] = ROBOT

        print(display_grid)


    # robot movement dynamics
    # movement validation checks are performed in the warehouse class because the warehouse has the knowledge 
    # of the grid and can check for obstacles and boundaries, 
    # while the robot class is more focused on the robot's state and actions. 
    # This separation of concerns allows for better organization and maintainability of the code.
    def move_robot(self, robot, new_position):

        row, col = new_position
        
        self.validate_free_cell(row, col, label="movement")

        # Update robot position
        robot.move_to(new_position)

    # spatial violation checks
    def is_within_bounds(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols
    
    def is_obstacle(self, row, col):
        return self.grid[row, col] == OBSTACLE
    
    def validate_free_cell(self, row, col, label="position"):

        if not self.is_within_bounds(row, col):
            raise ValueError(f"Invalid {label} at {(row, col)}: out of bounds.")

        if self.is_obstacle(row, col):
            raise ValueError(f"Invalid {label} at {(row, col)}: position is occupied by an obstacle.")
        

    