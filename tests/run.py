from panda_patrol.data.patrol_result import Severity
from panda_patrol.patrols import patrol_group
from panda_patrol.parameters import adjustable_parameter, static_parameter
import pandas as pd


def run_tests_on_dataframe(df):
    with patrol_group("numeric tests") as patrol:
        # Apply tests to the 'values' column and create new columns for results
        @patrol("is_positive", severity=Severity.INFO)
        def is_positive(patrol_id):
            postive_min = adjustable_parameter("is_positive", patrol_id, 0)
            df["is_positive"] = df["values"].apply(lambda num: num > postive_min)
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
