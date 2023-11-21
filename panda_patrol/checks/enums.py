import pandas as pd
from panda_patrol.parameters import adjustable_parameter


def should_run(df: pd.DataFrame):
    if df.dtype == "object":
        return False
    return (df.nunique() / df.count()) < 0.3


def run_patrol(df: pd.DataFrame, column, patrol):
    @patrol(f"ENUM: {column}")
    def enums(patrol_id):
        unique_values = df[column].unique()
        assert len(unique_values) <= int(
            adjustable_parameter("expected_enums", patrol_id, len(unique_values))
        )
        return unique_values


def run(df: pd.DataFrame, patrol):
    for column in df.columns:
        if should_run(df[column]):
            run_patrol(df, column, patrol)
