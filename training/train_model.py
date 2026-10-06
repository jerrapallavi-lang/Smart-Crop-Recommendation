
import pandas as pd
import pickle
from pathlib import Path

from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

# Setup paths
TRAINING_DIR = Path(__file__).parent
PROJECT_ROOT = TRAINING_DIR.parent
DATASET_PATH = PROJECT_ROOT / "dataset" / "crop_data.csv"
MODELS_DIR = PROJECT_ROOT / "models"

# Create models directory if it doesn't exist
MODELS_DIR.mkdir(exist_ok=True)

data = pd.read_csv(DATASET_PATH)
data = data.dropna(subset=["soil_type", "temperature", "rainfall", "ph", "crop", "yield"])
data = data[data["soil_type"].astype(str).str.strip() != "I"]

data["soil_type"] = data["soil_type"].astype(str).str.strip()
data["crop"] = data["crop"].astype(str).str.strip()

data["temperature"] = pd.to_numeric(data["temperature"], errors="coerce")
data["rainfall"] = pd.to_numeric(data["rainfall"], errors="coerce")
data["ph"] = pd.to_numeric(data["ph"], errors="coerce")
data["yield"] = pd.to_numeric(data["yield"], errors="coerce")

data = data.dropna(subset=["temperature", "rainfall", "ph", "yield"])

soil_encoder = LabelEncoder()
crop_encoder = LabelEncoder()

data["soil_type"] = soil_encoder.fit_transform(data["soil_type"])
data["crop"] = crop_encoder.fit_transform(data["crop"])

X = data[["soil_type", "temperature", "rainfall", "ph"]]
y_crop = data["crop"]
y_yield = data["yield"]

crop_model = RandomForestClassifier(n_estimators=300, random_state=42)
crop_model.fit(X, y_crop)

yield_model = RandomForestRegressor(n_estimators=300, random_state=42)
yield_model.fit(X, y_yield)

with open(MODELS_DIR / "crop_model.pkl", "wb") as f:
    pickle.dump(crop_model, f)
with open(MODELS_DIR / "yield_model.pkl", "wb") as f:
    pickle.dump(yield_model, f)
with open(MODELS_DIR / "soil_encoder.pkl", "wb") as f:
    pickle.dump(soil_encoder, f)
with open(MODELS_DIR / "crop_encoder.pkl", "wb") as f:
    pickle.dump(crop_encoder, f)

print("Models trained and saved successfully")
print(f"Models saved to: {MODELS_DIR}")
