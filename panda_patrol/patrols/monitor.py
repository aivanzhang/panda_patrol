from datetime import datetime
from contextlib import contextmanager
from io import StringIO
import sys
from panda_patrol.data.patrol_result import PandaResult, Status, Severity


@contextmanager
def monitor(group_name: str):
    start = datetime.utcnow()
    patrol_logs = StringIO()
    status: Status = Status.SUCCESS
    exception: Exception = None
    sys.stdout = patrol_logs
    try:
        yield
    except Exception as e:
        status = Status.FAILURE
        exception = e
    sys.stdout = sys.__stdout__

    print(patrol_logs.getvalue().strip())
    if exception:
        print(exception)

    end = datetime.utcnow()

    patrol_info = {
        "patrol_group": group_name,
        "patrol": "Run Status",
        "patrol_code": None,
        "severity": Severity.CRITICAL,
        "status": status,
        "logs": patrol_logs.getvalue().strip(),
        "return_value": None,
        "start_time": start,
        "end_time": end,
        "exception": exception,
    }
    PandaResult(**patrol_info).log()
    if exception:
        raise exception
