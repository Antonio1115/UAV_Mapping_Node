import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import math

class OccupancyGridMap:

    UNKNOWN = -1
    FREE = 0
    OCCUPIED = 1

    def __init__(self, width_meters, height_meters, resolution, inflation_meters):
        if resolution <= 0:
            raise ValueError("resolution must be > 0")
        if width_meters <= 0 or height_meters <= 0:
            raise ValueError("width_meters and height_meters must be > 0")

        self.width_meters = width_meters
        self.height_meters = height_meters
        self.inflation_meters = max(0.0, inflation_meters)
        self.resolution = resolution

        self.grid_width = math.ceil(self.width_meters / self.resolution)
        self.grid_height = math.ceil(self.height_meters / self.resolution)
        self.inflation_radius_cells = max(0, int(self.inflation_meters / self.resolution))

        self.grid = [
            [self.UNKNOWN for col in range(self.grid_width)]
            for row in range(self.grid_height)
            ]

    def world_to_grid(self, x, y):
        """
        Converts world coordinates into grid coordinates
        """

        row = math.floor((y + self.height_meters / 2) / self.resolution)
        col = math.floor((x + self.width_meters / 2) / self.resolution)

        return row, col

    def _inflate_occupied(self, center_row, center_col):
        if self.inflation_radius_cells <= 0:
            return

        radius = self.inflation_radius_cells
        for r in range(center_row - radius, center_row + radius + 1):
            if r < 0 or r >= self.grid_height:
                continue
            for c in range(center_col - radius, center_col + radius + 1):
                if c < 0 or c >= self.grid_width:
                    continue
                dr = r - center_row
                dc = c - center_col
                if dr * dr + dc * dc <= radius * radius:
                    self.grid[r][c] = self.OCCUPIED
    
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

        if not local_grid or not local_grid[0]:
            return

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
                    if value == self.OCCUPIED:
                        self.grid[global_row][global_col] = self.OCCUPIED
                        self._inflate_occupied(global_row, global_col)
                    elif self.grid[global_row][global_col] != self.OCCUPIED:
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

            