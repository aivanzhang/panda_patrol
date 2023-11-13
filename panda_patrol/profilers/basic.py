import pandas as pd
from ydata_profiling import ProfileReport
from panda_patrol.profilers import save_report


def basic_data_profile(df: pd.DataFrame, patrol_group: str, patrol: str):
    profile = ProfileReport(df, title="Profiling Report")
    save_report(profile.to_html(), patrol_group, patrol, "html")
