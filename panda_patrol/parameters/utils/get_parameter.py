import requests
from panda_patrol.headers.get_headers import get_headers


def get_parameter(url, patrol_id, parameter_id, type):
    response = requests.get(
        f"{url}/patrol_parameters/{patrol_id['patrol_group']}/{patrol_id['patrol']}/{type}/{parameter_id}",
        headers=get_headers(),
    )
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Failed to get parameter value from the server")
    returnValue = response.json()
    return returnValue["value"] if "value" in returnValue else None
