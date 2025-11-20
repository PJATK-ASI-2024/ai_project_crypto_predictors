# Raport: Modeling — porównanie podejść

## 1. Dane wejściowe

* Train: `data/model_input/train.csv`
* Val: `data/model_input/val.csv`
* Test: `data/model_input/test.csv`
* Target: `Close` (regresja)

## 2. Modele

* **Baseline**: DummyRegressor (mean) + LinearRegression
* **AutoML**: RandomForest
* **Custom**: GridSearch

## 3. Wyniki i metryki

| Model                       | RMSE      | MAE       | R²          |
| --------------------------- | --------- | --------- | ----------- |
| Baseline (LinearRegression) | 0.0004678 | 0.0001944 | 0.99999978  |
| AutoML (RandomForest)       | 0.0016664 | 0.0010961 | 0.99999724  |
| AutoML (Dummy)              | 1.0036454 | 0.8016739 | -0.00000781 |
| Custom (GridSearch)         | 0.0006949 | 0.0003792 | 0.99999952  |

### Najlepszy model - LinearRegression

> **Uwaga:** wartości RMSE, MAE i R² pochodzą z plików `baseline_metrics.json`, `automl_metrics.json` i `custom_metrics.json`.

## 4. Rekomendacja

* Najlepszy model według RMSE: **Baseline / LinearRegression** (RMSE = 0.0004678)
* Kolejne kroki: dalsze strojenie (np. Optuna), eksperymenty z funkcjami czasowymi, analiza residuów, wdrożenie modelu

## 5. Pliki wygenerowane

* `data/reporting/baseline_model.pkl`
* `data/reporting/automl_model.pkl`
* `data/reporting/custom_model.pkl`
* `data/reporting/automl_results.csv`
* `data/reporting/*.json` — metryki i porównania
