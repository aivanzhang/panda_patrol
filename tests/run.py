from panda_patrol.data.patrol_result import Severity
from panda_patrol.patrols import patrol_group
from panda_patrol.parameters import adjustable_parameter, static_parameter
from panda_patrol.profilers import save_report

# from ydata_profiling import ProfileReport
# from dataprofiler import Profiler
import json
import pandas as pd


class Test:
    def __init__(self) -> None:
        self.apple = 1

    def run_this(self):
        assert self.apple == 1


def run_tests_on_dataframe(df):
    with patrol_group("numeric tests") as patrol:
        # t = Test()
        # patrol("is_positive", severity=Severity.INFO)(t.run_this)

        # Apply tests to the 'values' column and create new columns for results
        @patrol("is_positive2", severity=Severity.INFO)
        def is_positive(patrol_id):
            postive_min = int(adjustable_parameter("is_positive", patrol_id, 0))
            static_postive_min = int(static_parameter("is_positive", patrol_id, 4))
            df["is_positive"] = df["values"].apply(lambda num: num > postive_min)
            # profile = Profiler(df)

            # Print the report using json to prettify.
            # report = profile.report(report_options={"output_format": "pretty"})
            # save_report(
            #     json.dumps(report, indent=4), "numeric tests", "is_positive", "json"
            # )

            # profile = ProfileReport(df, title="Profiling Report")
            # html_str = profile.to_html()
            # save_report(html_str, "numeric tests", "is_positive", "html")
            # json_str = profile.to_json()
            # save_report(json_str, "numeric tests", "is_positive", "json")

            # print(patrol_id, df)
            assert df["is_positive"].all()
            return "POSITIVE"

        # @patrol("is_even", severity=Severity.INFO)
        # def is_even(patrol_id):
        #     # print(patrol_id)
        #     df["is_even"] = df["values"].apply(lambda num: num % 2 == 0)
        #     # print(patrol_id, df)

        #     return "EVEN"


# Sample dataframe
data = {"values": [2, 4, 7, 9, 15, 16, 23, -5, -8]}
df = pd.DataFrame(data)

result_df = run_tests_on_dataframe(df)
# print(result_df)
