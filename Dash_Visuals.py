import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd


def dash_visuals_init(server):
    df = pd.read_csv("Hotel_Reviews_2_Formatted.csv")
    app = dash.Dash(
        __name__,
        server=server,
        routes_pathname_prefix='/visuals/')
    app.layout = html.Div(children=[
        html.Form([html.Button('Back', type='submit')], action='/home', method='post'),
        html.P(),
        dcc.Graph(
            id='count-by-polarity',
            figure={
                'data': [
                    {'x': round(df.Review_Polarity, 2), 'type': 'histogram', 'histfunc': 'count',
                     'name': 'Reviews by Rating'},
                ],
                'layout': {
                    'title': 'Number of Reviews by Review Polarity',
                    'xaxis': dict(title='Review Polarity'),
                    'yaxis': dict(title='Count')
                }
            }
        ),
        html.P(),
        dcc.Graph(
            id='rating-by-review',
            figure={
                'data': [
                    {'x': round(df.Review_Polarity, 1), 'y': df.Reviewer_Score, 'type': 'histogram', 'histfunc': 'avg',
                     'name': 'Review Polarity'},
                ],
                'layout': {
                    'title': 'Average Rating by Review Polarity',
                    'xaxis': dict(title='Review Polarity'),
                    'yaxis': dict(title='Average Rating')
                }
            }
        ),
        html.P(),
        dcc.Graph(
            id='rating-by-title',
            figure={
                'data': [
                    {'x': round(df.Title_Polarity, 1), 'y': df.Reviewer_Score,
                     'type': 'histogram', 'histfunc': 'avg', 'name': 'Title Polarity'},
                ],
                'layout': {
                    'title': 'Average Rating by Title Polarity',
                    'xaxis': dict(title='Title Polarity'),
                    'yaxis': dict(title='Average Rating')
                }
            }
        )
    ])
