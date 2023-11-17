import pandas as pd
from panda_patrol.parameters import adjustable_parameter


def should_run(df: pd.DataFrame):
    return True


def run_patrol(df: pd.DataFrame, column, patrol):
    @patrol(f"Completeness: {column}")
    def completeness(patrol_id):
        percent_null = df[column].isnull().mean()
        assert percent_null <= float(
            adjustable_parameter("percent_null", patrol_id, percent_null)
        )
        return percent_null


def run(df: pd.DataFrame, patrol):
    for column in df.columns:
        if should_run(df[column]):
            run_patrol(df, column, patrol)
