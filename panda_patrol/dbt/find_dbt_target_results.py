import os
from pathlib import Path


def find_dbt_target_results():
    target_results_path = os.path.join(os.getcwd(), "target/run_results.json")

    if os.path.exists(target_results_path):
        return target_results_path
    else:
        target_directory = os.path.join(os.getcwd(), "target")
        if not os.path.exists(target_directory):
            os.mkdir(target_directory)
        Path(os.path.join(target_directory, "run_results.json")).touch()

    return None
