from occupancy_grid import OccupancyGridMap
from image_to_grid import image_to_grid

def main():

    grid = OccupancyGridMap (
        width_meters = 20,
        height_meters = 20,
        resolution = .2,
        inflation_meters = .5
    )

    local_grid = image_to_grid("images/black_and_white_maze.png", (100,100))

    grid.update_from_local_grid(
    local_grid=local_grid,
    drone_x=0.0,
    drone_y=0.0
    )


    grid.visualize_grid()

if __name__ == "__main__":
    main()