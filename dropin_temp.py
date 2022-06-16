import base64
import datetime
import io
import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table
import plotly.express as px
import pandas as pd

#############3
""""
temporary read header
"""""

dff = pd.read_csv('/home/michael/Desktop/Recordings/EBA/618e558a8fa38d33e9d69d42/2020.10.09_at_15.37.30_camera-mi_5022_extract_1602259269281220us_to_1602259311323110us_id0.csv')
print("relevant data is: \n" , dff)
print("Header2222 is \n" , dff.columns.tolist())

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Markdown(children='# Mapi + CSV reader display tool'),
    dcc.Graph(id='mygraph' , figure={}),
    dcc.Dropdown(id = 'dropdown' , options=dff.columns.tolist() , clearable=False),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),

    html.Div(id='output-data-upload')
])

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')
    global df
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            df.to_dict('records'),
            [{'name': i, 'id': i} for i in df.columns]
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'

        } )
    ])

@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))

def children(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        print("imported type is:" , type(df))  # this will show data type as a pandas dataframe
        print("The impoted data is: \n" , df)
        return children


@app.callback(
    Output(component_id='mygraph', component_property='figure'),
    Input(component_id='dropdown', component_property='value')

)

def update_graph(user_input):  # function arguments come from the component property of the Input
    fig = px.scatter(data_frame=dff, x=dff.columns.tolist()[0], y=user_input)
    return fig  # returned objects are assigned to the component property of the Output

if __name__ == '__main__':
    app.run_server(debug=True)
