import cv2
import numpy as np

FREE = 0
OCCUPIED = 1

def image_to_grid(image_path, grid_size):
    """
    Converts a top-down image into a local occupancy grid.
    """
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Image not found")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    grid_height, grid_width = grid_size
    
    # Apply bilateral filter to reduce noise while keeping edges sharp
    gray = cv2.bilateralFilter(gray, 9, 75, 75)
    
    # Use INTER_CUBIC for better shape preservation during downsampling
    gray = cv2.resize(gray, (grid_width, grid_height), interpolation=cv2.INTER_CUBIC)

    # Light Gaussian blur to smooth minor noise
    blur = cv2.GaussianBlur(gray, (3, 3), 0)

    # Use Otsu's method for automatic threshold - better for shape preservation
    _, binary = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Minimal morphology - only remove single isolated pixels
    kernel_small = np.ones((2, 2), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel_small, iterations=1)

    local_grid = []

    for row in binary:
        grid_row = []
        
        for pixel in row:
            grid_row.append(OCCUPIED if pixel == 0 else FREE)

        local_grid.append(grid_row)

    return local_grid
