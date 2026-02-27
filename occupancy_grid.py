import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import math

class OccupancyGridMap:

    UNKNOWN = -1
    FREE = 0
    OCCUPIED = 1
    MARKER = 2

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
        self.marker_layer = [
            [False for col in range(self.grid_width)]
            for row in range(self.grid_height)
        ]
        self.aruco_marker = None

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

    def _mark_occupied_with_radius(self, center_row, center_col, radius_cells):
        if radius_cells <= 0:
            if 0 <= center_row < self.grid_height and 0 <= center_col < self.grid_width:
                self.grid[center_row][center_col] = self.OCCUPIED
                self._inflate_occupied(center_row, center_col)
            return

        for r in range(center_row - radius_cells, center_row + radius_cells + 1):
            if r < 0 or r >= self.grid_height:
                continue
            for c in range(center_col - radius_cells, center_col + radius_cells + 1):
                if c < 0 or c >= self.grid_width:
                    continue
                dr = r - center_row
                dc = c - center_col
                if dr * dr + dc * dc <= radius_cells * radius_cells:
                    self.grid[r][c] = self.OCCUPIED
                    self._inflate_occupied(r, c)

    def _cell_center_world(self, row, col):
        x = (col + 0.5) * self.resolution - (self.width_meters / 2)
        y = (row + 0.5) * self.resolution - (self.height_meters / 2)
        return x, y

    def _point_in_polygon(self, x, y, polygon):
        inside = False
        n = len(polygon)
        j = n - 1

        for i in range(n):
            xi, yi = polygon[i]
            xj, yj = polygon[j]

            intersects = ((yi > y) != (yj > y)) and (
                x < (xj - xi) * (y - yi) / (yj - yi + 1e-12) + xi
            )
            if intersects:
                inside = not inside

            j = i

        return inside

    def _mark_polygon_occupied(self, polygon):
        if len(polygon) < 3:
            return

        min_x = min(point[0] for point in polygon)
        max_x = max(point[0] for point in polygon)
        min_y = min(point[1] for point in polygon)
        max_y = max(point[1] for point in polygon)

        min_row, min_col = self.world_to_grid(min_x, min_y)
        max_row, max_col = self.world_to_grid(max_x, max_y)

        row_start = max(0, min(min_row, max_row) - 1)
        row_end = min(self.grid_height - 1, max(min_row, max_row) + 1)
        col_start = max(0, min(min_col, max_col) - 1)
        col_end = min(self.grid_width - 1, max(min_col, max_col) + 1)

        for row in range(row_start, row_end + 1):
            for col in range(col_start, col_end + 1):
                x, y = self._cell_center_world(row, col)
                if self._point_in_polygon(x, y, polygon):
                    self.grid[row][col] = self.OCCUPIED
                    self._inflate_occupied(row, col)

    def _clear_marker_layer(self):
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                self.marker_layer[row][col] = False

    def _mark_polygon_marker(self, polygon):
        if len(polygon) < 3:
            return

        min_x = min(point[0] for point in polygon)
        max_x = max(point[0] for point in polygon)
        min_y = min(point[1] for point in polygon)
        max_y = max(point[1] for point in polygon)

        min_row, min_col = self.world_to_grid(min_x, min_y)
        max_row, max_col = self.world_to_grid(max_x, max_y)

        row_start = max(0, min(min_row, max_row) - 1)
        row_end = min(self.grid_height - 1, max(min_row, max_row) + 1)
        col_start = max(0, min(min_col, max_col) - 1)
        col_end = min(self.grid_width - 1, max(min_col, max_col) + 1)

        for row in range(row_start, row_end + 1):
            for col in range(col_start, col_end + 1):
                x, y = self._cell_center_world(row, col)
                if self._point_in_polygon(x, y, polygon):
                    self.marker_layer[row][col] = True
    
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

        # Optional path for image-space pipelines; world-frame inputs can update
        # the global grid directly via update_from_obstacles().

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

    def add_obstacle_points(self, points, radius_m=0.0):
        """
        Marks obstacle points in world coordinates as occupied.
        Optional radius_m expands each point into a filled circle.
        """

        if not points:
            return

        radius_cells = max(0, int(radius_m / self.resolution))

        for x, y in points:
            row, col = self.world_to_grid(x, y)
            self._mark_occupied_with_radius(row, col, radius_cells)

    def _mark_bbox_occupied(self, xmin, ymin, xmax, ymax, padding_m=0.0):
        xmin, xmax = sorted((xmin, xmax))
        ymin, ymax = sorted((ymin, ymax))

        pad = max(0.0, padding_m)
        xmin -= pad
        xmax += pad
        ymin -= pad
        ymax += pad

        min_row, min_col = self.world_to_grid(xmin, ymin)
        max_row, max_col = self.world_to_grid(xmax, ymax)

        row_start = max(0, min(min_row, max_row) - 1)
        row_end = min(self.grid_height - 1, max(min_row, max_row) + 1)
        col_start = max(0, min(min_col, max_col) - 1)
        col_end = min(self.grid_width - 1, max(min_col, max_col) + 1)

        for row in range(row_start, row_end + 1):
            for col in range(col_start, col_end + 1):
                x, y = self._cell_center_world(row, col)
                if xmin <= x <= xmax and ymin <= y <= ymax:
                    self.grid[row][col] = self.OCCUPIED
                    self._inflate_occupied(row, col)

    def update_from_obstacles(self, obstacles, default_radius_m=0.0):
        """
        Flexible adapter for upstream obstacle outputs.
        Supported obstacle fields (best-effort):
        - points: list of (x, y)
        - polygon: list of (x, y)
        - bbox: dict or list [xmin, ymin, xmax, ymax]
        - x, y: single point
        """

        if not obstacles:
            return

        for obstacle in obstacles:
            points = []
            radius_m = default_radius_m

            if isinstance(obstacle, dict):
                if "radius_m" in obstacle:
                    radius_m = obstacle["radius_m"]

                if "points" in obstacle:
                    points = obstacle["points"]
                elif "polygon" in obstacle:
                    points = obstacle["polygon"]
                elif "bbox" in obstacle:
                    bbox = obstacle["bbox"]
                    if isinstance(bbox, dict):
                        xmin = bbox.get("xmin")
                        ymin = bbox.get("ymin")
                        xmax = bbox.get("xmax")
                        ymax = bbox.get("ymax")
                    else:
                        if len(bbox) == 4:
                            xmin, ymin, xmax, ymax = bbox
                        else:
                            xmin = ymin = xmax = ymax = None

                    if xmin is not None:
                        self._mark_bbox_occupied(xmin, ymin, xmax, ymax, padding_m=radius_m)
                        continue
                elif "x" in obstacle and "y" in obstacle:
                    points = [(obstacle["x"], obstacle["y"])]

            if points:
                self.add_obstacle_points(points, radius_m=radius_m)

    def add_aruco_marker(self, center_x, center_y, size_m, yaw_rad=0.0):
        """
        Adds/updates ArUco marker input.
        Marker is modeled as a square in world coordinates.
        """

        if size_m <= 0:
            raise ValueError("size_m must be > 0")

        half = size_m / 2.0
        cos_yaw = math.cos(yaw_rad)
        sin_yaw = math.sin(yaw_rad)

        local_corners = [
            (-half, -half),
            (half, -half),
            (half, half),
            (-half, half),
        ]

        world_corners = []
        for x_local, y_local in local_corners:
            x_world = center_x + (x_local * cos_yaw - y_local * sin_yaw)
            y_world = center_y + (x_local * sin_yaw + y_local * cos_yaw)
            world_corners.append((x_world, y_world))

        self.aruco_marker = {
            "center": (center_x, center_y),
            "size_m": size_m,
            "yaw_rad": yaw_rad,
            "corners": world_corners,
        }

        self._clear_marker_layer()
        self._mark_polygon_marker(world_corners)

    def update_from_aruco_marker(self, marker):
        """
        ArUco marker input.
        Expected keys: x, y, size_m, optional yaw_rad.
        """

        if not marker:
            self.aruco_marker = None
            self._clear_marker_layer()
            return

        center_x = marker.get("x")
        center_y = marker.get("y")
        size_m = marker.get("size_m")
        yaw_rad = marker.get("yaw_rad", 0.0)

        if center_x is None or center_y is None or size_m is None:
            return

        self.add_aruco_marker(
            center_x=center_x,
            center_y=center_y,
            size_m=size_m,
            yaw_rad=yaw_rad,
        )

    def visualize_grid(self):
        display_grid = [row[:] for row in self.grid]
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                if self.marker_layer[row][col]:
                    display_grid[row][col] = self.MARKER

        cmap = mcolors.ListedColormap(['gray', 'white', 'black', 'green'])
        bounds = [-1.5, -0.5, 0.5, 1.5, 2.5]
        norm = mcolors.BoundaryNorm(bounds, cmap.N)

        plt.imshow(display_grid, origin='lower', cmap=cmap, norm=norm)
        plt.title("Occupancy Grid")
        plt.xlabel("X (columns)")
        plt.ylabel("Y (rows)")
        
        cbar = plt.colorbar(ticks=[-1, 0, 1, 2])
        cbar.ax.set_yticklabels(['UNKNOWN', 'FREE', 'OCCUPIED', 'ARUCO'])
        
        plt.savefig("occupancy_grid.png")
        plt.close()

            