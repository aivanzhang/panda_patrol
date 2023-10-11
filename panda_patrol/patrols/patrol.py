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
from panda_patrol.users.get_user import get_user
from panda_patrol.utils.email_utils import send_failure_email


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

        # Setup for before executing
        reset_parameters(group_name, context["patrol_dict"]["patrol"])
        settings = get_settings(group_name, context["name"])
        should_run = True
        should_alert = True
        user_to_alert = None

        if bool(settings):
            if settings["silenced_until"]:
                silenced_until_time = datetime.fromisoformat(
                    settings["silenced_until"]
                ).replace(tzinfo=timezone.utc)
                if silenced_until_time > datetime.now(timezone.utc):
                    should_run = False

            if settings["assigned_to_person"]:
                user_to_alert = get_user(settings["assigned_to_person"])

            should_alert = settings["alerting"] and user_to_alert

        if context["store_logs"]:
            sys.stdout = patrol_logs
        if should_run:
            try:
                return_value = context["func"](context["patrol_dict"])
            except Exception as e:
                status = Status.FAILURE
                exception = e
        else:
            status = Status.SKIPPED

        sys.stdout = sys.__stdout__
        if context["store_logs"] or os.environ.get("PANDA_PATROL_ENV") == "dev":
            print(patrol_logs.getvalue().strip())
            if exception:
                print(exception)

        end = datetime.utcnow()

        patrol_info = {
            "patrol_group": group_name,
            "patrol": context["name"],
            "severity": context["severity"],
            "status": status,
            "logs": patrol_logs.getvalue().strip(),
            "return_value": return_value,
            "start_time": start,
            "end_time": end,
            "exception": exception,
        }
        PandaResult(**patrol_info).log()

        if status == Status.FAILURE and should_alert and user_to_alert:
            send_failure_email(
                user_to_alert["name"],
                user_to_alert["email"],
                patrolInfo=patrol_info,
            )
