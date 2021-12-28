import dash
import dash_bio as dashbio
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from tmtools import tm_align

from .styles import get_alphafold_style, get_chain_style
from .transform import affine_transform, combine_moldata


_EMPTY_MOL3D = {
    "atoms": [],
    "bonds": [],
}
_EMPTY_STYLES = []


def _to_dropdown(values):
    return [
        {"label": value, "value": value} for value in values
    ]


def create_app(structures, loader, default_acr="anti_CRISPR0001"):

    default_pdbs = structures.get_matches(default_acr)
    default_pdb = default_pdbs[0]
    default_chains = structures.get_chains(default_acr, default_pdb)
    default_chain = default_chains[0]  # replace with best chain

    app = dash.Dash(
        __name__,
        external_stylesheets=[dbc.themes.BOOTSTRAP]
    )

    controls = dbc.Row([
        dbc.Col([
            dbc.Label("Prediction", html_for="acr-dropdown"),
            dcc.Dropdown(
                id="acr-dropdown",
                options=_to_dropdown(structures.acr_ids),
                value="anti_CRISPR0001",
                clearable=False,
            ),
        ], width=3),
        dbc.Col([
            dbc.Label("Ground Truth", html_for="pdb-drowndown"),
            dcc.Dropdown(
                id="pdb-dropdown",
                options=_to_dropdown(default_pdbs),
                value=default_pdb,
                clearable=False,
            ),
        ], width=3),
        dbc.Col([
            dbc.Label("Ground Truth Chain"),
            dcc.Dropdown(
                id="chain-dropdown",
                options=_to_dropdown(default_chains),
                value=default_chain,
                clearable=False,
            ),
        ], width=3),
    ], className="g-3")

    graphs = dbc.Row([
        dbc.Col([
            dcc.Loading(
                id="loading-1",
                type="default",
                children=html.Div([
                    html.Div([
                        dashbio.Molecule3dViewer(
                            id='plddt-molecule-viewer',
                            modelData=_EMPTY_MOL3D,
                            styles=_EMPTY_STYLES,
                        ),
                    ], style={'display': 'inline-block'}),
                    html.Div([
                        dashbio.Molecule3dViewer(
                            id='align-molecule-viewer',
                            modelData=_EMPTY_MOL3D,
                            styles=_EMPTY_STYLES,
                        ),
                    ], style={'display': 'inline-block'}),
                ]),
            ),
        ]),
    ])

    app.layout = dbc.Container([
        controls,
        graphs,
    ], fluid=True)

    @app.callback(
        Output("pdb-dropdown", "value"),
        Output("pdb-dropdown", "options"),
        Input("acr-dropdown", "value"),
    )
    def update_selectable_pdbs(acr_id):
        pdb_ids = structures.get_matches(acr_id)
        return pdb_ids[0], _to_dropdown(pdb_ids)

    @app.callback(
        Output("chain-dropdown", "value"),
        Output("chain-dropdown", "options"),
        Input("acr-dropdown", "value"),
        Input("pdb-dropdown", "value"),
    )
    def update_selectable_chains(acr_id, pdb_id):

        scores = _get_chains_with_scores(structures, loader, acr_id, pdb_id)
        scores = {chain: score for chain, score in scores.items() if score > 0}

        sorted_chains = sorted(scores, key=lambda ch: scores[ch], reverse=True)
        dropdown_labels = [
            {"label": f"{chain} (TM {scores[chain]:.02f})", "value": chain}
            for chain in sorted_chains
        ]

        return sorted_chains[0], dropdown_labels

    @app.callback(
        Output("plddt-molecule-viewer", "modelData"),
        Output("plddt-molecule-viewer", "styles"),
        Input("acr-dropdown", "value"),
    )
    def update_molecule_viewer(acr_id):

        mol3d, bfactors, sequence, positions = loader.load_pdb(acr_id)
        style = get_alphafold_style(bfactors)

        return mol3d, style

    @app.callback(
        Output("align-molecule-viewer", "modelData"),
        Output("align-molecule-viewer", "styles"),
        Input("acr-dropdown", "value"),
        Input("pdb-dropdown", "value"),
        Input("chain-dropdown", "value"),
    )
    def update_comparison_viewer(acr_id, pdb_id, chain_id):

        mol3d1, _, sequence1, positions1 = loader.load_pdb(acr_id)
        mol3d2, _, sequence2, positions2 = loader.load_pdb(pdb_id, chain_id)

        res = tm_align(positions1, positions2, sequence1, sequence2)
        mol3d1 = affine_transform(mol3d1, res.u, res.t)

        moldata = combine_moldata(mol3d1, mol3d2)
        styles = get_chain_style(moldata["atoms"])

        return moldata, styles

    return app


def _get_chains_with_scores(structures, loader, acr_id, pdb_id):

    mol3d1, _, sequence1, positions1 = loader.load_pdb(acr_id)

    chain_ids = structures.get_chains(acr_id, pdb_id)
    tm_scores = {}
    for chain_id in chain_ids:
        mol3d2, _, sequence2, positions2 = loader.load_pdb(pdb_id, chain_id)
        if len(positions2) > 0:
            res = tm_align(positions1, positions2, sequence1, sequence2)
            score = res.tm_norm_chain1
        else:
            score = 0.0
        tm_scores[chain_id] = score

    return tm_scores
