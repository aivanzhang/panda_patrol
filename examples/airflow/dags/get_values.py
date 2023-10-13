import os
from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from panda_patrol.patrols import patrol_group

# Allow requests to access hosts directly without a proxy defined
os.environ["no_proxy"] = "*"


def get_values():
    data = [
        {"id": 1, "value": 100},
        {"id": 2, "value": 200},
        {"id": 3, "value": 0},
    ]

    # Simple test: Ensure no "value" field in the dataset is zero
    with patrol_group(
        "Value Checks",
    ) as patrol:

        @patrol("All values are non-zero")
        def no_zero_values(patrol_id):
            for entry in data:
                assert (
                    entry["value"] != 0
                ), f"Entry with id {entry['id']} has zero value!"


dag = DAG(
    "get_values",
    description="Get Values DAG",
    start_date=datetime(2017, 3, 20),
    catchup=False,
)

get_values_operator = PythonOperator(
    task_id="get_values_task", python_callable=get_values, dag=dag
)

get_values_operator
