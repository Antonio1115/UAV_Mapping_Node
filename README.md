# UAV Occupancy Grid Mapping

This project is a Python-based occupancy grid mapping system designed for autonomous drone navigation. The goal is to build a 2D occupancy grid for obstacle detection and path planning. The primary input is world-frame obstacle data, with an optional image-based pipeline for testing.

This project is being built with robotics competitions and real-world deployment in mind, so the focus is on clean architecture and realistic sensor processing.

## Features

**Occupancy Grid Mapping**  
Maintains a global 2D grid with three states: UNKNOWN, FREE, and OCCUPIED

**Flexible Obstacle Inputs**  
Accepts obstacle inputs as points, polygons, or bounding boxes in world coordinates

**ArUco Marker Input (Single Square)**  
Accepts one ArUco marker as a square detection with center, size, and optional yaw

**Optional Image Processing**  
HSV-based image pipeline for synthetic tests and legacy image inputs

**World Coordinate Mapping**  
Converts between real-world coordinates (meters) and grid indices

**Synthetic Field Generator**  
Generates realistic test images with obstacles, grass texture, and varied colors for simulation

**Visualization Tools**  
Color-coded grid output for debugging and analysis  
(gray = unknown, white = free, black = occupied)

## Requirements

```bash
pip install opencv-python numpy matplotlib
```

## Project Structure

```
uav-mapping/
├── occupancy_grid.py      # Global occupancy grid implementation
├── image_to_grid.py       # Image processing pipeline (HSV detection)
├── utils/
│   └── test_field.py      # Synthetic field generator
├── main.py                # Example usage / demo
├── images/                # Input images
└── .gitignore
```

## Usage

### Basic Example (Obstacle Inputs)

```python
from occupancy_grid import OccupancyGridMap
from image_to_grid import image_to_grid

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
    - In the current adapter, vertices are treated as obstacle points,
        then expanded by `radius_m`.

Note: `bbox` is fill-based. `polygon` is still treated as obstacle points.

### Image-Based Pipeline (Optional)

```python
from occupancy_grid import OccupancyGridMap
from image_to_grid import image_to_grid

grid = OccupancyGridMap(
    width_meters=20,
    height_meters=20,
    resolution=0.1,
    inflation_meters=0.5
)

local_grid = image_to_grid("images/field.png", (200, 200))
grid.update_from_local_grid(
    local_grid=local_grid,
    drone_x=0.0,
    drone_y=0.0
)

grid.visualize_grid()  # Saves to occupancy_grid.png
```

### Generate Synthetic Test Fields

Synthetic fields simulate a competition environment with obstacles like boxes and cones on grass.

```python
from utils.test_field import generate_field

generate_field(
    width_px=600,
    height_px=600,
    output_path="images/field.png"
)
```

## How It Works

### 1. Obstacle Inputs (World Frame)

When obstacles already come in world coordinates, the local image grid is optional.
The mapping node can update the global grid directly via `update_from_obstacles()`.

### 2. Image Processing Pipeline (Optional)

The image processing uses HSV color space to detect obstacles on green grass:

- Resize image to match grid dimensions
- Blur to reduce camera noise
- Convert to HSV color space (separates color from brightness)
- Detect green range to identify grass
- Invert to find non-green obstacles (any color)
- Apply light morphological operations to fill holes and remove noise
- Convert to grid values (FREE or OCCUPIED)

This approach is robust because it works with obstacles of any color, not just specific shades.

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

**0 (FREE)**  
Clear space, safe for navigation

**1 (OCCUPIED)**  
Obstacle detected (box, cone, etc.)

## Configuration

Key parameters can be adjusted in `main.py`:

- `width_meters`, `height_meters` - Size of the world in meters
- `resolution` - Cell size (smaller = more detail, more computation)
- `inflation_meters` - Safety margin around obstacles
- HSV green range in `image_to_grid.py` - Adjust for different lighting conditions
- `update_from_obstacles()` - Adapter for upstream obstacle formats

## License

Developed for SMU Drone Club

## Author

Antonio  
SMU Drone Club
