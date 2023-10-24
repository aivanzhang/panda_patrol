import sys
import inspect
import os
from typing import TypedDict, Callable
from datetime import datetime, timezone
from io import StringIO
from contextlib import contextmanager
from panda_patrol.data.patrol_result import PandaResult, Status, Severity
from panda_patrol.parameters.utils.reset_parameters import reset_parameters
from panda_patrol.settings.get_settings import get_settings
from panda_patrol.utils.func_utils import extract_function_source


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
        start = datetime.utcnow()
        patrol_logs = StringIO()
        status: Status = Status.SUCCESS
        exception: Exception = None
        return_value: any = None

        # Setup for before executing
        reset_parameters(group_name, context["patrol_dict"]["patrol"])
        settings = get_settings(group_name, context["name"])
        should_run = True

        if bool(settings):
            if settings["silenced_until"]:
                silenced_until_time = datetime.fromisoformat(
                    settings["silenced_until"]
                ).replace(tzinfo=timezone.utc)
                if silenced_until_time > datetime.now(timezone.utc):
                    should_run = False

        if context["store_logs"]:
            sys.stdout = patrol_logs
        if should_run:
            try:

                def data_test_wrapper(**kwargs):
                    function_parameters = context["func"].__code__.co_varnames[
                        : context["func"].__code__.co_argcount
                    ]
                    if "patrol_id" in function_parameters:
                        return context["func"](
                            patrol_id=context["patrol_dict"], **kwargs
                        )
                    else:
                        return context["func"](**kwargs)

                return_value = data_test_wrapper()
            except Exception as e:
                status = Status.FAILURE
                exception = e
        else:
            status = Status.SKIPPED

        sys.stdout = sys.__stdout__
        if context["store_logs"]:
            print(patrol_logs.getvalue().strip())
            if exception:
                print(exception)

        patrol_code = "# Could not retrieve patrol code. Note that if you're using dbt the patrol code will not be available."
        try:
            patrol_code = inspect.getsource(context["func"])
        except:
            pass
        if dbt_model_uri:
            try:
                file_path = os.path.join(os.getcwd(), f"models/{dbt_model_uri}.py")
                patrol_code = extract_function_source(
                    file_path, context["func"].__name__
                )
            except:
                pass

        end = datetime.utcnow()

        patrol_info = {
            "patrol_group": group_name,
            "patrol": context["name"],
            "patrol_code": patrol_code,
            "severity": context["severity"],
            "status": status,
            "logs": patrol_logs.getvalue().strip(),
            "return_value": f"{return_value}",
            "start_time": start,
            "end_time": end,
            "exception": exception,
        }
        PandaResult(**patrol_info).log()
