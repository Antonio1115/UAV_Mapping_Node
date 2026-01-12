import cv2

FREE = 0
OCCUPIED = 1

def image_to_grid(image_path, grid_size):
    """
    Turns an image into a local occupancy grid
    """

    img = cv2.imread(image_path)

    if img is None:
        raise ValueError("Image not found")
    
    grid_height, grid_width = grid_size
    
    img = cv2.resize(img, (grid_width, grid_height))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (5,5), 0)

    bw = cv2.adaptiveThreshold(
    blur,
    255,
    cv2.ADAPTIVE_THRESH_MEAN_C,
    cv2.THRESH_BINARY,
    11,
    2
)
    local_grid = []

    for row in bw:
        grid_row = []
        for pixel in row: 
            if pixel == 0:
                grid_row.append(OCCUPIED)
            else:
                grid_row.append(FREE)

        local_grid.append(grid_row)

    return local_grid
