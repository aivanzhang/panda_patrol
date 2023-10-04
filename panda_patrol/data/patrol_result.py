"""
Result from a data patrol run
"""
import traceback
import requests
from enum import Enum
from panda_patrol.conf import settings


class Severity(Enum):
    """
    Severity of the patrol
    """

    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"


class Status(Enum):
    """
    Status of the patrol
    """

    SUCCESS = "success"
    FAILURE = "failure"
    SKIPPED = "skipped"


class PandaResult:
    """
    Result from a data patrol run

    Attributes:
    - troop: Name of the group containing many patrols
    - patrol: Name of data rule that failed
    - severity: Severity of the patrol
    - logs: Logs from the patrol
    - returnValue (optional): Return value of the patrol
    - patrol_code (optional): Code-related to the patrol that failed
    - exception (optional): Exception that was raised
    """

    def __init__(
        self,
        troop: str,
        patrol: str,
        status: Status,
        severity: Severity,
        logs: str,
        returnValue: str = None,
        patrol_code: str = None,
        exception: Exception = None,
    ):
        # Get current runtime, set status to failure
        self.troop = troop
        self.patrol = patrol
        self.status = status
        self.severity = severity
        self.logs = logs

        # Optional attributes
        self.returnValue = returnValue
        self.patrol_code = patrol_code
        self.exception = exception

        super().__init__()

    def __str__(self):
        return f"{self.troop}:{self.patrol} failed with severity {self.severity}"

    def __details__(self):
        return f"Code\n{self.patrol_code}\n\nReturn Value\n{self.returnValue}\n\nException\n{self.exception}Logs\n{self.logs}\n\n"

    def log(self):
        """
        Log the result of the patrol. If patrol url is provided, send the information externally. Otherwise, log locally.
        """
        payload = {
            "troop": self.troop,
            "patrol": self.patrol,
            "status": self.status,
            "severity": self.severity,
            "logs": self.logs,
            "returnValue": self.returnValue,
            "patrol_code": self.patrol_code,
            "exception": "\n".join(traceback.format_tb(self.exception.__traceback__)),
        }
        if settings.PATROL_URL:
            requests.post(settings.PATROL_URL, data=payload)
        return payload
