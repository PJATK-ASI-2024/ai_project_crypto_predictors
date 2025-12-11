from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_home():
    r = client.get("/")
    assert r.status_code == 200
    assert "BTC Prediction API" in r.json().get("message", "") or "BTC" in r.json().get("message", "")

def test_predict_basic():
    r = client.post("/predict", json={"horizon": "1h"})
    assert r.status_code == 200
    j = r.json()
    assert "prediction" in j
    assert isinstance(j["prediction"], float) or isinstance(j["prediction"], int)

def test_predict_with_features():
    payload = {
        "horizon": "1h",
        "Timestamp": 1325412060.0,
        "Open": 4.58,
        "High": 4.58,
        "Low": 4.58,
        "Volume": 0.0
    }
    r = client.post("/predict", json=payload)
    assert r.status_code == 200
    j = r.json()
    assert "used_input" in j
    assert j["used_input"]["Open"] == 4.58
    assert "prediction" in j
