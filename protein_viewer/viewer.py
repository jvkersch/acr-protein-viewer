from pathlib import Path

from .app import create_app
from .metadata import load_metadata
from .loader import PDBLoader


def main():
    datadir = Path("data")
    metadata = load_metadata(datadir)
    loader = PDBLoader(datadir)

    app = create_app(metadata, loader)
    app.run_server(debug=True)


if __name__ == "__main__":
    main()
