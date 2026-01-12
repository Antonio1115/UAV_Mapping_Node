# UAV Occupancy Grid Mapping

This project is a Python-based occupancy grid mapping system designed for autonomous drone navigation. The goal is to take a top-down camera image from a drone and convert it into a 2D occupancy grid that can be used for obstacle detection and path planning.

## Features

**Occupancy Grid Mapping**  
Maintains a global 2D grid with three states: UNKNOWN, FREE, and OCCUPIED

**Image-to-Grid Conversion**  
Uses OpenCV to process top-down images and convert them into local occupancy grids

**World Coordinate Mapping**  
Converts between real-world coordinates (meters) and grid indices

**Synthetic Field Generator**  
Generates test images with squares and circles for simulation and testing

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
├── occupancy_grid.py      # Global occupancy grid  implementation
├── image_to_grid.py       # Image processing pipeline
├── test_field.py          # Test field generator
├── main.py                # Example usage / demo
├── images/                # Input images
└── .gitignore
```

## Usage

### Basic Example

```python
from occupancy_grid import OccupancyGridMap
from image_to_grid import image_to_grid

# Create a 20x20 meter grid with 0.2m resolution
grid = OccupancyGridMap(
    width_meters=20,
    height_meters=20,
    resolution=0.2,
    inflation_meters=0.5
)

# Convert an image into a local occupancy grid
local_grid = image_to_grid("images/field.png", (100, 100))

# Update the global map from the drone's position
grid.update_from_local_grid(
    local_grid=local_grid,
    drone_x=0.0,
    drone_y=0.0
)

# Visualize and save the result
grid.visualize_grid()  # Saves to occupancy_grid.png
```

### Generate Test Fields

Using test fields currently because I could not find images that fit the type of pictures the drone will be taking.

```python
from test_field import generate_field

generate_field(
    width_px=600,
    height_px=600,
    output_path="images/field.png"
)
```

## How It Works

### 1. Image Processing Pipeline

The image processing pipeline is designed to be simple but robust for top-down views:

- Convert image to grayscale
- Blur the image to reduce noise
- Apply binary thresholding to separate obstacles from free space
- Use light morphological operations to clean up noise
- Convert pixels into occupancy grid values

This pipeline is meant to closely mirror how real camera data would be processed onboard a drone.

### 2. Coordinate Transformation

- Converts world coordinates (meters) into grid indices
- Handles differences between image coordinate systems and grid coordinates
- Keeps the global map centered and consistent as new observations come in

### 3. Map Integration

- Local grids from the drone's camera are projected into the global map
- Unknown cells are updated as new data is observed
- Occupied cells are preserved once detected to maintain safety

## Occupancy Grid States

**-1 (UNKNOWN)**  
Area has not been observed yet

**0 (FREE)**  
Clear space, safe for navigation

**1 (OCCUPIED)**  
Obstacle detected (e.g. box, cone)

## License

Developed for SMU Drone Club

## Author

Antonio F.
