# CustomDashboard
A tool to build out a custom SparkPost dashboard and event table

This is a simple tool that will:
 - connect to your SparkPost account
 - call the metrics API to build a graph of various metrics
 - allow you to select various metrics and timeframes to be graphed
 - call the events API to build a table of the 10 most recent events

## Setup
Clone this repo, then modify the App.py with your API key

NOTE: This MUST be run on python 3.10 or above

You must install the following libraries:
 -requests
 -dash
 -pandas

Then point your browser to http://localhost:8050

For more detailed information about Plotly Dash see: https://dash.plotly.com/introduction