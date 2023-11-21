import pandas as pd
from panda_patrol.parameters import adjustable_parameter


def should_run(df: pd.DataFrame):
    if df.dtype == "object":
        date_column = pd.to_datetime(df, errors="coerce", format="mixed")
        return date_column.notnull().all()
    return df.dtype == "datetime64[ns]"


def run_patrol(df: pd.DataFrame, column, patrol):
    @patrol(f"Freshness: {column}")
    def freshness(patrol_id):
        latest_date = df[column].max()
        days_old = int(
            adjustable_parameter(
                "days-old",
                patrol_id,
                (pd.Timestamp.now() - pd.Timestamp(latest_date)).days or 1,
            )
        )

        assert pd.to_datetime(
            latest_date, errors="coerce", format="mixed"
        ) >= pd.Timestamp.now() - pd.Timedelta(days=days_old)

        return latest_date


def run(df: pd.DataFrame, patrol):
    for column in df.columns:
        if should_run(df[column]):
            run_patrol(df, column, patrol)
