import pandas as pd
from panda_patrol.parameters import adjustable_parameter


def should_run(df: pd.DataFrame):
    return df.shape[0] > 0


def run_patrol(df: pd.DataFrame, patrol):
    @patrol(f"Volume")
    def volume(patrol_id):
        curr_row_count = df.shape[0]
        expected_row_count = int(
            adjustable_parameter("row_count", patrol_id, curr_row_count)
        )
        assert curr_row_count <= expected_row_count * 1.5
        return curr_row_count


def run(df: pd.DataFrame, patrol):
    if should_run(df):
        run_patrol(df, patrol)
