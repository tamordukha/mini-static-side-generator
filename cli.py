import argparse
from builder import build, clean, serve


def parse_args():
    parser = argparse.ArgumentParser(description="Static Site Generator CLI")

    parser.add_argument(
        "command",
        choices=["build", "clean", "serve", "rebuild"],
        help="Команда: build, clean, serve, rebuild"
    )
    return parser.parse_args()

args = parse_args()
if args.command == "build":
    build()

elif args.command == "rebuild":
    clean()
    build()

elif args.command == "clean":
    clean()

elif args.command == "serve":
    serve()