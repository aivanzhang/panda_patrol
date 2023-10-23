import os
from pathlib import Path


def find_dbt_target_results():
    target_directory = os.path.join(os.getcwd(), "target")
    if not os.path.exists(target_directory):
        os.mkdir(target_directory)

    target_results_path = os.path.join(target_directory, "run_results.json")
    if not os.path.exists(target_results_path):
        Path(target_results_path).touch()

    return target_results_path
