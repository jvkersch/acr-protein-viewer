from copy import deepcopy

import numpy as np


def affine_transform(moldata, A, v):
    new_moldata = deepcopy(moldata)
    for atom in new_moldata["atoms"]:
        atom["positions"] = np.dot(atom["positions"], A.T) + v
    return new_moldata


def combine_moldata(m1, m2):
    m1 = deepcopy(m1)
    m2 = deepcopy(m2)

    # Renumber chains
    for atom in m1["atoms"]:
        atom["chain"] = "A"
    for atom in m2["atoms"]:
        atom["chain"] = "B"

    # Offset indices in chain 2
    n_atoms1 = len(m1["atoms"])
    for atom in m2["atoms"]:
        atom["serial"] += n_atoms1
    for bond in m2["bonds"]:
        bond["atom1_index"] += n_atoms1
        bond["atom2_index"] += n_atoms1

    # Join both sets
    m1["atoms"].extend(m2["atoms"])
    m1["bonds"].extend(m2["bonds"])

    return m1
