import argparse
import os
import uvicorn
import json
import webbrowser


def main():
    parser = argparse.ArgumentParser(
        prog="python -m panda_patrol", description="Starts the panda patrol server."
    )
    parser.add_argument(
        "--host",
        type=str,
        default="localhost",
        help="The host to run the server on.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="The port to run the server on.",
    )
    args = parser.parse_args()

    url = "http://{}:{}".format(args.host, args.port)

    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
    )
    with open(os.path.join(__location__, "../backend/static/config.json"), "w") as f:
        json.dump({"PANDA_PATROL_URL": url}, f)

    webbrowser.open(url)
    uvicorn.run(
        "panda_patrol.backend.app:app", host=args.host, port=args.port, reload=True
    )
