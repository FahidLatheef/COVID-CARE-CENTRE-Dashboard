"""
Created on Saturday Sep 12, 23:59:49 2020

@author: Fahid Latheef A

Project: Covid care centre dashboard

Purpose: To provide analytics of covid care centre data using interactive web inteface

Features:
1. 5 potential Analytical Questions on COVID CARE CENTRE
2. Solution to them using the research done in Jupyter Notebook
3. Plots to support the findings/answers
4. Multi-app/webpages linked together using Dash

# Running on http://127.0.0.1:1234/
"""
###############################################################
# IMPORTING REQUIRED PACKAGES
###############################################################
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])
app.config.suppress_callback_exceptions = True
pd.options.plotting.backend = "plotly"

###############################################################
# DATASET PREPROCESSING
###############################################################

# loading the dataset
df = pd.read_csv('karnataka_ccc.csv')

# Renaming
df.columns = ['Date', 'Daily_Collected_Samples', 'Daily_Negative',
              'Daily_Positive', 'People_In_Observation', 'Daily_Discharge']

df['Date'] = df['Date'].apply(pd.to_datetime)  # Converting to datetime OBJECT

df['Weekday_Index'] = df['Date'].dt.dayofweek
days = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}  # Index for arranging weekdays
df['Weekday'] = df['Weekday_Index'].apply(lambda x: days[x])

# Re arranging columns

df = df[['Date', 'Weekday_Index', 'Weekday', 'Daily_Collected_Samples', 'Daily_Negative', 'Daily_Positive',
         'People_In_Observation', 'Daily_Discharge']]

df['Cumulative_Collected_Samples'] = df['Daily_Collected_Samples'].cumsum()  # Cumulative value of Daily collected
df['Daily_Tests'] = df['Daily_Negative'] + df['Daily_Positive']  # Finding Daily Tests
df['Samples_Tested_Till_Today'] = df['Daily_Tests'].cumsum()  # Finding total tests done till that day
df['Cumulative_Positive'] = df['Daily_Positive'].cumsum()  # Finding cumulative case of positive cases
df['Daily_Lag'] = df['Daily_Collected_Samples'] - (df['Daily_Negative'] + df['Daily_Positive'])  # Finding Daily lag
df['Cumulative_Lag'] = df['Daily_Lag'].cumsum()  # Finding Cumulative lag

# plt1 = df[['Weekday_Index', 'Daily_Collected_Samples', 'Daily_Tests']].groupby(['Weekday_Index']).sum()

# make the columns of the dataset for filter dropdown
col_options = df.columns[3:]


###############################################################
# NAVIGATION BAR FUNCTION
###############################################################

# This function is called on every page to render the navigation bar

def Navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("My Portfolio", href="https://github.com/FahidLatheef", target='_blank')),
            # target='_blank' makes sure that the link is opened in a new tab
        ],
        brand="Home",
        brand_href="/home",
        sticky="top",
    )
    return navbar


###############################################################
# URL BAR
###############################################################

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),  # represents the URL bar, doesn't render anything
    html.Div(id='page-content'),  # content will be rendered in this element
])
# For different Web Format, uncomment these two.
# app.css.config.serve_locally = False  # To run the external page online

# app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

###############################################################
# PAGE1: HOME PAGE - Background + Objective + Questions
###############################################################

index_page = dbc.Container(
    [Navbar(),
     html.H2("Background"),
     html.P(
         [
             " Due to the current COVID-19 pandemic worldwide, the Government of India (GOI) set up few Covid Care Centres "
             " all over India with the following objectives:", html.Br(),
             html.Li(
                 [" It will function as an isolation centre for mild and asymptomatic Covid-19 positive patients."]),
             html.Li(
                 [" They have basic facilities and services to support testing, treatment and monitor the patients."]),
             html.Li(
                 [" They provide the analytics and case data database with designated authorities in secure manner"])]
     ),
     html.H2("Objective"),
     html.P(["Build an analytics dash board for Covid Care Centres in Karnataka and answer the analytical"
             " questions that a person may face if he is hired as a Data-Scientist for a COVID-CARE-CENTRE."]),
     html.H2("A few analytical questions to ponder..."),
     html.P(
         [
             '1) How likely you are tested positive if you are getting tested?', html.Br(),
             '2) There has been rumours that the testing is quite low during weekends. Is it true?',
             html.Br(),
             '3) Is it true that Monday is the day in which the most testing happens (Especially due to the claim that there is low testing during the weekend and it get postponed to monday)?',
             html.Br(),
             '4) There is also rumours that the sample collection is quite less during the weekends, validate?',
             html.Br(),
             '5) Clearly not all the samples collected are tested in the same day. Is this lag manageable? How severe is it?'
         ]
     ),

     html.Br(),
     dbc.Row(
         [
             dbc.Col(dbc.Button("View Answers", color="secondary", href='/answers')),
             dbc.Col(""),
             dbc.Col(dbc.Button("View Dashboards and Plots", color="secondary", href='/plots')),
         ],
         no_gutters=True,
     )
     ]
)


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/plots':
        return plots
    elif pathname == '/answers':
        return answers
    else:
        return index_page


