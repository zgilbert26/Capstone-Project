# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px


# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                      dcc.Dropdown(id='site- Dropdown',
                                                    options=[
                                                         {'label': 'All Sites', 'value': 'ALL'},
                                                         {'label': 'CCAFS L40', 'value': 'CCAFS L40'},
                                                         {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                         {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                         {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                                    ],
                                                    value='ALL',
                                                    placeholder="Select a Launch Site Here",
                                                    searchable=True
                                                    ),
                                                    ])
                               


# Layout with dropdown for selecting a launch site and pie chart visualization
app.layout = html.Div([
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'}
        ] + [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
        value='ALL',
        placeholder="Select a launch site",
    ),
    dcc.Graph(id='success-pie-chart'),
])

# Callback function to update pie chart based on dropdown selection
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_pie_chart(selected_site):
    if selected_site == "ALL":
        data = spacex_df.groupby("class").size().reset_index(name="count")
        title = "Total Success Launches Across All Sites"
    else:
        data = spacex_df[spacex_df["Launch Site"] == selected_site].groupby("class").size().reset_index(name="count")
        title = f"Success vs Failed Launches for {selected_site}"
    
    fig = px.pie(data, values="count", names="class", title=title,  
                 color="class", color_discrete_map={1: "green", 0: "red"})
    
    return fig 
                                
dcc.RangeSlider(id='id',
                    min=0, max=10000, step=1000,
                    marks={0: '0',
                          100: '100'},
                    value=[min, max])

         # TASK 4: Add a scatter chart to show the correlation between payload and launch success

# Assume spacex_df is preloaded with 'Launch Site', 'Payload Mass (kg)', 'class', and 'Booster Version Category' columns

# Layout with dropdown for launch site selection, slider for payload range, and scatter plot
app.layout = html.Div([
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'}
        ] + [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
        value='ALL',
        placeholder="Select a launch site",
    ),
    dcc.RangeSlider(
        id='payload-slider',
        min=spacex_df["Payload Mass (kg)"].min(),
        max=spacex_df["Payload Mass (kg)"].max(),
        step=100,
        marks={i: str(i) for i in range(int(spacex_df["Payload Mass (kg)"].min()), int(spacex_df["Payload Mass (kg)"].max()), 1000)},
        value=[spacex_df["Payload Mass (kg)"].min(), spacex_df["Payload Mass (kg)"].max()]
    ),
    dcc.Graph(id='success-payload-scatter-chart'),
])

# Callback function to update scatter plot
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_plot(selected_site, payload_range):
    # Filter dataframe based on payload range
    filtered_df = spacex_df[(spacex_df["Payload Mass (kg)"] >= payload_range[0]) &
                            (spacex_df["Payload Mass (kg)"] <= payload_range[1])]

    if selected_site == "ALL":
        title = "Correlation Between Payload and Launch Outcome for All Sites"
    else:
        # Filter dataframe by selected site
        filtered_df = filtered_df[filtered_df["Launch Site"] == selected_site]
        title = f"Payload vs Launch Outcome for {selected_site}"

    # Create scatter plot
    fig = px.scatter(
        filtered_df, x="Payload Mass (kg)", y="class", color="Booster Version Category",
        title=title, labels={"class": "Launch Outcome"}
    )

    return fig                  

# Run the app
if __name__ == '__main__':
    app.run(port=8052)
    

