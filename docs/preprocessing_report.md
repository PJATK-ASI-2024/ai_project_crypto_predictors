# Raport: Data Preprocessing

## Opis działań

W pipeline'ie *preprocessing* wykonano trzy etapy:

### 1. Czyszczenie danych
- Usunięto kolumny z >40% braków.
- Braki uzupełniono medianą (dla liczb) lub najczęstszą wartością (dla tekstu).
- Usunięto duplikaty i wartości odstające (IQR).
- Dokonano konwersji typów danych.

### 2. Standaryzacja
- Użyto `StandardScaler` (średnia = 0, odchylenie = 1).
- Dane zapisano do `data/primary/scaled_data.csv`.

### 3. Podział danych
- Podział: 70% train, 15% val, 15% test.
- Wyniki zapisano do `data/model_input/`.

## Wyniki pipeline’u
| Zbiór  | Liczba wierszy | Ścieżka pliku |
|--------|----------------|----------------|
| train  | 70% danych    | `data/model_input/train.csv` |
| val    | 15% danych    | `data/model_input/val.csv` |
| test   | 15% danych    | `data/model_input/test.csv` |

## Wyniki testów
```python
=========================================================================== test session starts ===========================================================================
platform win32 -- Python 3.12.4, pytest-9.0.1, pluggy-1.6.0
rootdir: D:\ProjektyPython\ASI\BTC_project
configfile: pyproject.toml
plugins: anyio-4.11.0
collected 3 items

src\tests\pipelines\preprocessing\test_nodes.py ...                                                                                                                  [100%]

============================================================================ 3 passed in 1.02s ============================================================================
```

## Kolejne kroki
- Dalszy feature engineering.
- Detekcja trendów czasowych.
- Selekcja cech pod modele ML.
