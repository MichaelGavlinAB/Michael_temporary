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
dff_relevant = dff [['MTS.Package.TimeStamp','MFC5xx Device.VDY.VehDyn.Longitudinal.Velocity','MFC5xx Device.VDY.VehDyn.Longitudinal.varAccel','MFC5xx Device.VDY.VehDyn.Lateral.YawRate.YawRate']]
print("relevant data is: \n" , dff_relevant)

header = []
for ii in dff_relevant:
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
dropdown = dcc.Dropdown(options=[header[0],header[1],header[2],header[3]],
                        clearable=False)

# Customize your own Layout
app.layout = dbc.Container([mytitle , mygraph, dropdown , mytitle2])

# Callback allows components to interact
@app.callback(
    Output(mygraph, component_property='figure'),
    Input(dropdown, component_property='value')
)

# def update_graph(user_input):  # function arguments come from the component property of the Input
#     if user_input == 'Bar Plot':
#         fig = px.bar(data_frame=dff_pandas, x="a", y="b")
#
#     elif user_input == 'Scatter Plot':
#         fig = px.scatter(data_frame=dff_pandas, x="a", y="b")
#     return fig  # returned objects are assigned to the component property of the Output

def update_graph(user_input):  # function arguments come from the component property of the Input

    if user_input == header[0]:
        print(header[0])
        fig = px.scatter(data_frame=dff_relevant, x=header[0], y=header[0])
    elif user_input == header[1]:
        print(header[1])
        fig = px.scatter(data_frame=dff_relevant, x=header[0], y=header[1])
    elif user_input == header[2]:
        print(header[2])
        fig = px.scatter(data_frame=dff_relevant, x=header[0], y=header[2])
    elif user_input == header[3]:
        print(header[3])
        fig = px.scatter(data_frame=dff_relevant, x=header[0], y=header[3])
    return fig  # returned objects are assigned to the component property of the Output


# Run app
if __name__=='__main__':
    app.run_server(port=8053)