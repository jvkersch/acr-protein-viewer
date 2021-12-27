import json
import os
import pathlib


import click
import openpyxl


@click.command()
@click.argument("excel", type=click.Path(exists=True, path_type=pathlib.Path))
@click.argument("pdb-directory", type=click.Path(
    file_okay=False, dir_okay=True, path_type=pathlib.Path))
def main(excel, pdb_directory):

    structures = {}

    wb = openpyxl.load_workbook(excel)
    ws = wb["Set A and C"]

    row_iter = ws.iter_rows(values_only=True)
    next(row_iter)  # Skip header

    for row in row_iter:
        acr_id = row[0]
        pdb_ids = _normalize_pdb_ids(row[-2])
        structures[acr_id] = pdb_structures = {}

        for pdb_id in pdb_ids:
            chain_ids = _find_chains(pdb_directory, pdb_id)
            pdb_structures[pdb_id] = chain_ids

    with open(pdb_directory / "structures.json", "wt", encoding="utf-8") as fp:
        json.dump(structures, fp, indent=2)


def _normalize_pdb_ids(s):
    pdb_ids = []
    for item in s.split(";"):
        item = item.strip()
        item = item.split('-')[0]
        if not item:
            continue
        pdb_ids.append(item)
    return pdb_ids


def _find_chains(directory, pdb_id):
    pdb_glob = directory.glob(f"{pdb_id}_*.pdb")
    return [_get_chain_id(match) for match in pdb_glob]


def _get_chain_id(fname):
    fname = os.path.basename(fname)
    base = os.path.splitext(fname)[0]
    return base.split('_')[1]


if __name__ == "__main__":
    main()
