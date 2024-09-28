from sys import argv
from pathlib import Path

from src.app import App


def main() -> None:
    app = App(Path(argv[1]), argv[2])
    app.run()


if __name__ == "__main__":
    main()
