import os
from dotenv import load_dotenv

load_dotenv(override=True)
# Set default values for environment variables
os.environ.setdefault("PANDA_PATROL_ENV", "dev")
os.environ.setdefault("PANDA_DATABASE_URL", "sqlite:///panda_patrol.db")
