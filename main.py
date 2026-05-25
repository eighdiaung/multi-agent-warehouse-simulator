import numpy as np
from warehouse import Warehouse
from robot import Robot
from planner import Planner
from simulate import plot_simulation

'''
classes and their responsibilities:
Warehouse
- handles the spatial representation of the warehouse
- grid
- obstacles
- pickups/dropoffs
- validity checks

Robot
- handles the state and actions of individual robots
- id
- position
- goal
- priority
- task status

Planner/Controller
- handles global coordination decision making whether it is a centralized planner or a decentralized controller
- asks robots for candidate moves
- sorts robots by priority
- assigns next positions
- prevents collisions
'''

## define warehouse dimensions and obstacle locations first before creating the warehouse object, so that we can use them to initialize the warehouse and add the obstacles to it. This way, we can ensure that the warehouse is set up correctly 
# before we start adding robots and other elements to it.
warehouse = Warehouse(10, 10)
obstacles = [(1, 1), (2, 3), (4, 5), (6, 7), (9, 5), (3,5)]
warehouse.add_obstacle(obstacles)

# create robots and add them to the warehouse
robot1 = Robot(robot_id="R1", start_position=(9, 1))
robot2 = Robot(robot_id="R2", start_position=(9, 9))
robot1.priority = 1 # switching order here really affects the dynamics
robot2.priority = 2

warehouse.add_robot(robot1)
warehouse.add_robot(robot2)

planner = Planner(warehouse)
planner.add_task(pickup=(0, 0), dropoff=(9, 9))
planner.add_task(pickup=(3, 2), dropoff=(7, 6))
planner.assign_tasks_to_robots(warehouse.robots)

reserved_positions = planner.get_reserved_positions(warehouse.robots)
print(reserved_positions)

for step in range(100):

    print(f"\n--- Step {step} ---")

    planner.step_all_robots()

    plot_simulation(warehouse, planner)

    robot1.display_status()
    robot2.display_status()

    print(planner.tasks)