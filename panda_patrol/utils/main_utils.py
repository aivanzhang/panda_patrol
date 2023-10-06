import argparse
import uvicorn
from panda_patrol.backend.app import app


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

    uvicorn.run(app, host=args.host, port=args.port)
