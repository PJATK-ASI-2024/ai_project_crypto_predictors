from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import os
import pickle
from pathlib import Path
from sklearn.dummy import DummyRegressor

app = FastAPI(title="BTC Prediction API", version="1.0")

MODEL_CANDIDATES = [
    "data/reporting/best_model.pkl",
    "data/reporting/custom_model.pkl",
    "data/reporting/automl_model.pkl",
    "data/reporting/baseline_model.pkl",
    "data/reporting/automl_model.pkl",
]

ZIP_PATH = "data/raw/btc-price-history.zip"
CSV_FALLBACKS = [
    "data/intermediate/clean_data.csv",
    "data/raw/dataset.csv",
    "data/raw/btc-price-history.csv",
]


def load_model() -> object:
    for p in MODEL_CANDIDATES:
        if os.path.exists(p):
            try:
                with open(p, "rb") as f:
                    model = pickle.load(f)
                return model
            except Exception:
                continue    
    dummy = DummyRegressor(strategy="mean")    
    X = [[0, 0, 0, 0, 0]]
    y = [0.0]
    dummy.fit(X, y)
    return dummy


MODEL = load_model()


class PredictRequest(BaseModel):        
    horizon: str | None = None    
    Timestamp: float | None = None
    Open: float | None = None
    High: float | None = None
    Low: float | None = None
    Close: float | None = None
    Volume: float | None = None


@app.get("/")
def home():
    return {"message": "BTC Prediction API działa. Użyj /predict"}


def read_latest_row_from_zip(zip_path: str) -> pd.Series | None:
    import zipfile

    if not os.path.exists(zip_path):
        return None
    try:
        with zipfile.ZipFile(zip_path, "r") as z:            
            csv_files = [n for n in z.namelist() if n.lower().endswith(".csv")]
            if not csv_files:
                return None            
            with z.open(csv_files[0]) as f:
                df = pd.read_csv(f)
            if df.empty:
                return None
            return df.iloc[-1]
    except Exception:
        return None


def read_latest_row_from_csv_list(paths: list[str]) -> pd.Series | None:
    for p in paths:
        if os.path.exists(p):
            try:
                df = pd.read_csv(p)
                if df.empty:
                    continue
                return df.iloc[-1]
            except Exception:
                continue
    return None


def get_input_row(req: PredictRequest) -> dict:    
    if req.Timestamp is not None and req.Open is not None and req.High is not None and req.Low is not None and req.Volume is not None:
        return {
            "Timestamp": float(req.Timestamp),
            "Open": float(req.Open),
            "High": float(req.High),
            "Low": float(req.Low),
            "Volume": float(req.Volume),
        }
    
    row = read_latest_row_from_zip(ZIP_PATH)
    if row is None:
        row = read_latest_row_from_csv_list(CSV_FALLBACKS)
    
    if row is None:
        return {"Timestamp": 0.0, "Open": 0.0, "High": 0.0, "Low": 0.0, "Volume": 0.0}
        
    def get_val(r, keys):
        for k in keys:
            if k in r:
                return r[k]
        return 0.0
    
    r = row
    return {
        "Timestamp": float(get_val(r, ["Timestamp", "timestamp", "Time", "time"])),
        "Open": float(get_val(r, ["Open", "open"])),
        "High": float(get_val(r, ["High", "high"])),
        "Low": float(get_val(r, ["Low", "low"])),
        "Volume": float(get_val(r, ["Volume", "volume", "Vol"])),
    }


@app.post("/predict")
def predict(req: PredictRequest):
    input_row = get_input_row(req)
    
    X = pd.DataFrame([input_row])    
    try:
        pred = MODEL.predict(X)[0]
        msg = "prediction (model used directly)"
    except Exception:        
        try:
            pred = MODEL.predict([[input_row["Timestamp"], input_row["Open"], input_row["High"], input_row["Low"], input_row["Volume"]]])[0]
            msg = "prediction (model used as list)"
        except Exception as exc:            
            dummy = DummyRegressor(strategy="mean")
            dummy.fit([[0, 0, 0, 0, 0]], [0.0])
            pred = dummy.predict([[0, 0, 0, 0, 0]])[0]
            msg = f"fallback prediction (model failed: {str(exc)})"

    return {
        "prediction": float(abs(pred)),
        "horizon_received": req.horizon,
        "note": msg,
        "used_input": input_row,
    }
