import requests
import os


def get_user(user_id):
    patrol_url = os.environ.get("PANDA_PATROL_URL")
    if patrol_url:
        response = requests.get(f"{patrol_url}/user/{user_id}")
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return "Request failed with error: " + str(e)
        return response.json()

    return {}
