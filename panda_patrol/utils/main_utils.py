import argparse


def main():
    parser = argparse.ArgumentParser(
        prog="python -m panda_patrol", description="Starts the panda patrol server."
    )

    parser.add_argument(
        "--port",
        "-p",
        type=int,
        help="The port to run the server on.",
        default=8000,
    )

    args = parser.parse_args()

    print(args.port)
