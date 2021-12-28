import dash_bio as dashbio
from dash import dcc, html
import dash_bootstrap_components as dbc


_EMPTY_MOL3D = {
    "atoms": [],
    "bonds": [],
}
_EMPTY_STYLES = []


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
