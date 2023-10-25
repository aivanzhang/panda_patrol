import os
from datetime import datetime
import pandas as pd
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from ydata_profiling import ProfileReport
from panda_patrol.patrols import patrol_group
from panda_patrol.parameters import adjustable_parameter
from panda_patrol.profilers import save_report

# Allow requests to access hosts directly without a proxy defined
os.environ["no_proxy"] = "*"


def get_values():
    data = [
        {"id": 1, "value": 100},
        {"id": 2, "value": 200},
        {"id": 3, "value": 0},
    ]

    # Group: Tests for the values
    with patrol_group(
        "Value Checks",
    ) as patrol:
        # Test: All values are above a certain threshold
        @patrol("All values are above a certain threshold")
        def values_above_threshold(patrol_id):
            value_threshold = float(adjustable_parameter("threshold", patrol_id, -10))
            for entry in data:
                assert (
                    entry["value"] > value_threshold
                ), f"Entry with id {entry['id']} is below the threshold of {value_threshold}!"

    report = ProfileReport(pd.DataFrame(data))
    # Save the report
    save_report(report.to_html(), "Value Checks", "Values Profiling Report", "html")


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
