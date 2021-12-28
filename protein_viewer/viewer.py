from pathlib import Path

from flask import Flask

from .app import create_app
from .metadata import load_metadata
from .loader import PDBLoader


def main():
    server = Flask(__name__)

    datadir = Path("data")
    metadata = load_metadata(datadir)
    loader = PDBLoader(datadir)

    app = create_app(server, metadata, loader)
    return server, app


if __name__ == "__main__":
    server, app = main()
    app.run_server(debug=True)
