# Raport: Automatyzacja Pipeline'u ML przy użyciu Apache Airflow

## 1. Cel projektu

Celem było zautomatyzowanie procesu ETL i ML dla predykcji ceny Bitcoina poprzez stworzenie DAG-u w Apache Airflow, który orkiestruje kolejne pipeline'y Kedro w ustalonej kolejności:

1. **EDA** – eksploracyjna analiza danych historycznych BTC
2. **Preprocessing** – czyszczenie, skalowanie i podział danych
3. **Modeling** – trenowanie trzech modeli ML (Baseline, AutoML, Custom)
4. **Verification** – weryfikacja poprawności wygenerowanych artefaktów

Pipeline jest uruchamiany automatycznie co tydzień, zapewniając regularny retraining modeli na świeżych danych.

---

## 2. Architektura DAG-u

### 2.1 Struktura

Plik `dags/kedro_dag.py` definiuje kompleksowy DAG składający się z:

#### Główne taski:

- **start_pipeline** (PythonOperator) – logowanie rozpoczęcia wykonania
- **eda_pipeline** (BashOperator) – analiza eksploracyjna danych BTC
- **preprocessing_pipeline** (BashOperator) – przygotowanie danych do modelowania
- **modeling_pipeline** (BashOperator) – trenowanie modeli predykcyjnych
- **verify_results** (BashOperator) – weryfikacja utworzonych plików i metryk
- **end_pipeline** (PythonOperator) – logowanie zakończenia wykonania

#### Task alternatywny:

- **run_full_pipeline** (BashOperator) – możliwość uruchomienia pełnego pipeline'u w jednym kroku

### 2.2 Przepływ danych
```
start_pipeline 
    ↓
eda_pipeline (generuje: docs/heatmap_correlation.png, hist_*.png)
    ↓
preprocessing_pipeline (generuje: train.csv, val.csv, test.csv)
    ↓
modeling_pipeline (generuje: 3 modele .pkl + metryki .json)
    ↓
verify_results (sprawdza istnienie plików i wyświetla wyniki)
    ↓
end_pipeline
```

---

## 3. Konfiguracja i parametry

### 3.1 Parametry DAG-u

- dag_id: "btc_price_prediction_pipeline"
- schedule_interval: "@weekly" (każdy poniedziałek)
- max_active_runs: 1 (zapobiega konfliktom)
- retries: 2 (automatyczny retry przy błędzie)
- retry_delay: 5 minut

### 3.2 Tagi i metadane

DAG jest otagowany jako: `["kedro", "mlops", "bitcoin", "prediction", "ml"]`  
Ułatwia to filtrowanie i zarządzanie w Airflow UI.

---

## 4. Integracja Airflow z Kedro

### 4.1 Środowisko Docker

- Pipeline'y uruchamiają się wewnątrz kontenera Docker (`apache/airflow:2.9.0`)
- Kedro jest instalowany w kontenerze poprzez montowanie katalogu projektu: `/opt/project`
- Każdy task zmienia katalog roboczy na `/opt/project` przed wykonaniem

### 4.2 Wywołania Kedro

Każdy BashOperator wykorzystuje `set -e` dla natychmiastowego zatrzymania przy błędzie:
```bash
cd /opt/project
kedro run --pipeline=<nazwa_pipeline>
```

### 4.3 Możliwości uruchomienia

1. **Automatyczne** – co tydzień zgodnie z harmonogramem
2. **Manualne** – przez Airflow UI lub CLI
3. **Pojedyncze pipeline'y** – możliwość uruchomienia tylko wybranego kroku
4. **Pełny pipeline** – alternatywny task `run_full_pipeline`

---

## 5. Monitoring i diagnostyka

### 5.1 Logowanie

- Każdy task loguje swoje kroki przez `echo`
- Python Operators logują metadane wykonania (run_id, execution_date)
- Logi są dostępne w Airflow UI dla każdego taska osobno

### 5.2 Weryfikacja wyników

Task `verify_results` automatycznie sprawdza:

- Istnienie 3 modeli: `baseline_model.pkl`, `automl_model.pkl`, `custom_model.pkl`
- Istnienie pliku porównawczego: `model_comparison.json`
- Wyświetla wyniki porównania modeli w logach

### 5.3 Airflow UI

Dashboard umożliwia:

- **Tree View** – chronologiczne wykonania DAG-u
- **Graph View** – wizualizacja zależności między taskami
- **Gantt Chart** – analiza czasu wykonania
- **Task Logs** – szczegółowe logi każdego taska
- **Code View** – podgląd kodu DAG-u

---

## 6. Obsługa błędów i retry

- Automatyczne 2 próby ponownego uruchomienia przy błędzie
- 5-minutowa przerwa między próbami
- `max_active_runs=1` zapobiega konfliktom równoległych uruchomień

---

## 7. Wygenerowane artefakty

### 7.1 Po EDA
```
docs/
├── heatmap_correlation.png
├── hist_Open.png
├── hist_High.png
├── hist_Low.png
├── hist_Close.png
└── hist_Volume.png
```

### 7.2 Po Preprocessing
```
data/model_input/
├── train.csv (~70% danych)
├── val.csv (~15% danych)
└── test.csv (~15% danych)
```

### 7.3 Po Modeling
```
data/reporting/
├── baseline_model.pkl (model referencyjny)
├── baseline_metrics.json (RMSE, MAE, R²)
├── automl_model.pkl (najlepszy z 3 kandydatów)
├── automl_metrics.json (metryki + best_model)
├── custom_model.pkl (GridSearchCV RandomForest)
├── custom_metrics.json (metryki + cv_best_params)
└── model_comparison.json (porównanie RMSE wszystkich modeli)
```

---

## 9. Zrealizowane cele

- Pełna automatyzacja procesu ML
- Cotygodniowy retraining modeli
- Monitoring i logowanie każdego kroku
- Automatyczna weryfikacja outputów
- Obsługa błędów z retry
- Konteneryzacja w Docker

---

## 11. Korzyści z automatyzacji

1. **Spójność** – każdy model jest trenowany w identycznych warunkach
2. **Powtarzalność** – możliwość odtworzenia każdego run'u po run_id
3. **Skalowalność** – łatwe dodawanie nowych pipeline'ów
4. **Observability** – pełna widoczność procesu przez Airflow UI
5. **Niezawodność** – automatyczne retry i obsługa błędów

---

## 12. Podsumowanie

Projekt **Bitcoin Price Prediction Pipeline** stanowi kompleksowe rozwiązanie MLOps łączące:

- **Kedro** – modularność i reproducibility kodu ML
- **Airflow** – orkiestrację i scheduling
- **Docker** – konteneryzację i izolację środowiska

System umożliwia automatyczny modeli predykcyjnych na świeżych danych BTC, z pełnym monitoringiem i obsługą błędów. Pipeline jest gotowy do rozbudowy o kolejne funkcjonalności .
---