from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from app.logger import get_logger
from app.pipeline.raw_pipeline import run_raw_pipeline


logger = get_logger(__name__)

deafult_args = {
    "owner": "Soluckyo",
    "start_date": datetime(2026, 5, 25),
    "retries": 1
}

with DAG(
    dag_id = "crypto_pipeline",
    default_args = deafult_args,
    schedule_interval = timedelta(minutes=5),
    catchup = False
) as dag:
    
    raw = PythonOperator(
        task_id = "load_raw",
        python_callable = run_raw_pipeline,
        op_kwargs={"limit": 100}
    )