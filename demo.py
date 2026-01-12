from occupancy_grid import OccupancyGridMap

def main():

    grid = OccupancyGridMap (
        width_meters = 20,
        height_meters = 20,
        resolution = .2,
        inflation_meters = .5
    )

    grid.add_obstacle(2.0, 1.0)
    grid.add_obstacle(-1.5, 3.0)
    grid.add_obstacle(0.0, -2.0)

    grid.mark_visible_area(
        drone_x = 0.0,
        drone_y = 0.0,
        drone_view_radius= 10
    )

    grid.visualize_grid()

if __name__ == "__main__":
    main()