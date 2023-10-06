import argparse
import uvicorn


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

    uvicorn.run(
        "panda_patrol.backend.app:app", host=args.host, port=args.port, reload=True
    )
