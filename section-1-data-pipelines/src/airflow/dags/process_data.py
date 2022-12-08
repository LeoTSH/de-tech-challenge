import os
import time
import pendulum
from datetime import timedelta, datetime, tzinfo
from airflow import DAG
from airflow.operators.bash import BashOperator

DAG_ID = os.path.basename(__file__).replace('.py', '')
DEFAULT_ARGS = {
    'owner': "Leo",
    'depends_on_past': False,
    'start_date': datetime(2022, 12, 8),
    'retries': 0,
    'retry_delay': timedelta(minutes=60),
    'provide_context': True,
    'email_on_failure': True,
    'email_on_retry': False
}

with DAG(
    dag_id=DAG_ID,
    description="Airflow dag to schedule data processing and insertion",
    default_args=DEFAULT_ARGS,
    catchup=False,
    dagrun_timeout=timedelta(hours=2),
    schedule_interval="0 */1 * * *"
    ) as ag:

    gen_data = BashOperator(
        task_id="gen_data",
        bash_command="python ./src/main.py"
    )

    gen_data
