from occupancy_grid import OccupancyGridMap
from image_to_grid import image_to_grid

def main():

    grid = OccupancyGridMap (
        width_meters = 20,
        height_meters = 20,
        resolution = .2,
        inflation_meters = .3
    )

    use_image_pipeline = False

    if use_image_pipeline:
        local_grid = image_to_grid("images/field.png", (100, 100))
        grid.update_from_local_grid(
            local_grid=local_grid,
            drone_x=0.0,
            drone_y=0.0
        )

    obstacles = [
        {"x": -1.5, "y": 2.0, "radius_m": 0.4},
        {"bbox": [-3.0, -1.0, -2.0, 0.5], "radius_m": 0.2},
        {"points": [(1.0, 1.0), (1.2, 1.1), (1.4, 1.05)]}
    ]
    grid.update_from_obstacles(obstacles)


    grid.visualize_grid()

if __name__ == "__main__":
    main()