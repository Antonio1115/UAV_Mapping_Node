from occupancy_grid import OccupancyGridMap

def main():

    grid = OccupancyGridMap (
        width_meters = 20,
        height_meters = 20,
        resolution = .2,
        inflation_meters = .5
    )

    local_grid = [
    [-1, -1,  1,  1,  1, -1, -1],
    [-1,  0,  0,  0,  0,  0, -1],
    [ 1,  0,  0,  0,  0,  0,  1],
    [ 1,  0,  0,  0,  0,  0,  1],
    [ 1,  0,  0,  0,  0,  0,  1],
    [-1,  0,  0,  0,  0,  0, -1],
    [-1, -1,  1,  1,  1, -1, -1],
    ]

    grid.update_from_local_grid(
    local_grid=local_grid,
    drone_x=0.0,
    drone_y=0.0
    )
    

    grid.visualize_grid()

if __name__ == "__main__":
    main()