import cv2

FREE = 0
OCCUPIED = 1

def image_to_grid(image_path, grid_size):
    """
    Turns an image into a local occupancy grid
    """

    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        raise ValueError("Image not found")
    
    grid_height, grid_width = grid_size
    
    img = cv2.resize(img, (grid_width, grid_height))
    _, img_bw = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    local_grid = []

    for row in img_bw:
        grid_row = []
        for pixel in row: 
            if pixel == 0:
                grid_row.append(OCCUPIED)
            else:
                grid_row.append(FREE)

        local_grid.append(grid_row)

    return local_grid
