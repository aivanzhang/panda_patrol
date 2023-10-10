import sys
import inspect
import os
from typing import TypedDict, Callable
from datetime import datetime
from io import StringIO
from contextlib import contextmanager
from panda_patrol.data.patrol_result import PandaResult, Status, Severity
from panda_patrol.parameters.utils.reset_parameters import reset_parameters


class PatrolContext(TypedDict):
    name: str
    severity: Severity
    store_logs: bool
    func: Callable


@contextmanager
def patrol_group(
    group_name: str,
):
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
        start = datetime.utcnow()
        patrol_logs = StringIO()
        status: Status = Status.SUCCESS
        exception: Exception = None
        return_value: any = None
        reset_parameters(group_name, context["patrol_dict"]["patrol"])

        if context["store_logs"]:
            sys.stdout = patrol_logs

        try:
            return_value = context["func"](context["patrol_dict"])
        except Exception as e:
            status = Status.FAILURE
            exception = e

        end = datetime.utcnow()
        sys.stdout = sys.__stdout__
        if context["store_logs"] or os.environ.get("PANDA_PATROL_ENV") == "dev":
            print(patrol_logs.getvalue().strip())

        PandaResult(
            patrol_group=group_name,
            patrol=context["name"],
            status=status,
            severity=context["severity"],
            patrol_code=inspect.getsource(context["func"]),
            logs=patrol_logs.getvalue().strip(),
            return_value=return_value,
            start_time=start,
            end_time=end,
            exception=exception,
        ).log()
