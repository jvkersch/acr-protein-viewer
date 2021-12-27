import json

from .structures import Structures


def load_structures(datadir):
    with open(datadir / "structures.json", encoding="utf-8") as fp:
        return Structures(json.load(fp))
