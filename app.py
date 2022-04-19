import dash
import dash_bootstrap_components as dbc
import warnings
warnings.filterwarnings("ignore")

# bootstrap theme
# https://bootswatch.com/superhero/
external_stylesheets = [dbc.themes.PULSE]

app = dash.Dash(__name__, suppress_callback_exceptions=True,
                external_stylesheets=external_stylesheets)

server = app.server
# app.config.suppress_callback_exceptions = True
