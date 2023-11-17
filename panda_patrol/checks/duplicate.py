import pandas as pd
from panda_patrol.parameters import adjustable_parameter


def should_run(df: pd.DataFrame):
    return True


def run_patrol(df: pd.DataFrame, column, patrol):
    @patrol(f"Duplicates: {column}")
    def duplicates(patrol_id):
        percent_duplicates = df[column].duplicated(keep=False).mean()
        assert percent_duplicates <= float(
            adjustable_parameter("percent_duplicates", patrol_id, percent_duplicates)
        )
        return percent_duplicates


def run(df: pd.DataFrame, patrol):
    for column in df.columns:
        if should_run(df[column]):
            run_patrol(df, column, patrol)
