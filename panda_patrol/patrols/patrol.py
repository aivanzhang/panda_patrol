from typing import TypedDict, Callable
from contextlib import contextmanager
from panda_patrol.data.patrol_result import Severity
from panda_patrol.utils.patrol_utils import run_patrol, PatrolContext


class PatrolContext(TypedDict):
    name: str
    severity: Severity
    store_logs: bool
    func: Callable


@contextmanager
def patrol_group(group_name: str, dbt_model_uri=None):
    patrols: dict[str:PatrolContext] = dict()

    def patrol(
        name: str, severity: Severity = Severity.CRITICAL, store_logs: bool = True
    ):
        def patrol_decorator(func: Callable):
            patrol_id = f"{group_name}.{name}"
            patrols[patrol_id] = PatrolContext(
                name=name,
                severity=severity,
                store_logs=store_logs,
                func=func,
                patrol_dict={
                    "patrol_group": group_name,
                    "patrol": name,
                },
            )

        return patrol_decorator

    yield patrol

    for context in patrols.values():
        run_patrol(group_name, context, dbt_model_uri=dbt_model_uri)
