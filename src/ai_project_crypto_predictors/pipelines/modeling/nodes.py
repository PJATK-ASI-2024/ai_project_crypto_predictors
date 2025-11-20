import logging
import pickle
from pathlib import Path
from typing import Dict, Tuple, Any

import numpy as np
import pandas as pd
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import GridSearchCV

logger = logging.getLogger(__name__)

def _subsample(df: pd.DataFrame, n: int = 50000) -> pd.DataFrame:
    """Ucina dataset do maksymalnie n wierszy dla szybkiego trenowania."""
    if len(df) > n:
        logger.warning(f"Dataset ma {len(df)} wierszy — redukuję do {n}.")
        return df.sample(n=n, random_state=42)
    return df


def _regression_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    rmse = mean_squared_error(y_true, y_pred, squared=False)
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    return {"rmse": float(rmse), "mae": float(mae), "r2": float(r2)}


def _save_pickle(obj: Any, path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(obj, f)
    logger.info(f"Zapisano pickle: {path}")


def _save_dataframe(df: pd.DataFrame, path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    logger.info(f"Zapisano CSV: {path}")


def train_baseline(train_data: pd.DataFrame, val_data: pd.DataFrame):
    logger.info("Trening modelu bazowego...")
    train_data = _subsample(train_data)
    val_data = _subsample(val_data)

    target = "Close"

    X_train = train_data.drop(columns=[target])
    y_train = train_data[target].values
    X_val = val_data.drop(columns=[target])
    y_val = val_data[target].values

    dummy = DummyRegressor(strategy="mean")
    dummy.fit(X_train, y_train)

    lin = LinearRegression(n_jobs=-1)
    lin.fit(X_train, y_train)

    metrics = {
        "dummy": _regression_metrics(y_val, dummy.predict(X_val)),
        "linear_regression": _regression_metrics(y_val, lin.predict(X_val)),
    }

    logger.info("Baseline trained.")
    return lin, metrics


def train_automl(train_data: pd.DataFrame, val_data: pd.DataFrame):
    logger.info("AutoML (light version)...")
    train_data = _subsample(train_data)
    val_data = _subsample(val_data)

    target = "Close"

    X_train = train_data.drop(columns=[target])
    y_train = train_data[target].values
    X_val = val_data.drop(columns=[target])
    y_val = val_data[target].values

    candidate_models = {
        "LinearRegression": LinearRegression(n_jobs=-1),
        "RandomForest": RandomForestRegressor(
            n_estimators=50, max_depth=8, n_jobs=-1, random_state=42
        ),
        "Dummy": DummyRegressor(strategy="mean"),
    }

    best_model = None
    best_rmse = float("inf")
    results = {}

    for name, model in candidate_models.items():
        model.fit(X_train, y_train)
        metrics = _regression_metrics(y_val, model.predict(X_val))
        results[name] = metrics
        if metrics["rmse"] < best_rmse:
            best_rmse = metrics["rmse"]
            best_model = model

    results["best_model"] = best_model.__class__.__name__
    logger.info(f"AutoML zakończone. Best: {best_model.__class__.__name__}")
    return best_model, results


def train_custom(train_data: pd.DataFrame, val_data: pd.DataFrame):
    logger.info("Custom model (fast GridSearch)...")
    train_data = _subsample(train_data)
    val_data = _subsample(val_data)

    target = "Close"

    X_train = train_data.drop(columns=[target])
    y_train = train_data[target].values
    X_val = val_data.drop(columns=[target])
    y_val = val_data[target].values

    rf = RandomForestRegressor(random_state=42, n_jobs=-1)

    param_grid = {
        "n_estimators": [20, 50],
        "max_depth": [5, 10],
    }

    gscv = GridSearchCV(
        rf,
        param_grid,
        cv=2,
        scoring="neg_root_mean_squared_error",
        n_jobs=-1,
    )

    gscv.fit(X_train, y_train)
    best = gscv.best_estimator_

    metrics = _regression_metrics(y_val, best.predict(X_val))
    metrics["cv_best_params"] = gscv.best_params_

    logger.info("Custom model trained.")
    return best, metrics


def evaluate_models(baseline_metrics, automl_metrics, custom_metrics):
    logger.info("Porównanie modeli...")

    def get_rmse(d):
        if "linear_regression" in d:
            return d["linear_regression"]["rmse"]
        if "rmse" in d:
            return d["rmse"]
        if "dummy" in d:
            return d["dummy"]["rmse"]
        return float("inf")

    scores = {
        "baseline_rmse": get_rmse(baseline_metrics),
        "automl_rmse": get_rmse(automl_metrics),
        "custom_rmse": get_rmse(custom_metrics),
    }

    best_key = min(scores, key=scores.get)
    scores["best"] = best_key.replace("_rmse", "")

    return scores


def persist_baseline(model, metrics):
    path_model = "data/reporting/baseline_model.pkl"
    path_metrics = "data/reporting/baseline_metrics.json"
    _save_pickle(model, path_model)
    pd.Series(metrics).to_json(path_metrics)
    return {"model_path": path_model}


def persist_automl(model, metrics):
    path_model = "data/reporting/automl_model.pkl"
    path_metrics = "data/reporting/automl_metrics.json"
    _save_pickle(model, path_model)
    pd.Series(metrics).to_json(path_metrics)
    return {"model_path": path_model}



def persist_custom(model, metrics):
    path_model = "data/reporting/custom_model.pkl"
    path_metrics = "data/reporting/custom_metrics.json"
    _save_pickle(model, path_model)
    pd.Series(metrics).to_json(path_metrics)
    return {"model_path": path_model}
