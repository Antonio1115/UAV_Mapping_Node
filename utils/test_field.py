import cv2
import numpy as np
import random

def generate_field(
    width_px=600,
    height_px=600,
    output_path="images/field.png"
):
    img = np.zeros((height_px, width_px, 3), dtype=np.uint8)
    
    grass_base = np.random.randint(50, 80, (height_px, width_px, 1))
    img[:, :, 1] = grass_base[:, :, 0]
    img[:, :, 0] = grass_base[:, :, 0] // 3
    img[:, :, 2] = grass_base[:, :, 0] // 4
    
    texture = np.random.normal(0, 6, (height_px, width_px))
    texture = cv2.GaussianBlur(texture.astype(np.uint8), (7, 7), 0)
    img[:, :, 1] = np.clip(img[:, :, 1].astype(float) + texture, 0, 255).astype(np.uint8)
    
    obstacle_colors = [
        (20, 20, 20),      # Dark gray/black
        (25, 40, 100),     # Dark brown
        (30, 60, 120),     # Dark reddish-brown
        (50, 80, 150),     # Dark orange-brown
    ]
    
    for _ in range(5):
        x = random.randint(40, width_px - 120)
        y = random.randint(40, height_px - 120)
        w = random.randint(40, 100)
        h = random.randint(40, 100)

        color = random.choice(obstacle_colors)
        cv2.rectangle(img, (x, y), (x + w, y + h), color, -1)
        shadow_color = tuple(c // 2 for c in color)
        cv2.rectangle(img, (x, y), (x + w, y + h), shadow_color, 2)

    for _ in range(5):
        x = random.randint(50, width_px - 50)
        y = random.randint(50, height_px - 50)
        r = random.randint(12, 30)

        color = random.choice(obstacle_colors)
        cv2.circle(img, (x, y), r, color, -1)
        shadow_color = tuple(c // 2 for c in color)
        cv2.circle(img, (x, y), r, shadow_color, 2)

    gradient = np.linspace(0.9, 1.1, width_px)
    gradient = np.tile(gradient, (height_px, 1))
    gradient = gradient[:, :, np.newaxis]
    img = np.clip(img.astype(float) * gradient, 0, 255).astype(np.uint8)

    noise = np.random.normal(0, 6, img.shape)
    img = np.clip(img.astype(float) + noise, 0, 255).astype(np.uint8)

    img = cv2.GaussianBlur(img, (3, 3), 0)

    cv2.imwrite(output_path, img)
    print(f"Saved synthetic field to {output_path}")

if __name__ == "__main__":
    generate_field()
