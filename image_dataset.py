
import os
import cv2
import numpy as np

def load_images(image_files, image_dir, size=224):
    images = []
    for f in image_files:
        path = os.path.join(image_dir, f)
        img = cv2.imread(path)
        if img is None:
            img = np.zeros((size, size, 3), dtype=np.uint8)
        img = cv2.resize(img, (size, size))
        img = img / 255.0
        images.append(img)
    return np.array(images)
