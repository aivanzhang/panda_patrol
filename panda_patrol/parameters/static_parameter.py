import os
from panda_patrol.parameters.utils.update_parameter import update_parameter


def static_parameter(parameter_id, patrol_id, value):
    patrol_url = os.environ.get("PANDA_PATROL_URL")
    patrol_user = os.environ.get("PANDA_PATROL_USER")
    if patrol_url and patrol_user:
        update_parameter(
            patrol_url, patrol_user, patrol_id, parameter_id, "static", value, value
        )
    return value
