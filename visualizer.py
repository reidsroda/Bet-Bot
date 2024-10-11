from dash import html, dcc, Output, Input, Dash, State
import dash_bootstrap_components as dbc
import math
import sqlite3
import time
import pandas

update_frequency = 1000



default_fig = dict(
                data=[{'x':[],'y':[]}],
                layout=dict(
                    xaxis=dict(range=[-1,1], visible = False),
                    yaxis=dict(range=[165,195], color="white"),
                    paper_bgcolor="#2D2D2D",
                    plot_bgcolor="#2D2D2D"
                    ))


time.sleep(37)

app = Dash()

app.layout = html.Div([
    
    html.H1(id= "live_total"),
    dcc.Graph(id = "graph", figure = default_fig ),
    dcc.Interval(id = "update", interval = update_frequency)
    
    ])


@app.callback(
        Output("graph", "extendData"),
        Output("live_total", "children"),
        Input("update", "n_intervals"),
        )

def update_data(intervals):
    connection = sqlite3.connect("./NBA.db")
    cursor = connection.cursor()
    
    datap = cursor.execute("SELECT live_total FROM live_lines WHERE team1='Selfoss' ORDER BY date DESC LIMIT 1").fetchall()
    y_val = datap[0]
    return (dict(x = [[time.time()]], y = [[y_val[0]]]), [0], 100), y_val[0]
    
    

if __name__ == "__main__":
    app.run_server(debug=True)
    