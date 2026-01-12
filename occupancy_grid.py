import matplotlib.pyplot as plt

class OccupancyGridMap:

    UNKNOWN = -1
    FREE = 0
    OCCUPIED = 1

    def __init__(self, width_meters, height_meters, resolution, inflation_meters):
        self.width_meters = width_meters
        self.height_meters = height_meters
        self.inflation_meters = inflation_meters
        self.resolution = resolution

        self.grid_width = int(self.width_meters / self.resolution)
        self.grid_height = int(self.height_meters / self.resolution)
        self.inflation_radius_cells = int(self.inflation_meters / self.resolution)

        self.grid = [
            [self.UNKNOWN for col in range(self.grid_width)]
            for row in range(self.grid_height)
            ]

    def world_to_grid(self, x, y):
        """
        Converts world coordinates into grid coordinates
        """

        row = int((y + self.height_meters / 2) / self.resolution)
        col = int((x + self.width_meters / 2) / self.resolution)

        return row, col

    def inflate_obstacle(self, center_row, center_col):
        """
        Inflates the obstacles in a grid by taking the center position
        and marking surrounding cells as OCCUPIED as well
        """

        for dy in range(-self.inflation_radius_cells, self.inflation_radius_cells + 1):
            for dx in range(-self.inflation_radius_cells, self.inflation_radius_cells + 1):
                row = center_row + dy
                col = center_col + dx

                if 0 <= row < self.grid_height and 0 <= col < self.grid_width:
                    self.grid[row][col] = self.OCCUPIED

    def add_obstacle(self, x, y):
        """
        Takes real world coordinates and adds them as obstacles in a grid
        """

        row, col = self.world_to_grid(x,y)

        if 0 <= row < self.grid_height and 0 <= col < self.grid_width:
            self.inflate_obstacle(row, col)

    def is_line_of_sight_clear(self, start_row, start_col, end_row, end_col):
        """
        Takes starting a starting grid cell and an end grid cell to determine
        whether there is a clear line of sight between the two cells
        """

        dr = abs(end_row - start_row)
        dc = abs(end_col - start_col)

        error = dr - dc

        step_row = 1 if end_row > start_row else -1
        step_col = 1 if end_col > start_col else -1

        r, c = start_row, start_col

        while (r, c) != (end_row, end_col):
                
            if self.grid[r][c] == self.OCCUPIED:
                return False
            
            e2 = 2 * error

            if e2 > -dc:
                error -= dc
                r += step_row

            if e2 < dr:
                error += dr
                c += step_col

        if self.grid[end_row][end_col] == self.OCCUPIED:
            return False
        
        return True


    def mark_visible_area(self, drone_x, drone_y, drone_view_radius):
        """
        Marks visble area on the grid based of the drones inputs
        """

        center_row, center_col = self.world_to_grid(drone_x, drone_y)
        view_radius = int(drone_view_radius / self.resolution)


        for dy in range(-view_radius, view_radius + 1):
            for dx in range(-view_radius, view_radius + 1):
                row = center_row + dy
                col = center_col + dx

                if 0 <= row < self.grid_height and 0 <= col < self.grid_width:
                    distance = (dy**2 + dx**2)**.5

                    if distance <= view_radius:
                        if self.is_line_of_sight_clear(center_row, center_col, row, col):
                            if self.grid[row][col] != self.OCCUPIED:
                                self.grid[row][col] = self.FREE

    def visualize_grid(self):
        plt.imshow(self.grid, origin = "lower")
        plt.title("Occupancy Grid")
        plt.xlabel("X (columns)")
        plt.ylabel("Y (rows)")
        plt.colorbar(label = "-1 = UNKNOWN, 0 = FREE, 1 = OCCUPIED")
        plt.savefig("occupancy_grid.png")
        plt.close()

        