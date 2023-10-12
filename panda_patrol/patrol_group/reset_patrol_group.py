import requests
import os


def reset_patrol_group(patrol_group):
    payload = {
        "patrol_group": patrol_group,
    }
    patrol_url = os.environ.get("PANDA_PATROL_URL")
    if patrol_url:
        response = requests.post(f"{patrol_url}/reset_patrol_group", json=payload)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return "Request failed with error: " + str(e)
    else:
        print(payload)
    return payload
