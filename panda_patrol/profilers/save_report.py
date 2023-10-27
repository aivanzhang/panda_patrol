import requests
import os
from datetime import datetime
from panda_patrol.headers.get_headers import get_headers


def save_report(report_string: str, patrol_group: str, patrol: str, report_format: str):
    """
    Uploads a report to the server.

    Args:
        report_string (str): The report string.
        patrol_group (str): Name of the patrol group.
        patrol (str): Name of the patrol.
        report_format (str): Format of the report. Supports 'html' or 'json'.
    """

    payload = {
        "patrol_group": patrol_group,
        "patrol": patrol,
        "report": report_string,
        "format": report_format,
        "time": str(datetime.now()),
    }

    patrol_url = os.environ.get("PANDA_PATROL_URL")
    if patrol_url:
        response = requests.post(
            f"{patrol_url}/profile", json=payload, headers=get_headers()
        )

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Failed to upload report.")

    return response.json()
