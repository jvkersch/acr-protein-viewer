import dash
import dash_bio as dashbio
from dash import dcc, html
from dash.dependencies import Input, Output

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

    app = dash.Dash(__name__)

    app.layout = html.Div([
        dcc.Dropdown(
            id="acr-dropdown",
            options=_to_dropdown(structures.acr_ids),
            value="anti_CRISPR0001",
        ),
        dcc.Dropdown(
            id="pdb-dropdown",
            options=_to_dropdown(default_pdbs),
            value=default_pdb,
        ),
        dcc.Dropdown(
            id="chain-dropdown",
            options=_to_dropdown(default_chains),
            value=default_chain,
        ),
        html.Hr(),
        html.Div(id="hidden-div", style={"display": "none"}),
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
    ])

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
        chain_ids = structures.get_chains(acr_id, pdb_id)
        return chain_ids[0], _to_dropdown(chain_ids)

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
