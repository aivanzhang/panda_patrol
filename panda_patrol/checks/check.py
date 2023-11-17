import pandas as pd
import inspect
from panda_patrol.patrols import patrol_group
from panda_patrol.checks.utils import import_all_modules_from_directory


def check(df: pd.DataFrame, patrol_group_name: str):
    checks = import_all_modules_from_directory()
    with patrol_group(patrol_group_name) as patrol:
        for check in checks.keys():
            check_func = checks[check].run_patrol
            if "column" in inspect.signature(check_func).parameters.keys():
                for column in df.columns:
                    if checks[check].should_run(df[column]):
                        checks[check].run_patrol(df, column, patrol)
            else:
                if checks[check].should_run(df):
                    checks[check].run_patrol(df, patrol)
