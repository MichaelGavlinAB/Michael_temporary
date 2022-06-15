import plotly.express as px
import pandas as pd
import numpy as np
from skimage import io
import dash
import dash_bootstrap_components as dbc
from dash import html
# import dash_html_components as html
# import dash_core_components as dcc
from dash import dcc
from dash.dependencies import Output, Input
import plotly.graph_objs as go
from dash import Dash, dcc               # pip install dash
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components
pd.options.plotting.backend = "plotly"

# img = io.imread('/home/michael/Desktop/pics/QUAD_1601568800054435.png')
# fig = px.imshow(img)
# fig.show()

################################################################################################
"""
Michael function - Read CSV file and extract data
"""
dff = pd.read_csv('/home/michael/Desktop/Recordings/EBA/618e558a8fa38d33e9d69d42/2020.10.09_at_15.37.30_camera-mi_5022_extract_1602259269281220us_to_1602259311323110us_id0.csv')
# dff_relevant = dff [['MTS.Package.TimeStamp','MFC5xx Device.VDY.VehDyn.Longitudinal.Velocity','MFC5xx Device.VDY.VehDyn.Longitudinal.varAccel','MFC5xx Device.VDY.VehDyn.Lateral.YawRate.YawRate']]
print("relevant data is: \n" , dff)

header = []
for ii in dff:
    header.append(ii)
print("Header is: \n",header)

################################################################################################

# If you prefer to run the code online instead of on your computer click:
# https://github.com/Coding-with-Adam/Dash-by-Plotly#execute-code-in-browser

# Build your components
app = Dash(__name__, external_stylesheets=[dbc.themes.VAPOR])
mytitle = dcc.Markdown(children='# Mapi + CSV reader display tool')
mytitle2 = dcc.Markdown(children='# System engineering')
mygraph = dcc.Graph(figure={})
dropdown = dcc.Dropdown(options=header,
                        clearable=False)

# Customize your own Layout
app.layout = dbc.Container([mytitle , mygraph, dropdown , mytitle2])

# Callback allows components to interact
@app.callback(
    Output(mygraph, component_property='figure'),
    Input(dropdown, component_property='value')
)

def update_graph(user_input):  # function arguments come from the component property of the Input
    fig = px.scatter(data_frame=dff, x=header[0], y=user_input)

    return fig  # returned objects are assigned to the component property of the Output

# Run app
if __name__=='__main__':
    app.run_server(port=8053)