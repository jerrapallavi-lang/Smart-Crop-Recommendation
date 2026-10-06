import pickle
import subprocess
import sys
import unittest
from pathlib import Path

import pandas as pd
from sklearn.model_selection import KFold, cross_val_score
from sklearn.preprocessing import LabelEncoder

ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = ROOT / "dataset" / "crop_data.csv"
MODELS_DIR = ROOT / "models"


class TestModelQuality(unittest.TestCase):
    def setUp(self):
        subprocess.run([sys.executable, str(ROOT / "training" / "train_model.py")], cwd=str(ROOT), check=True)

        with open(MODELS_DIR / "crop_model.pkl", "rb") as f:
            self.crop_model = pickle.load(f)
        with open(MODELS_DIR / "yield_model.pkl", "rb") as f:
            self.yield_model = pickle.load(f)
        with open(MODELS_DIR / "soil_encoder.pkl", "rb") as f:
            self.soil_encoder = pickle.load(f)
        with open(MODELS_DIR / "crop_encoder.pkl", "rb") as f:
            self.crop_encoder = pickle.load(f)

        df = pd.read_csv(DATASET_PATH)
        df = df[df["soil_type"].astype(str).str.strip() != "I"]
        df["soil_type"] = self.soil_encoder.transform(df["soil_type"])
        df["crop"] = self.crop_encoder.transform(df["crop"])
        self.X = df[["soil_type", "temperature", "rainfall", "ph"]]
        self.y = df["yield"]

    def test_yield_model_r2_above_threshold(self):
        cv = KFold(n_splits=min(5, len(self.X)), shuffle=True, random_state=42)
        scores = cross_val_score(self.yield_model, self.X, self.y, cv=cv, scoring="r2")
        self.assertGreater(scores.mean(), 0.8, f"Yield model R2 too low: {scores.mean()}")


if __name__ == "__main__":
    unittest.main()
