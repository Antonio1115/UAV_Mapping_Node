import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import math

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
    
    # This function is currently not being used, but will be kept in case I need it in the future
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

    
    def update_from_local_grid(self, local_grid, drone_x, drone_y):
        """
        Takes the local map created from the drones image and uses it to update
        the global grid map
        """

        center_row, center_col = self.world_to_grid(drone_x, drone_y)

        grid_height = len(local_grid)
        grid_width = len(local_grid[0])

        half_h = grid_height // 2
        half_w = grid_width // 2

        for i in range(grid_height):
            flipped_i = grid_height - 1 - i  # flip image rows because OpenCV origin is top-left
            for j in range(grid_width):

                value = local_grid[flipped_i][j]

                if value == self.UNKNOWN:
                    continue

                global_row = center_row + (i - half_h)
                global_col = center_col + (j - half_w)

                if 0 <= global_row < self.grid_height and 0 <= global_col < self.grid_width:
                    if self.grid[global_row][global_col] != self.OCCUPIED:
                        self.grid[global_row][global_col] = value


    def visualize_grid(self):
        cmap = mcolors.ListedColormap(['gray', 'white', 'black'])
        bounds = [-1.5, -0.5, 0.5, 1.5]
        norm = mcolors.BoundaryNorm(bounds, cmap.N)

        plt.imshow(self.grid, origin='lower', cmap=cmap, norm=norm)
        plt.title("Occupancy Grid")
        plt.xlabel("X (columns)")
        plt.ylabel("Y (rows)")
        
        cbar = plt.colorbar(ticks=[-1, 0, 1])
        cbar.ax.set_yticklabels(['UNKNOWN', 'FREE', 'OCCUPIED'])
        
        plt.savefig("occupancy_grid.png")
        plt.close()

            