###############################################################
# PAGE2: PLOTS AND DASHBOARDS
###############################################################
# Plots taken from the Jupyter Notebook

#
plots = html.Div([Navbar(),
                  html.H2("COVID-19 CARE CENTRES DASHBOARD AND OTHER RELEVANT PLOTS"),
                  # <h2>Covid care centre data</h2>
                  html.Div(
                      [
                          dcc.Dropdown(
                              id="Select_data",
                              options=[{
                                  'label': i,
                                  'value': i
                              } for i in col_options]
                              , value='')
                      ],
                      style={'width': '25%',
                             'display': 'inline-block'}),
                  dcc.Graph(id='c3-graph'),

                  html.Div(
                      [

                          dcc.Graph(id='g2', figure=df.plot(x="Date",
                                                            y=['Daily_Collected_Samples', 'Daily_Negative',
                                                               'Daily_Positive',
                                                               'People_In_Observation',
                                                               'Daily_Discharge', 'Daily_Tests'],
                                                            title="Covid-19 - Daily Plots", template="simple_white",
                                                            labels=dict(index="Date", value="Number of people",
                                                                        variable="Label")))
                      ]),

                  html.Div(
                      [

                          dcc.Graph(id='g3', figure=df.plot(x="Date",
                                                            y=['Cumulative_Collected_Samples',
                                                               'Samples_Tested_Till_Today',
                                                               'Cumulative_Positive', 'Cumulative_Lag'],
                                                            title="Covid-19 - Cumulative Plots",
                                                            template="simple_white",
                                                            labels=dict(index="Date", value="Number of people",
                                                                        variable="Patient type")))
                      ]),

                  html.Div(
                      [

                          dcc.Graph(id='g4', figure=df.plot(x="Date",
                                                            y=['Daily_Collected_Samples', 'Daily_Negative',
                                                               'Daily_Positive',
                                                               'Daily_Tests'],
                                                            kind='bar',
                                                            title="COVID-19 CARE CENTRES Daily Plots - Bar Representation",
                                                            template="simple_white",
                                                            labels=dict(index="Date", value="Number of people",
                                                                        variable="Patient type")))
                      ]),

                  ])


# make the graph object interactive using callback


@app.callback(
    Output('c3-graph', 'figure'),  # from dash dependencies
    [Input('Select_data', 'value')])  # input from combobox
def update_graph(Select_data):
    col = Select_data
    print(col)
    plot_1 = go.Scatter(x=df['Date'], y=df[col])  # plotting the graph

    # render the graph plot_1 as as web component
    return {
        'data': [plot_1],
        'layout':
            go.Layout(
                title='Covid care centre report for  {}'.format(Select_data),
            )
    }


###############################################################
# PAGE3: ANSWER PAGE
###############################################################
answers = dbc.Container(
    [Navbar(),
     html.H2("Answers"),
     html.P(
         ['1) How likely you are tested positive if you are getting tested?', html.Br(),
          'A) There is 3.64% chance of you getting positive if you are tested (from past data)', html.Br(), html.Br(),
          '2) There has been rumours that the testing is quite low during weekends. Is it true?', html.Br(),
          'A) This is absolutely correct, Sunday and Saturday are the days with least testing', html.Br(), html.Br(),
          '3) Is it true that Monday is the day in which the most testing happens (Especially due to the claim that there is low testing during the weekend and it get postponed to monday)?',
          html.Br(),
          'A) Most of the testing is not done on Monday, but rather on Wednesday and Thursday', html.Br(), html.Br(),
          '4) There is also rumours that the sample collection is quite less during the weekends, validate?',
          html.Br(),
          'A) The numbers do validate the rumour that the sample collection is low during weekends compared to the weekdays.',
          html.Br(), html.Br(),
          '5) Clearly not all the samples collected are tested in the same day. Is this lag manageable? How severe is it?',
          html.Br(),
          'A) Clearly we can see that the number of samples collected, but not tested, is increasing day-by-day and is getting tough for the care-centres to keep up with the testing.'
          ]
     ),
     dbc.Button("View Questions", color="secondary", href='/home'),
     ]
)

###############################################################
# RUNNING THE APP
###############################################################

if __name__ == '__main__':
    app.run_server(port=1234, debug=False)
