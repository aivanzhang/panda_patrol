from panda_patrol.dbt.find_dbt_target_results import *
from panda_patrol.dbt.run_dbt import *


def main():
    dbt_results_path = find_dbt_target_results()
    if dbt_results_path:
        run_dbt(dbt_results_path)
    else:
        print(
            "No dbt results files found. Make sure that you're running this command in a dbt project."
        )
        return
