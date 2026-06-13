
import pandas as pd
import pickle
from pathlib import Path
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LinearRegression

# Setup paths
TRAINING_DIR = Path(__file__).parent
PROJECT_ROOT = TRAINING_DIR.parent
DATASET_PATH = PROJECT_ROOT / "dataset" / "crop_data.csv"
MODELS_DIR = PROJECT_ROOT / "models"

# Create models directory if it doesn't exist
MODELS_DIR.mkdir(exist_ok=True)

data = pd.read_csv(DATASET_PATH)

soil_encoder = LabelEncoder()
crop_encoder = LabelEncoder()

data["soil_type"] = soil_encoder.fit_transform(data["soil_type"])
data["crop"] = crop_encoder.fit_transform(data["crop"])

X = data[["soil_type", "temperature", "rainfall", "ph"]]
y_crop = data["crop"]
y_yield = data["yield"]

crop_model = DecisionTreeClassifier()
crop_model.fit(X, y_crop)

yield_model = LinearRegression()
yield_model.fit(X, y_yield)

pickle.dump(crop_model, open(MODELS_DIR / "crop_model.pkl", "wb"))
pickle.dump(yield_model, open(MODELS_DIR / "yield_model.pkl", "wb"))
pickle.dump(soil_encoder, open(MODELS_DIR / "soil_encoder.pkl", "wb"))
pickle.dump(crop_encoder, open(MODELS_DIR / "crop_encoder.pkl", "wb"))

print("Models trained and saved successfully")
print(f"Models saved to: {MODELS_DIR}")
