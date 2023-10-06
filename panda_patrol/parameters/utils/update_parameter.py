import requests


def update_parameter(url, patrol_id, parameter_id, type, default_value, value):
    payload = {
        "groupName": patrol_id["patrol_group"],
        "patrolName": patrol_id["patrol"],
        "parameterId": parameter_id,
        "value": value,
        "defaultValue": default_value,
        "type": type,
    }
    response = requests.post(
        f"{url}/patrol_parameters",
        json=payload,
    )

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Failed to store parameter value in server")
