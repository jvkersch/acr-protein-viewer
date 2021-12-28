from dash import dcc
import dash_bootstrap_components as dbc

from .utils import to_dropdown


def controls_factory(acr_values):
    controls = dbc.Row([
        dbc.Col([
            dbc.Label("Prediction", html_for="acr-dropdown"),
            dcc.Dropdown(
                id="acr-dropdown",
                options=to_dropdown(acr_values),
                value=acr_values[0],
                clearable=False,
            ),
        ], width=3),
        dbc.Col([
            dbc.Label("Ground Truth", html_for="pdb-drowndown"),
            dcc.Dropdown(
                id="pdb-dropdown",
                options=[],
                clearable=False,
            ),
        ], width=3),
        dbc.Col([
            dbc.Label("Ground Truth Chain"),
            dcc.Dropdown(
                id="chain-dropdown",
                options=[],
                clearable=False,
            ),
        ], width=3),
    ], className="g-3")
    return controls
