# UAV Occupancy Grid Mapping

This project is a Python-based occupancy grid mapping system designed for autonomous drone navigation. The goal is to take a top-down camera image from a drone and convert it into a 2D occupancy grid that can be used for obstacle detection and path planning.

This project is being built with robotics competitions and real-world deployment in mind, so the focus is on clean architecture and realistic sensor processing.

## Features

**Occupancy Grid Mapping**  
Maintains a global 2D grid with three states: UNKNOWN, FREE, and OCCUPIED

**HSV-Based Image Processing**  
Uses OpenCV HSV color space to detect non-green obstacles on grass fields

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

### Basic Example

```python
from occupancy_grid import OccupancyGridMap
from image_to_grid import image_to_grid

# Create a 20x20 meter grid with 0.1m resolution
grid = OccupancyGridMap(
    width_meters=20,
    height_meters=20,
    resolution=0.1,
    inflation_meters=0.5
)

# Convert a drone image into a local occupancy grid
local_grid = image_to_grid("images/field.png", (200, 200))

# Update the global map from the drone's position
grid.update_from_local_grid(
    local_grid=local_grid,
    drone_x=0.0,
    drone_y=0.0
)

# Visualize and save the result
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

### 1. Image Processing Pipeline

The image processing uses HSV color space to detect obstacles on green grass:

- Resize image to match grid dimensions
- Blur to reduce camera noise
- Convert to HSV color space (separates color from brightness)
- Detect green range to identify grass
- Invert to find non-green obstacles (any color)
- Apply light morphological operations to fill holes and remove noise
- Convert to grid values (FREE or OCCUPIED)

This approach is robust because it works with obstacles of any color, not just specific shades.

### 2. Coordinate Transformation

- Converts world coordinates (meters) to grid indices
- Handles differences between image origins and grid coordinates
- Keeps the global map consistent as observations update it
- Flips image rows to align with standard coordinate frame

### 3. Map Integration

- Local grids from the drone camera are projected into the global map
- Unknown cells are updated as new observations are made
- Occupied cells are preserved once detected (safety priority)
- Supports multiple observations over time

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

## License

Developed for SMU Drone Club

## Author

Antonio  
SMU Drone Club
