import requests


def get_parameter(url, user, patrol_id, parameter_id, type):
    params = {
        "groupName": patrol_id["patrol_group"],
        "patrolName": patrol_id["patrol"],
        "type": type,
    }
    response = requests.get(
        f"{url}/patrol_parameters/{parameter_id}",
        params=params,
        headers={"user-id": user, "Content-Type": "application/json"},
    )
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Failed to get parameter value from the server")
    return response.json()["value"]
