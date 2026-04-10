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