"""
Result from a data patrol run
"""
from datetime import datetime
import traceback
import requests
import os
from enum import Enum
from panda_patrol.headers.get_headers import get_headers


class Severity(Enum):
    """
    Severity of the patrol
    """

    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"

    def __repr__(self):
        return self.value


class Status(Enum):
    """
    Status of the patrol
    """

    SUCCESS = "success"
    FAILURE = "failure"
    SKIPPED = "skipped"

    def __repr__(self):
        return self.value


class PandaResult:
    """
    Result from a data patrol run

    Attributes:
    - patrol_group: Name of the group containing many patrols
    - patrol: Name of data rule that failed
    - status: Status of the patrol
    - severity: Severity of the patrol
    - logs: Logs from the patrol
    - start_time: UTC time of when the patrol started
    - return_value (optional): Return value of the patrol
    - patrol_code (optional): Code-related to the patrol that failed
    - exception (optional): Exception that was raised
    """

    def __init__(
        self,
        patrol_group: str,
        patrol: str,
        status: Status,
        severity: Severity,
        logs: str,
        start_time: datetime = None,
        end_time: datetime = None,
        return_value: str = None,
        patrol_code: str = None,
        exception: Exception = None,
    ):
        self.patrol_group = patrol_group
        self.patrol = patrol
        self.status = status
        self.severity = severity
        self.logs = logs
        self.start_time = start_time
        self.end_time = end_time

        # Optional attributes
        self.return_value = return_value
        self.patrol_code = patrol_code
        self.exception = exception

        super().__init__()

    def __str__(self):
        return f"{self.patrol_group}:{self.patrol} failed with severity {self.severity}"

    def __details__(self):
        return f"Code\n{self.patrol_code}\n\nReturn Value\n{self.return_value}\n\nException\n{self.exception}Logs\n{self.logs}\n\n"

    def log(self):
        """
        Log the result of the patrol. If patrol url is provided, send the information externally. Otherwise, log locally.
        """
        payload = {
            "patrol_group": self.patrol_group,
            "patrol": self.patrol,
            "status": self.status.value,
            "severity": self.severity.value,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "logs": self.logs or "",
            "return_value": self.return_value or "",
            "patrol_code": self.patrol_code or "",
            "exception": "".join(
                traceback.TracebackException.from_exception(self.exception).format()
            )
            if self.exception
            else "",
        }
        patrol_url = os.environ.get("PANDA_PATROL_URL")
        if patrol_url:
            response = requests.post(
                f"{patrol_url}/patrol/run", json=payload, headers=get_headers()
            )
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                return "Request failed with error: " + str(e)
        else:
            print(payload)
        return payload
