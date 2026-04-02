# UAV Occupancy Grid Mapping

This project is a Python-based occupancy grid mapping system designed for autonomous drone navigation. The goal is to build a 2D occupancy grid for obstacle detection and path planning. The primary input is world-frame obstacle data.

## Features

**Occupancy Grid Mapping**  
Maintains a global 2D grid with three states: UNKNOWN, FREE, and OCCUPIED

**Flexible Obstacle Inputs**  
Accepts obstacle inputs as points, polygons, or bounding boxes in world coordinates

**ArUco Marker Input**  
Accepts one ArUco marker as a square detection with center, size, and optional yaw

**World Coordinate Mapping**  
Converts between real-world coordinates (meters) and grid indices

**Visualization Tools**  
Color-coded grid output for debugging and analysis  
(gray = unknown, white = free, black = occupied)

## Requirements

```bash
pip install matplotlib
```

## Project Structure

```
uav-mapping/
├── package.xml                # ROS 2 package manifest
├── setup.py                   # Package setup configuration
├── setup.cfg                  # Installation configuration
├── resource/
│   └── uav_mapping            # Package marker file
├── uav_mapping/
│   ├── __init__.py
│   ├── uav_mapping.py         # Main ROS 2 node
│   └── occupancy_grid.py      # Occupancy grid implementation
├── test/
│   ├── test_copyright.py
│   ├── test_flake8.py
│   └── test_pep257.py
├── README.md
└── images/                    # Input images
```

## Usage

### Basic Example (Obstacle Inputs)

```python
from occupancy_grid import OccupancyGridMap

# Create an 8x8 meter grid with 0.2m resolution
grid = OccupancyGridMap(
    width_meters=8,
    height_meters=8,
    resolution=0.2,
    inflation_meters=0.0
)

obstacles = [
    # Type 1: center-point obstacle with circular footprint
    # (x, y are world-frame meters, radius_m controls footprint size)
    {"x": -1.0, "y": 1.2, "radius_m": 0.65},

    # Type 2: bounding box input [xmin, ymin, xmax, ymax]
    # Current adapter samples box corners + center as obstacle points,
    # then applies radius_m around each sampled point.
    {"bbox": [-2.8, -1.6, -1.6, -0.2], "radius_m": 0.0},

    # Another bbox obstacle
    {"bbox": [1.0, 0.2, 2.2, 1.4], "radius_m": 0.0},

    # Type 3: explicit obstacle points (useful for clusters from sensors)
    # Each point gets a circular footprint of radius_m.
    {"points": [(0.6, -1.4), (0.9, -1.1), (1.2, -1.3)], "radius_m": 0.25},

    # Another center-point obstacle
    {"x": 2.4, "y": -1.8, "radius_m": 0.45}
]
grid.update_from_obstacles(obstacles)

aruco_marker = {"x": -2.6, "y": 1.6, "size_m": 0.6, "yaw_rad": 0.0}
grid.update_from_aruco_marker(aruco_marker)

# ArUco marker parameters
# x: marker center X in world coordinates (meters)
# y: marker center Y in world coordinates (meters)
# size_m: physical side length of the square marker (meters)
# yaw_rad: marker rotation in radians in the world frame (0.0 = axis-aligned)

# Visualize and save the result
grid.visualize_grid()  # Saves to occupancy_grid.png
```

### Obstacle Input Types (World Frame)

All obstacle coordinates are in meters in the map/world frame.

- `{"x": x, "y": y, "radius_m": r}`
    - Single obstacle center point.
    - Marks one point, expanded by `radius_m` (circle footprint).

- `{"points": [(x1, y1), (x2, y2), ...], "radius_m": r}`
    - Explicit list of obstacle points.
    - Each point is marked and expanded by `radius_m`.

- `{"bbox": [xmin, ymin, xmax, ymax], "radius_m": r}`
    - Axis-aligned rectangle input format.
    - Filled as a true rectangle in the grid.
    - `radius_m` expands the rectangle outward before filling.

- `{"polygon": [(x1, y1), (x2, y2), ...], "radius_m": r}`
    - Polygon vertices input format.
    - Vertices are treated as obstacle points, then expanded by `radius_m`.

Note: `bbox` is fill-based. `polygon` is treated as obstacle points.

## How It Works

### 1. Obstacle Inputs (World Frame)

When obstacles already come in world coordinates, the local image grid is optional.
The mapping node can update the global grid directly via `update_from_obstacles()`.

### 2. Image Processing Pipeline (Optional)

This path is mainly for testing and demos.
The mian approach is direct world-frame obstacle inputs via `update_from_obstacles()`.

### 3. Coordinate Transformation

- Converts world coordinates (meters) to grid indices
- Handles differences between image origins and grid coordinates
- Keeps the global map consistent as observations update it
- Flips image rows to align with standard coordinate frame

### 4. Map Integration

- Local grids from the drone camera are projected into the global map
- Unknown cells are updated as new observations are made
- Occupied cells are preserved once detected (safety priority)
- Supports multiple observations over time

### 5. ArUco Marker Integration

- Use `update_from_aruco_marker()` with `x`, `y`, `size_m`, and optional `yaw_rad`
- `x`, `y`: marker center in world coordinates (meters)
- `size_m`: physical side length of the square marker in meters
- `yaw_rad`: in-plane rotation in radians (`0` means no rotation)
- Marker is modeled as a square in world coordinates
- Marker metadata is stored in `grid.aruco_marker`
- Marker is shown in green on the visualization
- Marker is always treated as a reference landmark (not an occupied obstacle)

## Occupancy Grid States

**-1 (UNKNOWN)**  
Area has not been observed yet

*orld-frame obstacle data is processed directly via `update_from_obstacles()` method.

### 2. Coordinate Transformation

- Converts world coordinates (meters) to grid indices
- Keeps the global map consistent as observations update it

### 3. Map Integration

- Obstacles are marked on the grid based on world-frame inputs
- Unknown cells are updated as new observations are made
- Occupied cells are preserved once detected (safety priority)
- Supports multiple observations over time

### 4io  
SMU Drone Club
