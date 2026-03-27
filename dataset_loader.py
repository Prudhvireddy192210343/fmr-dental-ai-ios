import pandas as pd
from feature_config import FEATURE_COLUMNS

def load_dataset(csv_path):
    df = pd.read_csv(csv_path)
    X_clinical = df[FEATURE_COLUMNS].values
    y_image = df["Image_Class"].values
    y_stage = df["TreatmentStage"].values
    y_prog = df["Prognosis"].values
    image_files = df["Image_File"].values
    return X_clinical, image_files, y_image, y_stage, y_prog
