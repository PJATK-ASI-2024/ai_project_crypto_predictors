# Bitcoin Price Prediction

## Cel projektu
Celem projektu jest stworzenie aplikacji do predykcji cen Bitcoina na podstawie danych historycznych.  
System może być wykorzystany do analizy trendów, edukacji lub do wspomagania decyzji inwestycyjnych.

Dane pochodzą z: [Bitcoin Historical Data — Kaggle](https://www.kaggle.com/datasets/mczielinski/bitcoin-historical-data)


## Zakres projektu
- **ETL (Kedro)** – przetwarzanie i czyszczenie danych, zapis do folderu `data/processed`.
- **Model ML** – predykcja ceny zamknięcia Bitcoina (np. RandomForest, XGBoost, LSTM).
- **Backend (FastAPI)** – endpoint `/predict`, który zwraca prognozowaną cenę.
- **UI (Streamlit)** – prosty interfejs użytkownika do wprowadzania danych i wyświetlania prognozy.
- **Airflow** – automatyczne harmonogramowanie pipeline’u.
- **Docker** – konteneryzacja całego systemu.

---


## Struktura katalogów
````
ai_project_crypto_predictors/
├── docs/
│   └── architecture_diagram.png
├── src/
│   └── ai_project_crypto_predictors/
├── data/
│   ├── raw/
│   ├── processed/
│   └── models/
├── notebooks/
├── .gitignore
├── requirements.txt
├── LICENSE
└── README.md
````


---

## Technologie
- Python 3.10+
- Kedro
- scikit-learn / TensorFlow / XGBoost
- FastAPI
- Streamlit
- Docker


---

## Ocena — Rezultat końcowy po zajęciach 1

| Nr | Element oceny | Opis | Punkty maks. | Punkty uzyskane |
|----|----------------|------|---------------|-----------------|
| 1️⃣ | **Repozytorium GitHub** | Utworzony projekt Kedro, README, `.gitignore`, `requirements.txt`, `LICENSE` | **10 pkt** | |
| 2️⃣ | **Backlog projektu w GitHub Projects** | Minimum 10 zadań w tablicy z przypisanymi osobami i statusem | **5 pkt** | |
| 3️⃣ | **Diagram architektury systemu (w folderze `docs/`)** | Diagram z modułami (ETL, ML, API, UI, Airflow, Docker) | **5 pkt** | |
|   | **Łącznie** |  | **20 pkt** | |

---

## Członkowie zespołu

| Imię i nazwisko | Rola w projekcie | GitHub login |
|------------------|------------------|---------------|
|Mikołaj Wróblewski|Project leader    |Mikku0         |

---

## Linki projektu

- Repozytorium GitHub: [GitHub Repo](https://github.com/Mikku0/ai_project_crypto_predictors)
- GitHub Project Board: [GitHub Project](https://github.com/users/Mikku0/projects/1)
- Dokumentacja / diagram architektury: [architecture_diagram.png](docs/architecture_diagram.png)

---

## Zadania na kolejne zajęcia
1. Przygotować dane do eksploracji (EDA) na zajęcia 2.  
2. Utworzyć pierwszy pipeline Kedro
---