from panda_patrol.data.patrol_result import Severity
from panda_patrol.patrols import patrol_group
import pandas as pd


def run_tests_on_dataframe(df):
    with patrol_group("numeric tests") as patrol:
        # Apply tests to the 'values' column and create new columns for results
        @patrol("is_positive", severity=Severity.INFO)
        def is_positive(patrol_id):
            print(patrol_id)
            df["is_positive"] = df["values"].apply(lambda num: num > 0)
            print(patrol_id, df)

            return "POSITIVE"

        @patrol("is_even", severity=Severity.INFO)
        def is_even(patrol_id):
            print(patrol_id)
            df["is_even"] = df["values"].apply(lambda num: num % 2 == 0)
            print(patrol_id, df)

            return "EVEN"


# Sample dataframe
data = {"values": [2, 4, 7, 9, 15, 16, 23, -5, -8]}
df = pd.DataFrame(data)

result_df = run_tests_on_dataframe(df)
print(result_df)
