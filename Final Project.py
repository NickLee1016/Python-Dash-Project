from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from pandas_datareader import data
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

my_app = Dash('my app')

df = pd.read_csv("GDP.csv")
df.Year=df.Year.apply(lambda x: int(x[-4:]))

print(df)

# this is a layout that may have several containers
my_app.layout = html.Div(
          children=[    # this is a container/divider that may have many components/children     

                    html.H1('GDP information'),  

                    html.Label('Country: '),    

                    dcc.Input(                  # this is an input box       dcc.Input(value=   , id=   )
                               value="Afghanistan",      
                               id='my_input'
                              ),

                    html.Div(      # this is another divider that is a "child" of the divider above
                              
                              id = 'my_graph',
                              children = dcc.Graph(figure = {'data' : [    # here is a list that may have several dictionaries for plots
                                                                       {'x': df["Year"], 'y': df["GDP_pp"],
                                                                        "line": dict(color="green", width=5, dash="dash")}
                                                                    
                                                               
                                                                      ]
                                                            }
 
                                                   )
                            ),       
                   
          
                    html.H2('GDP by Region'),
          
                    html.Label('Region: '),

                    dcc.Dropdown(
                                    id='region_input',
                                    options=[
                                        {'label': 'Middle East, North Africa, and Greater Arabia', 'value':'Middle East, North Africa, and Greater Arabia'},
                                        {'label': 'Europe', 'value':'Europe'},
                                        {'label': 'Sub-Saharan Africa', 'value':'Sub-Saharan Africa'},
                                        {'label': 'Central America and the Caribbean','value':'Central America and the Caribbean'},
                                        {'label': 'South America', 'value':'South America'},
                                        {'label': 'Australia and Oceania', 'value':'Australia and Oceania'},
                                        {'label': 'Asia', 'value':'Asia'},
                                        {'label': 'North America', 'value': 'North America'}
                                        ],
                                    value='North America'
                                    ),
                    html.Div(
                                id = 'my_graph2',
                                children = dcc.Graph(figure = {'data': [
                                                                            {'x':df["Year"], 'y':df["GDP_pp"],
                                                                             "line":dict(color="red", width=5,dash="dash")}
                                                                            ]
                                                               }
                                                     )
                           ),
                    html.H3('Lowest GDP World Map'),

                    html.Label('Year'),

                    dcc.Slider( id='year_input',min=1901, max=2011, step=5, value=1901, tooltip = { 'always_visible': True }),

                    html.Div(
                                id = 'my_graph3',
                                children = dcc.Graph(figure = px.choropleth(df, locations='Country_code', 
                                                                            color = 'GDP_pp', hover_name='Country',
                                                                            color_continuous_scale= px.colors.sequential.Turbo))
                                
                                

                                                                        ),
                    
                                  
                        
                        
                    html.H2('GDP of Region by Year'),
          
                    html.Label('Year: '),

                    dcc.Input(id='year_input2', type='number', min=1901, max=2011, step=5, value=1901),
                    
                    html.Div(
                                id = 'my_graph4',
                                children = dcc.Graph(figure ={"data":
                                    [go.Pie(labels=df['Region'], 
                                        values=df['GDP_pp'],sort=False)
##                                            color_discrete_map={
##                                                "Europe":'blue',
##                                                "Middle East, North Africa, and Greater Arabia":'yellow',
##                                                "Sub-Saharan Africa":'grey',
##                                                "Central America and the Caribbean":'green',
##                                                "North America":'red',
##                                                "Australia and Oceania":'purple',
##                                                "Asia":'pink',
##                                                "South America":'brown'
##                                                })
                                          ]}
                                                     )
                                
                            )
                      ]
                )


@my_app.callback(  # Output, [Input])
    [Output(component_id='my_graph', component_property='children'),
    Output(component_id='my_graph2', component_property='children'),
     Output(component_id='my_graph3', component_property='children'),
     Output(component_id='my_graph4', component_property='children')],
    [Input(component_id='my_input',component_property='value'),
    Input(component_id='region_input', component_property='value'),
     Input(component_id='year_input', component_property='value'),
     Input(component_id='year_input2', component_property='value')]
                )
def update_graph(inputCountry, inputRegion, inputYear, inputYear2):
    df1=df.loc[df['Country'] == inputCountry] # updated dataframe
    df2=df.loc[df['Region']== inputRegion]
    df2=df2.groupby("Year", as_index=False).max()
    df3=df.loc[df['Year'] == inputYear]
    df4=df.loc[df["Year"] == inputYear2]
    df5=df4.groupby("Region", as_index=False).sum()
    
    
    # graph by country
    fig_title = "Data for "+inputCountry

    fig={'data' : [    # here is a list that may have several dictionaries for traces
                   {'x': df1["Year"], 'y': df1["GDP_pp"],
                    "line": dict(color="green", width=5, dash="dash")}
                   ]}
      
    fig["layout"] = {"title": {"text": fig_title},
                 'plot_bgcolor':"aliceblue",
                 'paper_bgcolor': "lightcyan",
                 'font': {'color': "blue", "size": 20},
                 "height": 600,
                 'width': 1500}

    #graph by region

    fig1_title = "Data for "+inputRegion

    fig1={'data': [
                    {'x':df2["Year"], 'y':df2["GDP_pp"],
                     "line":dict(color="red", width=5,dash="dash")}
                    ]}

    fig1["layout"] = {"title": {"text": fig1_title},
                    'plot_bgcolor':"#DCDCDC",
                    'paper_bgcolor': "#fff",
                     'font': {'color': "blue", "size": 20},
                     "height": 600,
                     'width': 1500}

    #World Map

    fig2_title = "Minimum GDP Map by Year"
    
    fig2= px.choropleth(
                        df3, color='GDP_pp',
                        locations='Country_code',
                        hover_name='Country',
                        #locationmode ='country names',
                        color_continuous_scale=px.colors.sequential.Turbo)
                        #locations="Country_code", featureidkey="properties.district",
                        #projection="mercator", range_color=[0, 6500])
    fig2.layout.update(margin={"r":0,"t":0,"l":0,"b":0})


    #Pie Chart
    fig3={"data":
                [go.Pie(labels=df5["Region"], 
                    values=df5["GDP_pp"])
        ]}


    
                      
    graph= dcc.Graph(figure = fig)
    graph1= dcc.Graph(figure = fig1)
    graph2= dcc.Graph(figure = fig2)
    graph3= dcc.Graph(figure = fig3)
    return graph, graph1, graph2, graph3

if __name__ == '__main__':
    my_app.run_server(debug=True)
