import os
import time
from panda_patrol.dbt.dbt_to_panda_patrol import dbt_to_panda_patrol


def run_dbt(results):
    print(f"Monitoring dbt results file: {results}")
    run_results_mtime = os.path.getmtime(results)
    while True:
        new_run_results_mtime = os.path.getmtime(results)
        if new_run_results_mtime != run_results_mtime:
            dbt_to_panda_patrol(results)
            run_results_mtime = new_run_results_mtime
        time.sleep(5)
