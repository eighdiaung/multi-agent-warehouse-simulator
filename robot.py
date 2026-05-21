class Robot:
    def __init__(self, robot_id, start_position, goal=None): # initialize the robot with an ID and a starting position
        self.robot_id = robot_id
        self.position = start_position
        self.goal = goal
        self.current_task = None # this can be used to store the current task assigned to the robot

    def __repr__(self): # representation of the robot for easy debugging and visualization
        return f"Robot(ID={self.robot_id}, Position={self.position})"

    def display_status(self):
        print(f"{self.robot_id} | position={self.position} | goal={self.goal} | current_task={self.current_task}")

    def move_to(self, new_position):
        self.position = new_position

    def set_goal(self, goal_position):
        self.goal = goal_position

    def get_candidate_moves(self):
        # This method can be expanded to return valid 
        # candidate moves based on the robot's current position and the warehouse layout
        row, col = self.position
        return [
            (row-1, col), # up 
            (row+1, col), # down
            (row, col-1), # left
            (row, col+1), # right
            (row, col)    # wait/stay
        ]