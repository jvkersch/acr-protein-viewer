from pathlib import Path

from .app import create_app
from .io import load_structures
from .loader import PDBLoader


def main():
    datadir = Path("data")
    structures = load_structures(datadir)
    loader = PDBLoader(datadir)

    app = create_app(structures, loader)
    app.run_server(debug=True)


if __name__ == "__main__":
    main()
