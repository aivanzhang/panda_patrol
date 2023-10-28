import os
import requests
from panda_patrol.constants import DEFAULT_PANDA_PATROL_URL
from panda_patrol.headers.get_headers import get_headers


def init_panda_patrol():
    patrol_url = os.environ.get("PANDA_PATROL_URL")
    secret_key = os.environ.get("PANDA_PATROL_SECRET_KEY")

    if patrol_url == DEFAULT_PANDA_PATROL_URL and secret_key.startswith("public-"):
        print(
            "WARNING: You are using the default Panda Patrol URL and a public key. This is not recommended for production."
        )
        response = requests.post(f"{patrol_url}/organization", headers=get_headers())
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 409:
                pass
            else:
                raise e


def print_see_dashboard():
    patrol_url = os.environ.get("PANDA_PATROL_URL")
    secret_key = os.environ.get("PANDA_PATROL_SECRET_KEY")

    if patrol_url == DEFAULT_PANDA_PATROL_URL and secret_key.startswith("public-"):
        frontend_url = "https://panda-patrol.vercel.app/"
        print(
            f"\033[95m\033[92mSee your Panda Patrol dashboard here: \033[1m\033[4m{frontend_url}/public/{secret_key}\033[0m"
        )
