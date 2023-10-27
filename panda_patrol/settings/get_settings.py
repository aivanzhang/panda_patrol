import requests
import os
from panda_patrol.headers.get_headers import get_headers


def get_settings(patrol_group, patrol):
    patrol_url = os.environ.get("PANDA_PATROL_URL")
    if patrol_url:
        response = requests.get(
            f"{patrol_url}/patrol_settings/{patrol_group}/{patrol}",
            headers=get_headers(),
        )
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return "Request failed with error: " + str(e)
        return response.json()

    return {}
