import os
import pathlib

import numpy as np
from dash_bio_utils import PdbParser, create_mol3d_style
from parmed.residue import AminoAcidResidue

RESIDUE_SYMBOLS = {
    res.abbr: res.symbol for res in AminoAcidResidue.all_residues
}


class PDBLoader:

    def __init__(self, datadir):
        self._datadir = pathlib.Path(datadir)

    def load_pdb(self, pdb_id, chain=None):
        if chain:
            fname = f"{pdb_id}_{chain}.pdb"
        else:
            fname = f"{pdb_id}.pdb"

        return self._load_pdb(fname)

    def get_available_chains(self, pdb_id):
        chain_ids = []
        for p in self._datadir.glob(f"{pdb_id}_*.pdb"):
            fname = os.path.basename(p)
            chain_id = os.path.splitext(fname)[0].split("_")[1]
            chain_ids.append(chain_id)
        return chain_ids

    def _load_pdb(self, fname):

        parser = PdbParser(str(self._datadir / fname))

        # Atom-level data
        mol3d = parser.mol3d_data()
        bfactor = [a.bfactor for a in parser.atoms]

        # Residue (C-alpha) data
        backbone = [a for a in parser.atoms if a.name == "CA"]
        sequence = ''.join(RESIDUE_SYMBOLS[a.residue.name] for a in backbone)
        positions = np.asarray([[a.xx, a.xy, a.xz] for a in backbone])

        return mol3d, bfactor, sequence, positions
