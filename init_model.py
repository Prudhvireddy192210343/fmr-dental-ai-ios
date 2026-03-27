
import numpy as np
from model import build_model
from feature_config import FEATURE_COLUMNS
import os

# 1. Build model according to the specs in model.py
num_features = len(FEATURE_COLUMNS)
model = build_model(num_features)

# 2. Generate small amount of synthetic data to "prime" the model weights
batch_size = 4
synthetic_images = np.random.rand(batch_size, 224, 224, 3).astype(np.float32)
synthetic_clinical = np.random.rand(batch_size, num_features).astype(np.float32)

synthetic_y_img = np.random.randint(0, 4, size=(batch_size,))
synthetic_y_stage = np.random.randint(0, 6, size=(batch_size,))
synthetic_y_prog = np.random.randint(0, 4, size=(batch_size,))

print("Training on synthetic data for 1 epoch to initialize weights...")
model.fit(
    [synthetic_images, synthetic_clinical],
    [synthetic_y_img, synthetic_y_stage, synthetic_y_prog],
    epochs=1,
    verbose=1
)

# 3. Save the model
model_path = "full_mouth_model.h5"
model.save(model_path)
print(f"Model saved to {model_path}")
