
import os
import numpy as np
import tensorflow as tf
from PIL import Image
import traceback
from feature_config import FEATURE_COLUMNS, IMAGE_CLASSES

# Define the absolute path for the model to ensure it's found regardless of execution context
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "full_mouth_model.h5")

class AIEngine:
    def __init__(self):
        self.model = None
        print(f"Initializing AI Engine. Looking for model at: {MODEL_PATH}")
        if os.path.exists(MODEL_PATH):
            try:
                # Load the model - compiled metrics are not strictly necessary for inference
                self.model = tf.keras.models.load_model(MODEL_PATH)
                print("AI Model loaded successfully into memory.")
            except Exception as e:
                print(f"Error loading AI model: {e}")
                traceback.print_exc()
        else:
            print(f"CRITICAL: Model file not found at {MODEL_PATH}. Prediction features will be disabled.")

    def preprocess_image(self, image_file):
        """Resizes and normalizes the image for the model."""
        try:
            # Open image using Pillow
            img = Image.open(image_file).convert('RGB')
            img = img.resize((224, 224))
            img_array = np.array(img).astype(np.float32) / 255.0
            return np.expand_dims(img_array, axis=0) # Add batch dimension (1, 224, 224, 3)
        except Exception as e:
            print(f"Preprocessing error: {e}")
            raise

    def predict(self, image_file, clinical_features):
        """
        Runs the full AI inference pipeline.
        clinical_features: list of numeric values matching FEATURE_COLUMNS order.
        """
        if self.model is None:
            print("Predict called but model is not initialized.")
            return {"error": "AI Model not initialized"}

        try:
            # 1. Prepare image input
            img_input = self.preprocess_image(image_file)
            
            # 2. Prepare clinical features input (numerical)
            clinical_input = np.expand_dims(np.array(clinical_features, dtype=np.float32), axis=0)

            # 3. Perform Inference
            # The model has 3 outputs: image_class, stage, prognosis
            print("Running inference on model...")
            outputs = self.model.predict([img_input, clinical_input], verbose=0)
            
            # 4. Parse output tensors (Softmax results)
            # Use standard Python int() for JSON-safe representation
            image_class_idx = int(np.argmax(outputs[0]))
            stage_idx       = int(np.argmax(outputs[1]))
            prognosis_idx   = int(np.argmax(outputs[2]))

            result = {
                "image_class": IMAGE_CLASSES.get(image_class_idx, "Unknown"),
                "stage": stage_idx,
                "prognosis": prognosis_idx
            }
            print(f"Prediction successful: {result}")
            return result

        except Exception as e:
            print(f"AI Prediction Pipeline Error: {e}")
            traceback.print_exc()
            return {"error": f"Internal Prediction Error: {str(e)}"}

# Global instance
ai_engine = AIEngine()
