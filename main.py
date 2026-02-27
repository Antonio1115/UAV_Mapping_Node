from occupancy_grid import OccupancyGridMap
from image_to_grid import image_to_grid

def main():

    grid = OccupancyGridMap (
        width_meters = 8,
        height_meters = 8,
        resolution = .2,
        inflation_meters = 0.0
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
        {"x": -1.0, "y": 1.2, "radius_m": 0.65},
        {"bbox": [-2.8, -1.6, -1.6, -0.2], "radius_m": 0.0},
        {"bbox": [1.0, 0.2, 2.2, 1.4], "radius_m": 0.0},
        {"x": 2.4, "y": -1.8, "radius_m": 0.45}
    ]
    grid.update_from_obstacles(obstacles)

    aruco_marker = {"x": -2.6, "y": 1.6, "size_m": 0.6, "yaw_rad": 0.0}

    grid.update_from_aruco_marker(aruco_marker)


    grid.visualize_grid()

if __name__ == "__main__":
    main()