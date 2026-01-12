import cv2
import numpy as np
import random

def generate_field(
    width_px=600,
    height_px=600,
    output_path="images/field.png"
):
    # 1. Empty field (white)
    img = np.ones((height_px, width_px), dtype=np.uint8) * 255

    # Random boxes
    for _ in range(5):
        x = random.randint(50, 500)
        y = random.randint(50, 500)
        w = random.randint(30, 80)
        h = random.randint(30, 80)
        cv2.rectangle(img, (x, y), (x + w, y + h), 0, -1)

    # Random cones
    for _ in range(5):
        x = random.randint(50, 550)
        y = random.randint(50, 550)
        r = random.randint(10, 25)
        cv2.circle(img, (x, y), r, 0, -1)

    # 4. Save image
    cv2.imwrite(output_path, img)
    print(f"Saved synthetic field to {output_path}")

if __name__ == "__main__":
    generate_field()
