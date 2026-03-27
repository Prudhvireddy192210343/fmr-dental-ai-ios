
import requests
import json
import os

# Create a dummy image for testing if none exists
dummy_image_path = "test_image.jpg"
if not os.path.exists(dummy_image_path):
    from PIL import Image
    img = Image.new('RGB', (224, 224), color='red')
    img.save(dummy_image_path)

url = "http://127.0.0.1:8000/predict"

# Sample clinical features as defined in feature_config.py
features = {
    "F001_Age": 55,
    "F002_Missing_Teeth_Count": 4,
    "F003_Periodontal_Severity": 2,
    "F004_Bone_Loss_Percentage": 15.0,
    "F005_Caries_Risk": 1,
    "F006_Pulpal_Involvement": 0,
    "F007_Occlusal_Stability": 1,
    "F008_Vertical_Dimension_Loss": 0,
    "F009_TMJ_Disorder": 0,
    "F010_Systemic_Risk": 1,
    "F011_Implant_Indicated": 1,
    "F012_Esthetic_Demand": 2
}

files = {
    'image': open(dummy_image_path, 'rb')
}
data = {
    'features': json.dumps(features)
}

print(f"Sending request to {url}...")
try:
    response = requests.post(url, files=files, data=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
finally:
    files['image'].close()
