from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

default_args = {
    "owner": "crypto_predictors",
    "depends_on_past": False,
    "start_date": datetime(2025, 1, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

def log_pipeline_start(**context):
    """Loguje rozpoczęcie pipeline'u"""
    logger.info(f"Starting pipeline run: {context['dag_run'].run_id}")
    logger.info(f"Execution date: {context['execution_date']}")

def log_pipeline_end(**context):
    """Loguje zakończenie pipeline'u"""
    logger.info(f"Pipeline completed successfully: {context['dag_run'].run_id}")

with DAG(
    dag_id="btc_price_prediction_pipeline",
    default_args=default_args,
    description="Bitcoin price prediction ML pipeline using Kedro",
    schedule_interval="@weekly",  # Uruchamiaj co tydzień
    catchup=False,
    tags=["kedro", "mlops", "bitcoin", "prediction", "ml"],
    max_active_runs=1,  # Tylko jedna instancja naraz
) as dag:

    # Task startowy - logowanie
    start_pipeline = PythonOperator(
        task_id="start_pipeline",
        python_callable=log_pipeline_start,
        provide_context=True,
    )

    # Task 1: Eksploracyjna Analiza Danych (EDA)
    eda = BashOperator(
        task_id="eda_pipeline",
        bash_command="""
        set -e
        cd /opt/project
        echo "Running EDA pipeline..."
        kedro run --pipeline=eda
        echo "EDA pipeline completed successfully"
        """,
        dag=dag,
    )

    # Task 2: Preprocessing danych
    preprocessing = BashOperator(
        task_id="preprocessing_pipeline",
        bash_command="""
        set -e
        cd /opt/project
        echo "Running preprocessing pipeline..."
        kedro run --pipeline=preprocessing
        echo "Preprocessing completed successfully"
        ls -lh data/model_input/
        """,
        dag=dag,
    )

    # Task 3: Trenowanie modeli
    modeling = BashOperator(
        task_id="modeling_pipeline",
        bash_command="""
        set -e
        cd /opt/project
        echo "Running modeling pipeline..."
        kedro run --pipeline=modeling
        echo "Modeling completed successfully"
        ls -lh data/reporting/
        """,
        dag=dag,
    )

    # Task 4: Weryfikacja wyników
    verify_results = BashOperator(
        task_id="verify_results",
        bash_command="""
        set -e
        cd /opt/project
        echo "Verifying pipeline results..."
        
        # Sprawdź czy powstały wymagane pliki
        test -f data/reporting/baseline_model.pkl || exit 1
        test -f data/reporting/automl_model.pkl || exit 1
        test -f data/reporting/custom_model.pkl || exit 1
        test -f data/reporting/model_comparison.json || exit 1
        
        echo "All required files exist"
        
        # Wyświetl porównanie modeli
        echo "Model comparison results:"
        cat data/reporting/model_comparison.json
        """,
        dag=dag,
    )

    # Task końcowy - logowanie
    end_pipeline = PythonOperator(
        task_id="end_pipeline",
        python_callable=log_pipeline_end,
        provide_context=True,
    )

    # Alternatywny task dla pełnego pipeline'u (wszystkie kroki naraz)
    full_pipeline = BashOperator(
        task_id="run_full_pipeline",
        bash_command="""
        set -e
        cd /opt/project
        echo "Running complete pipeline..."
        kedro run
        echo "Full pipeline completed successfully"
        """,
        dag=dag,
        # Ten task nie będzie wykonywany domyślnie
        trigger_rule="none_failed_or_skipped",
    )

    # Definicja zależności
    start_pipeline >> eda >> preprocessing >> modeling >> verify_results >> end_pipeline
    
    # Alternatywna ścieżka: pełny pipeline w jednym tasku
    # (można uruchomić manualnie jeśli potrzebne)
    start_pipeline >> full_pipeline >> end_pipeline