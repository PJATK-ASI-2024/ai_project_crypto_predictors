## 1. Cel procesu
Celem było zautomatyzowanie procesu ETL i ML poprzez stworzenie DAG-u w Apache Airflow, który uruchamia kolejne pipeline’y Kedro w ustalonej kolejności:

1. **EDA** – eksploracyjna analiza danych  
2. **Preprocessing** – przetwarzanie i przygotowanie danych  
3. **Modeling** – trenowanie modelu ML  
4. **Evaluation** – ewaluacja i zapis wyników  

---

## 2. Struktura DAG-u
Plik `dags/kedro_dag.py` definiuje cztery taski odpowiadające poszczególnym pipeline’om Kedro:

- Task `eda_pipeline` uruchamia pipeline EDA  
- Task `preprocessing_pipeline` uruchamia pipeline preprocessing  
- Task `modeling_pipeline` uruchamia pipeline modeling  
- Task `evaluation_pipeline` uruchamia pipeline evaluation  

Zależności między taskami są zachowane w kolejności: **EDA → Preprocessing → Modeling → Evaluation**.  

Każdy task wywołuje odpowiednie polecenie `kedro run` w katalogu projektu.

---

## 3. Integracja Airflow z Kedro
- Pipeline’y uruchamiają się w kontenerze Docker. Polecenia `bash_command` w taskach zostały odpowiednio zmodyfikowane, aby działały wewnątrz środowiska kontenerowego
- Pipeline’y uruchamiają się w środowisku Airflow.
- Możliwe jest uruchamianie zarówno całego DAG-u, jak i pojedynczych pipeline’ów.

---

## 4. Monitoring i harmonogramowanie
- DAG działa w trybie manualnym, ale możliwe jest ustawienie harmonogramu np. codziennie o 8:00.  
- Airflow UI umożliwia monitorowanie:
  - Status tasków (Success / Failed)  
  - Szczegółowe logi wykonania każdego pipeline’u  
  - Tree View i Graph View DAG-u  
- Retry tasków ustawiono na 1.

---

## 5. Wnioski i usprawnienia
- Airflow umożliwia pełną automatyzację procesu ETL + ML, z monitorowaniem i retry tasków.  
- Harmonogramowanie DAG-u pozwala na automatyczny retraining modeli.  
- Można dodać powiadomienia - np przez e-mail dla szybkiej reakcji na błędy.  
- Projekt pozwala w prosty sposób integrować pipeline’y Kedro i monitorować ich wykonanie w jednym narzędziu.

---
