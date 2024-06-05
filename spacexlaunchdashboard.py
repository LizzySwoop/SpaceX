from dash import dcc
import pandas as pd
import plotly.express as px
import dash
from dash import html
from dash.dependencies import Input, Output

spacex_df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN"
                        "-SkillsNetwork/datasets"
    "/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

app = dash.Dash(__name__)

app.layout = html.Div(children=[html.H1('SpaceX Launch Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'fontSize': 35}),

                                dcc.Dropdown(id='site-dropdown',
                                             options=[
                                                 {'label': 'All Sites', 'value': 'ALL'},
                                                 {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                 {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                 {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                 {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},

                                             ],
                                             value='ALL',
                                             placeholder="Select a Launch Site",
                                             searchable=True),
                                html.Br(),

                                html.Div(dcc.Graph(id='success-pie-chart')),

                                html.Br(),

                                html.P("Payload range (kg):"),
                                dcc.RangeSlider(id='payload-slider',
                                                min=0,
                                                max=10000,
                                                step=1000,
                                                marks={0: '0',
                                                       1000: '1000',
                                                       10000: '10000'},
                                                value=[min_payload, max_payload]
                                                ),
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(site_dropdown):
    if site_dropdown == 'ALL':
        fig = px.pie(values=spacex_df.groupby('Launch Site')['class'].mean(),
                     names=spacex_df.groupby('Launch Site')['Launch Site'].first(),
                     title='Total Success Launches For All Sites')
        return fig

    else:
        fig = px.pie(
            values=spacex_df[spacex_df['Launch Site'] == str(site_dropdown)]['class'].value_counts(normalize=True),
            names=spacex_df['class'].unique(),
            title=f"Total Success Launches for site{site_dropdown}")
        return fig


@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')])
def scatter(site_dropdown, payload_slider):
    if site_dropdown == 'ALL':
        fig = px.scatter(spacex_df[spacex_df['Payload Mass (kg)'].between(payload_slider[0], payload_slider[1])],
                         x='Payload Mass (kg)', y='class', color='Booster Version Category',
                         hover_data=['Launch Site'],
                         title='Success Count vs Payload Mass (kg) for All Sites')
        return fig
    else:
        df = spacex_df[spacex_df['Launch Site']==str(site_dropdown)]
        fig = px.scatter(df[df['Payload Mass (kg)'].between(payload_slider[0], payload_slider[1])],
                         x='Payload Mass (kg)', y='class',
                         color='Booster Version Category',
                         hover_data=['Launch Site'],
                         title=f'Success count on Payload Mass for site {site_dropdown}')
        return fig


if __name__ == '__main__':
    app.run_server()
