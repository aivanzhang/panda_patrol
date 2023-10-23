import os


def find_dbt_target_results():
    target_results_path = os.path.join(
        os.getcwd() + "/examples/dbt_pipeline", "target/run_results.json"
    )

    if os.path.exists(target_results_path):
        return target_results_path

    return None
