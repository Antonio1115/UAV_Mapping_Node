import cv2
import numpy as np

FREE = 0
OCCUPIED = 1

def image_to_grid(image_path, grid_size):
    """
    Converts a top-down image into a local occupancy grid.
    Uses HSV color space to detect non-green obstacles on grass.
    """
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Image not found")

    grid_height, grid_width = grid_size
    
    # Resize first for efficiency
    img = cv2.resize(img, (grid_width, grid_height), interpolation=cv2.INTER_CUBIC)
    
    # Convert to HSV for color-based detection
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Define green range in HSV (grass colors)
    # H: 35-85 (green hues), S: 20-255 (saturation), V: 20-255 (value)
    lower_green = np.array([35, 20, 20])
    upper_green = np.array([85, 255, 255])
    
    # Create mask for green areas
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    
    # Invert to get non-green (obstacles)
    binary = cv2.bitwise_not(green_mask)
    
    # Light morphology to remove noise
    kernel_small = np.ones((2, 2), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel_small, iterations=1)

    local_grid = []

    for row in binary:
        grid_row = []
        
        for pixel in row:
            grid_row.append(OCCUPIED if pixel == 255 else FREE)

        local_grid.append(grid_row)

    return local_grid
