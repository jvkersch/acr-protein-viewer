import json


class Metadata:

    def __init__(self, sdata):
        self._sdata = sdata

    @property
    def acr_ids(self):
        return sorted(self._sdata)

    def get_matches(self, acr_id):
        return sorted(self._sdata[acr_id])

    def get_chains(self, acr_id, pdb_id):
        return sorted(self._sdata[acr_id][pdb_id])


def load_metadata(datadir):
    with open(datadir / "structures.json", encoding="utf-8") as fp:
        return Metadata(json.load(fp))
