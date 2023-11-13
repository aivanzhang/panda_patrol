import requests
import os
from datetime import datetime
from panda_patrol.headers.get_headers import get_headers
from panda_patrol.constants import DEFAULT_PANDA_PATROL_URL


def save_report(report_string: str, patrol_group: str, patrol: str, report_format: str):
    """
    Uploads a report to the server.

    Args:
        report_string (str): The report string.
        patrol_group (str): Name of the patrol group.
        patrol (str): Name of the patrol.
        report_format (str): Format of the report. Supports 'html', 'json', and 'image'.
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
        if os.environ.get("PANDA_PATROL_URL") == DEFAULT_PANDA_PATROL_URL:
            payload.pop("report", None)
            response = requests.get(
                f"{patrol_url}/get_presigned_profile_url",
                json=payload,
                headers=get_headers(),
            )
            try:
                response.raise_for_status()
                response = response.json()
                files = {"file": ("profile", report_string)}
                aws_upload_response = requests.post(
                    response["url"], data=response["fields"], files=files
                )
                return aws_upload_response
            except requests.exceptions.HTTPError as e:
                print("Failed to upload report.")

        else:
            response = requests.post(f"{patrol_url}/profile", json=payload)
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                print("Failed to upload report.")

            return response.json()

    return None
