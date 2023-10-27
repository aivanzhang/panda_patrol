import requests
import os
from panda_patrol.headers.get_headers import get_headers


def reset_parameters(patrol_group, patrol):
    payload = {
        "patrol_group": patrol_group,
        "patrol": patrol,
    }
    patrol_url = os.environ.get("PANDA_PATROL_URL")
    if patrol_url:
        response = requests.post(
            f"{patrol_url}/reset_parameters", json=payload, headers=get_headers()
        )
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return "Request failed with error: " + str(e)
    else:
        print(payload)
    return payload
