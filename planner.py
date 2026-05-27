class Planner:
    def __init__(self, warehouse):
        self.warehouse = warehouse
        self.tasks = [] # this can be used to store the list of tasks that need to be completed in the warehouse

    def add_task(self, pickup, dropoff):
        task = {
            "pickup": pickup,
            "dropoff": dropoff,
            "assigned_robot": None, # this can be used to track which robot is assigned to the task
            "status": "pending" # this can be used to track the status of the task (e.g., pending, in progress, completed)
        }

        self.tasks.append(task)

    def assign_tasks_to_robots(self, robots):
        # This method can be expanded to implement a task assignment algorithm that assigns tasks to robots based on their current state and the task requirements
        
        for task in self.tasks:
            if task["status"] == "pending":
                for robot in robots:
                    if robot.current_task is None: # check if the robot is available to take on a new task
                        task["assigned_robot"] = robot.robot_id
                        task["status"] = "assigned"
                        robot.current_task = task
                        robot.set_goal(task["pickup"]) # set the robot's goal to the pickup location of the task

                        break # break out of the task assignment loop to move on to the next task after assigning the current task to a robot

    def update_task_progress(self, robot):
        task = robot.current_task

        if task is not None:
            if robot.position == task["pickup"] and task["status"] == "assigned":
                task["status"] = "picked_up"
                robot.set_goal(task["dropoff"]) # set the robot's goal to the dropoff location of the task
            
            elif robot.position == task["dropoff"] and task["status"] == "picked_up":
                task["status"] = "completed" # update task status to completed when the robot reaches the dropoff location
                robot.current_task = None # clear the robot's current task after completing it
    
    def get_reserved_positions(self,robots):
        reserved_positions = set()

        robots_by_priority = self.get_robots_by_priority(robots)

        for robot in robots_by_priority:
            best_move = self.choose_best_move(robot, reserved_positions)

            reserved_positions.add(best_move)

        return reserved_positions

    def get_robots_by_priority(self, robots):
        return sorted(
            robots,
            key=lambda r: r.priority, #sort by robot priority
            reverse = True # higher priority robots should be considered first when determining reserved positions
        )

    def get_robots(self):
        return self.warehouse.robots

    def get_candidate_moves(self, robot):
        return robot.get_candidate_moves()
    
    def get_valid_moves_for_robot(self, robot, reserved_positions=None):
        if reserved_positions is None:
            reserved_positions = set() # create a dummy empty set if no reserved positions exist yet, so that we can still perform the validity checks for the robot's candidate moves without running into errors due to a NoneType object when we try to check if a move is in the reserved positions.
        
        candidate_moves = robot.get_candidate_moves()

        valid_moves = []

        for move in candidate_moves:
            row, col = move

            if move in reserved_positions:
                continue

            try:
                self.warehouse.validate_free_cell(row, col, label="candidate move")
                valid_moves.append(move)
                
            except ValueError:
                continue

        return valid_moves

    def compute_manhattan_distance(self, position, goal):
        row, col = position
        goal_row, goal_col = goal

        return abs(row - goal_row) + abs(col - goal_col)
    
    def rank_candidate_moves(self, robot, reserved_positions=None):
        valid_moves = self.get_valid_moves_for_robot(robot, reserved_positions)

        # sort(...,key = ...), where the key is a function that takes an element from the computation and returns a value that will be used for sorting. 
        # In this case, we are using a lambda function that computes the Manhattan distance from each valid move to the robot's goal. 
        # The sorted function will then sort the valid moves based on their distance to the goal, with closer moves being ranked higher.
        #ranked_moves = sorted(valid_moves, key=lambda move: self.compute_manhattan_distance(move, robot.goal))

        ranked_moves = sorted(
            valid_moves,
            key=lambda move: (
                move == robot.previous_position,
                self.compute_manhattan_distance(move, robot.goal)
            )
        )

        return ranked_moves
    
    def choose_best_move(self, robot, reserved_positions=None):
        ranked_moves = self.rank_candidate_moves(robot, reserved_positions)

        return ranked_moves[0] # return the best move (the one with the lowest Manhattan distance to the goal)
    
    def step_robot_towards_goal(self, robot):
        if robot.position == robot.goal:
            print(f"Robot {robot.robot_id} has reached its goal at {robot.position}.")
            return False # return boolean to signal iterations to stop when the robot has reached its goal
        
        best_move = self.choose_best_move(robot)
        self.warehouse.move_robot(robot, best_move)

        return True # return boolean to signal iterations to continue until the robot has reached its goal

    def step_all_robots(self):

        reserved_positions = set()
        robots_by_priority = self.get_robots_by_priority(self.get_robots())

        for robot in robots_by_priority:

            # Check task state before movement
            self.update_task_progress(robot)

            if robot.goal is None: # if the robot has no goal, then there is no need to compute a move for it
                continue

            # Check again in case update_task_progress completed a task
            if robot.position == robot.goal:
                self.update_task_progress(robot)
                continue

            best_move = self.choose_best_move(robot, reserved_positions)
            reserved_positions.add(best_move)
            self.warehouse.move_robot(robot, best_move)
            self.update_task_progress(robot)
