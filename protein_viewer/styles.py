from matplotlib.colors import LinearSegmentedColormap, rgb2hex


MPL_COLORS = [
    '#1f77b4',
    '#ff7f0e',
    '#2ca02c',
    '#d62728',
    '#9467bd',
    '#8c564b',
    '#e377c2',
    '#7f7f7f',
    '#bcbd22',
    '#17becf'
]

ALPHAFOLD_CMAP = LinearSegmentedColormap.from_list(
    "alphafold",
    [(0.0, "red"),
     (0.5, "orange"),
     (0.7, "yellow"),
     (0.9, "cornflowerblue"),
     (1.0, "blue")])


def get_alphafold_style(bfactors):
    return [{
        "visualization_type": "cartoon",
        "color": _alphafold_mapper(b),
    } for b in bfactors]


def get_chain_style(atomdata):

    def offset(c):
        return (ord(c) - ord("A")) % len(MPL_COLORS)

    return [{
        "visualization_type": "cartoon",
        "color": MPL_COLORS[offset(atom["chain"])],
    } for atom in atomdata]


def _alphafold_mapper(bfactor):
    return rgb2hex(ALPHAFOLD_CMAP(bfactor/100))
