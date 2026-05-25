import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(6, 6))
plt.ion()

def plot_simulation(warehouse, planner):

    ax.clear()

    ax.set_xlim(0, warehouse.cols)
    ax.set_ylim(0, warehouse.rows)
    ax.set_xticks(range(warehouse.cols + 1))
    ax.set_yticks(range(warehouse.rows + 1))
    ax.grid(True)
    ax.set_aspect("equal")

    for row, col in warehouse.obstacles:
        ax.add_patch(
            plt.Rectangle(
                (col, warehouse.rows - row - 1),
                1,
                1,
                color="gray"
            )
        )

    for robot in warehouse.robots:
        row, col = robot.position
        ax.add_patch(
            plt.Rectangle(
                (col, warehouse.rows - row - 1),
                1,
                1,
                color="green"
            )
        )

        ax.text(
            col + 0.5,
            warehouse.rows - row - 0.5,
            robot.robot_id,
            ha="center",
            va="center",
            color="white",
            fontsize=10,
            fontweight="bold"
        )

    for task in planner.tasks:
        pickup_row, pickup_col = task["pickup"]
        dropoff_row, dropoff_col = task["dropoff"]

        ax.scatter(
            pickup_col + 0.5,
            warehouse.rows - pickup_row - 0.5,
            marker="x",
            color="red",
            s=500,
            linewidths=4,
            zorder=10
        )

        ax.scatter(
            dropoff_col + 0.5,
            warehouse.rows - dropoff_row - 0.5,
            marker="o",
            facecolors="none",
            edgecolors="black",
            s=500,
            linewidths=4,
            zorder=10
        )

    plt.title("Multi-Agent Warehouse Simulation")
    
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.tick_params(length=0)
    plt.pause(0.3)