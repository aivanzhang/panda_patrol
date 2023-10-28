import os
from dotenv import load_dotenv, find_dotenv
import uuid
from panda_patrol.constants import DEFAULT_PANDA_PATROL_URL
from panda_patrol.utils.init_utils import init_panda_patrol, print_see_dashboard

found_dotenv = find_dotenv()
if found_dotenv:
    load_dotenv(override=True)
    with open(found_dotenv, "a") as f:
        if not os.environ.get("PANDA_PATROL_URL"):
            f.write(f'PANDA_PATROL_URL="{DEFAULT_PANDA_PATROL_URL}"')
        if not os.environ.get("PANDA_PATROL_SECRET_KEY"):
            f.write(f'PANDA_PATROL_SECRET_KEY="public-{uuid.uuid4()}"')
else:
    with open(".env", "w+") as f:
        f.write(
            f'PANDA_PATROL_URL="{DEFAULT_PANDA_PATROL_URL}"\nPANDA_PATROL_SECRET_KEY="public-{uuid.uuid4()}"'
        )

load_dotenv(override=True)
init_panda_patrol()
print_see_dashboard()
