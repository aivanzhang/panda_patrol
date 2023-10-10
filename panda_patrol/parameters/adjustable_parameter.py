from panda_patrol.parameters.utils.update_parameter import update_parameter
from panda_patrol.parameters.utils.get_parameter import get_parameter
import os


def adjustable_parameter(parameter_id, patrol_id, value):
    patrol_url = os.environ.get("PANDA_PATROL_URL")
    if patrol_url:
        param_value = get_parameter(patrol_url, patrol_id, parameter_id, "adjustable")
        if param_value == None:
            update_parameter(
                patrol_url,
                patrol_id,
                parameter_id,
                "adjustable",
                value,
            )
        else:
            update_parameter(
                patrol_url,
                patrol_id,
                parameter_id,
                "adjustable",
                param_value,
            )
            return param_value
    return value
