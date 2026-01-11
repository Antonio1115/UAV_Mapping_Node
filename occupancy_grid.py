import matplotlib.pyplot as plt

class OccupancyGridMap:

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
            [self.FREE for col in range(self.grid_width)]
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

    def visualize_grid(self):
        plt.imshow(self.grid, origin = "lower")
        plt.title("Occupancy Grid")
        plt.xlabel("X (columns)")
        plt.ylabel("Y (rows)")
        plt.colorbar(label = "0 = FREE, 1 = OCCUPIED")
        plt.savefig("occupancy_grid.png")
        plt.close()

        