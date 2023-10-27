import requests
from panda_patrol.headers.get_headers import get_headers


def update_parameter(url, patrol_id, parameter_id, type, value):
    payload = {
        "patrol_group": patrol_id["patrol_group"],
        "patrol": patrol_id["patrol"],
        "parameter_id": parameter_id,
        "value": f"{value}",
        "type": type,
        "is_active": True,
    }
    response = requests.post(
        f"{url}/patrol_parameters",
        json=payload,
        headers=get_headers(),
    )

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Failed to store parameter value in server")
    return
