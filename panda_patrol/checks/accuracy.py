import pandas as pd
from panda_patrol.parameters import adjustable_parameter


def should_run(df: pd.DataFrame):
    if df.dtype == "object":
        return False
    return df.dtype == "int64" or df.dtype == "float64"


def run_patrol(df: pd.DataFrame, column, patrol):
    @patrol(f"Accuracy: {column}")
    def accuracy(patrol_id):
        minimum = df[column].min()
        maximum = df[column].max()
        assert float(adjustable_parameter("min-value", patrol_id, minimum)) <= minimum
        assert float(adjustable_parameter("max-value", patrol_id, maximum)) >= maximum

        return f"min: {minimum}, max: {maximum}"


def run(df: pd.DataFrame, patrol):
    for column, column_type in df.dtypes.items():
        if should_run(column_type):
            run_patrol(df, column, patrol)
