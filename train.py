
from dataset_loader import load_dataset
from image_dataset import load_images
from model import build_model
from feature_config import FEATURE_COLUMNS
import numpy as np

CSV_PATH = "full_mouth_rehab_dataset.csv"
IMAGE_DIR = "images"

X_clinical, image_files, y_img, y_stage, y_prog = load_dataset(CSV_PATH)
X_images = load_images(image_files, IMAGE_DIR)

model = build_model(len(FEATURE_COLUMNS))

model.fit(
    [X_images, X_clinical],
    [y_img, y_stage, y_prog],
    epochs=5,
    batch_size=8
)

model.save("full_mouth_model.h5")
