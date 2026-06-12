from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from app.logger import get_logger
from app.pipeline.raw_pipeline import run_raw_pipeline
from app.pipeline.stg_pipeline import run_stg_pipeline
from airflow.models.param import Param


logger = get_logger(__name__)

def run_raw_pipeline_wrappers(**context):
    result = run_raw_pipeline(limit=100)

    context['ti'].xcom_push(key='inserted_id', value = result.get('inserted_id'))

    return result

def run_stg_pipeline_wrappers(**context):
    raw_id = context['params'].get('raw_id')
    if not raw_id:
        raw_id = context['ti'].xcom_pull(task_ids='load_raw', key='inserted_id')

    logger.info(f"Запуск run_stg_pipeline с id {raw_id}")
    return run_stg_pipeline(raw_id=raw_id)

default_args = {
    "owner": "Soluckyo",
    "start_date": datetime(2026, 5, 25),
    "retries": 1
}

with DAG(
    dag_id = "crypto_pipeline",
    default_args = default_args,
    params={'raw_id': Param(None, description="ID записи в raw.crypto_listings")},
    schedule_interval = timedelta(minutes=5),
    catchup = False
) as dag:
    
    raw = PythonOperator(
        task_id = "load_raw",
        python_callable = run_raw_pipeline_wrappers,
        op_kwargs={"limit": 100}
    )

    stg = PythonOperator(
        task_id = "load_stg",
        python_callable = run_stg_pipeline_wrappers
    )

raw >> stg