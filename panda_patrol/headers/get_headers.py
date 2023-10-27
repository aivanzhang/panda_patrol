import os


def get_headers():
    authorization_token = os.environ.get("PANDA_PATROL_SECRET_KEY")
    if authorization_token:
        return {"Authorization": f"Bearer {authorization_token}"}
    return None
