#NOTE: This MUST be run on python 3.10 or above

import requests
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
from datetime import date, datetime
import json

APP = Dash(__name__)
BASE_URL = "https://api.sparkpost.com/api/v1/"
#You MUST provide your API key below or the app will not function
API_KEY = ""

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

#Initialize Dataframe and Figure
df = pd.DataFrame({
    "Count": [0,0],
    "Time": [0,0]
})
fig = px.line(df,x="Time",y="Count")

#Build out the Dash app
APP.layout = html.Div([
    
    html.H1(children='SparkPost Analytics and Events'),

        dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Dashboard', value='tab-1'),
        dcc.Tab(label='Event Details', value='tab-2'),
    ]),

    html.Div(id='tabs-content'),
])

#Translates the dropdown values into values that can be passed into the API
def metrics(metric):
    match metric:
        case "Count Admin Bounce":
            return "count_admin_bounce"
        case "Count Accepted":
            return "count_accepted"
        case "Count Block Bounce":
            return "count_block_bounce"
        case "Count Bounce":
            return "count_bounce"
        case "Count Clicked":
            return "count_clicked"
        case "Count Delayed":
            return "count_delayed"
        case "Count Delayed First":
            return "count_delayed_first"
        case "Count Delivered":
            return "count_delivered"
        case "Count Delivered First":
            return "count_delivered_first"
        case "Count Delivered Subsequent":
            return "count_delivered_subsequent"
        case "Count Generation Failed":
            return "count_generation_failed"
        case "Count Generation Rejection":
            return "count_generation_rejection"
        case "Count Hard Bounce":
            return "count_hard_bounce"
        case "Count Inband Bounce":
            return "count_inband_bounce"
        case "Count Initial Rendered":
            return "count_initial_rendered"
        case "Count Injected":
            return "count_injected"
        case "Count Out of Band Bounce":
            return "count_outofband_bounce"
        case "Count Policy Rejection":
            return "count_policy_rejection"
        case "Count Rejected":
            return "count_rejected"
        case "Count Rendered":
            return "count_rendered"
        case "Count Sent":
            return "count_sent"
        case "Count Soft Bounce":
            return "count_soft_bounce"
        case "Count Spam Complaint":
            return "count_spam_complaint"
        case "Count Targeted":
            return "count_targeted"
        case "Count Undetermined Bounce":
            return "count_undetermined_bounce"
        case "Count Unique Clicked":
            return "count_unique_clicked"
        case "Count Unique Confirmed Opened":
            return "count_unique_confirmed_opened"
        case "Count Unique Initial Rendered":
            return "count_unique_initial_rendered"
        case "Count Unique Rendered":
            return "count_unique_rendered"
        case "Count Unsubscribe":
            return "count_unsubscribe"
        case "Total Delivery Time First":
            return "total_delivery_time_first"
        case "Total Delivery Time Subsequent":
            return "total_delivery_time_subsequent"
        case "Total Message Volume":
            return "total_msg_volume"

#App callback with the y-axis and dates as inputs, and the figure as an output
@APP.callback(
    Output('Emails', 'figure'),
    Input('y-axis', 'value'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'))

#When a change happens in the app to one of the above inputs, update the graph on the page
def update_graph(value,start_date,end_date):
    
    newvalue = []

    #Creating an array with the values selected from the dropdown
    for i in value:
        newvalue.append(metrics(i))

    joined_values = ",".join(newvalue)
    api_url = BASE_URL + "/metrics/deliverability/time-series?from=" + start_date + "T00:00&to=" + end_date + "T00:00&delimiter=,&precision=day&metrics=" + joined_values
    response_API = requests.get(api_url, headers = {"Authorization" : API_KEY})
    response_info = json.loads(response_API.text)

    new_df = pd.json_normalize(response_info, record_path=['results'])
    value_array = joined_values.split(",")

    fig = px.line(new_df, x=new_df['ts'], y=value_array, labels={"value": "Count", "variable": "Metric","ts":"Date"})
    fig.update_xaxes(title_text="Time")
    fig.update_yaxes(title_text="Count")

    return fig

@APP.callback(
    Output('tabs-content', 'children'),
    Input('tabs', 'value')
)

def render_content(tab):
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
    elif tab == 'tab-2':
        api_url = BASE_URL + "/events/message?delimiter=,&events=delivery,injection,bounce,delay,policy_rejection,out_of_band,open,click,generation_failure,generation_rejection,spam_complaint,list_unsubscribe,link_unsubscribe&page=1&per_page=10&reasons=bounce,internal"
        response_API = requests.get(api_url, headers = {"Authorization" : API_KEY})
        response_info = json.loads(response_API.text)

        new_df = pd.json_normalize(response_info, record_path=['results'])

        max_rows=10

        new_df = new_df.reindex(sorted(new_df.columns), axis=1)
        cols = ['timestamp']
        new_df = new_df[cols + [c for c in new_df.columns if c not in cols]]
        #new_df.rename(columns = {'timestamp':'Timestamp'},inplace=True)
 
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

if __name__ == '__main__':
    APP.run_server(debug=True)



    