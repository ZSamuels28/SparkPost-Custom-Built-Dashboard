#NOTE: This MUST be run on python 3.10 or above

import requests
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
from datetime import date, datetime
import json
from MetricTranslation import *

APP = Dash(__name__)
BASE_URL = "https://api.sparkpost.com/api/v1/"
#You MUST provide your API key below or the app will not function
API_KEY = ""

#Initialize Dataframe and Figure
df = pd.DataFrame({
    "Count": [0,0],
    "Time": [0,0]
})
fig = px.line(df,x="Time",y="Count")

#Build out the initial Dash app with 2 tabs (Dashboard and Event Details)
APP.layout = html.Div([
    
    html.H1(children='SparkPost Analytics and Events'),

        dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Dashboard', value='tab-1'),
        dcc.Tab(label='Event Details', value='tab-2'),
    ]),

    html.Div(id='tabs-content'),
])

#App callback for when the dropdown or dates are changed
#Y-axis and dates as inputs, figure as output
@APP.callback(
    Output('Emails', 'figure'),
    Input('y-axis', 'value'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'))

#When a change happens in the app to one of the above inputs, update the graph on the page
def update_graph(value,start_date,end_date):
    
    newvalue = []

    #Create an array with the values selected from the dashboard dropdown (note this references the function in MetricTranslation.py)
    for i in value:
        newvalue.append(metrics(i))

    #Build the API call utilizing the metrics and date provided
    joined_values = ",".join(newvalue)
    api_url = BASE_URL + "/metrics/deliverability/time-series?from=" + start_date + "T00:00&to=" + end_date + "T00:00&delimiter=,&precision=day&metrics=" + joined_values
    response_API = requests.get(api_url, headers = {"Authorization" : API_KEY})
    response_info = json.loads(response_API.text)

    new_df = pd.json_normalize(response_info, record_path=['results'])
    value_array = joined_values.split(",")

    #Build out a new dashboard utilizing the new metrics and dates from the updated API call
    fig = px.line(new_df, x=new_df['ts'], y=value_array, labels={"value": "Count", "variable": "Metric","ts":"Date"})
    fig.update_xaxes(title_text="Time")
    fig.update_yaxes(title_text="Count")

    return fig

#App callback for when the tabs are changed
@APP.callback(
    Output('tabs-content', 'children'),
    Input('tabs', 'value')
)

#When a change happens in the app to one of the tabs, update the html on the page
#This is also called at initialization to build out the page
def render_content(tab):

    #If the Dashboard tab (tab 1) is selected
    if tab == 'tab-1':
        return html.Div([

            html.H2('Analytics Dashboard'),

            #Multi-select dropdown
            dcc.Dropdown(['Count Accepted','Count Admin Bounce','Count Block Bounce','Count Bounce','Count Clicked','Count Delayed',
            'Count Delayed First','Count Delivered','Count Delivered First','Count Delivered Subsequent','Count Generation Failed',
            'Count Generation Rejection','Count Hard Bounce','Count Inband Bounce','Count Initial Rendered','Count Injected',
            'Count Out of Band Bounce', 'Count Policy Rejection','Count Rejected','Count Rendered','Count Sent','Count Soft Bounce',
            'Count Spam Complaint','Count Targeted','Count Undetermined Bounce','Count Unique Clicked','Count Unique Confirmed Opened',
            'Count Unique Initial Rendered','Count Unique Rendered','Count Unsubscribe','Total Delivery Time First','Total Delivery Time Subsequent',
            'Total Message Volume'], id="y-axis", multi=True, searchable=True, placeholder="Select metrics(s)"),

            #Date selector (max date allowed is set to today's date)
            dcc.DatePickerRange(
            id='date-picker-range',
            start_date=date(2022,1,1),
            end_date=date(2022, 2, 1),
            max_date_allowed=date(datetime.today().year,datetime.today().month,datetime.today().day),
            ),

            #Graph object
            dcc.Graph(
                id='Emails',
                figure=fig
                )
            ])

    #Else if Event Details tab (tab 2) is selected
    elif tab == 'tab-2':

        #Build out and call the events API
        api_url = BASE_URL + "/events/message?delimiter=,&events=delivery,injection,bounce,delay,policy_rejection,out_of_band,open,click,generation_failure,generation_rejection,spam_complaint,list_unsubscribe,link_unsubscribe&page=1&per_page=10"
        response_API = requests.get(api_url, headers = {"Authorization" : API_KEY})
        response_info = json.loads(response_API.text)

        new_df = pd.json_normalize(response_info, record_path=['results'])
        max_rows=10 #Max number of results show in the events table

        #Place timestamp as the first column in the table
        new_df = new_df.reindex(sorted(new_df.columns), axis=1)
        cols = ['timestamp']
        new_df = new_df[cols + [c for c in new_df.columns if c not in cols]]
 
        #Show the new HTML with the events table (note, this table also references table.css)
        return html.Div([
            html.H2("Event Details"),
            html.Table([
                html.Thead(
                    html.Tr([html.Th(col) for col in new_df.columns],className="table_css")
                ),
                html.Tbody([
                    html.Tr([
                        html.Td(new_df.iloc[i][col],className="table_css") for col in new_df.columns
                    ]) for i in range(min(len(new_df), max_rows))
                ])
            ])
        ])

#Run the app server
if __name__ == '__main__':
    APP.run_server(debug=False)



    