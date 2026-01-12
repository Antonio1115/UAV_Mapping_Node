import cv2
import numpy as np
import random

def generate_field(
    width_px=600,
    height_px=600,
    output_path="images/field.png"
):
    img = np.ones((height_px, width_px), dtype=np.uint8) * 220

    for _ in range(5):
        x = random.randint(40, width_px - 120)
        y = random.randint(40, height_px - 120)
        w = random.randint(40, 100)
        h = random.randint(40, 100)
        color = random.randint(0, 50)  # not pure black
        cv2.rectangle(img, (x, y), (x + w, y + h), color, -1)

    for _ in range(5):
        x = random.randint(50, width_px - 50)
        y = random.randint(50, height_px - 50)
        r = random.randint(12, 30)
        color = random.randint(0, 50)
        cv2.circle(img, (x, y), r, color, -1)

    gradient = np.linspace(0.85, 1.05, width_px)
    gradient = np.tile(gradient, (height_px, 1))
    img = np.clip(img * gradient, 0, 255).astype(np.uint8)

    noise = np.random.normal(0, 10, (height_px, width_px))
    img = np.clip(img + noise, 0, 255).astype(np.uint8)

    img = cv2.GaussianBlur(img, (5, 5), 0)

    cv2.imwrite(output_path, img)
    print(f"Saved synthetic field to {output_path}")

if __name__ == "__main__":
    generate_field()
