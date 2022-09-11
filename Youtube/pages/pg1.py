import dash
from dash import dcc, html, callback, Output, Input, State, dash_table
import plotly.express as px
import dash_bootstrap_components as dbc
from assets import youtube_dff
import pandas as pd

dash.register_page(__name__, path='/', name='Home General stats')  # '/' is home page

# page 1 data


layout = html.Div(
    [
        dbc.Row([dbc.Col(
            [html.Label("Enter channel-id", className="mt-4"),
             dcc.Input(id="input-handle", type="text", placeholder="insert youtubers channel id")
             ], width=3),
            dbc.Col(
                [html.Label("Enter channel-id", className="mt-4"),
                 dcc.Input(id="input-handle-2", type="text", placeholder="insert youtubers channel id")
                 ], width={"size": 2, "offset": 6})
        ]),
        dbc.Row(
            [
                dbc.Col(
                    [html.Button(id="hit-button", n_clicks=0, children="Submit",
                                 style={"background-color": "blue", "color": "white"}, className="mt-2"
                                 )], width=2)

            ]
        ),
        dbc.Row(
            [
                dbc.Col([html.P(id="header", children="", style={'fontSize': 25})], width={"size": 3, "offset": 2}),
                dbc.Col([html.P(id="header_2", children="", style={'fontSize': 25})], width={"size": 3, "offset": 3})
            ]
        ),
        dbc.Row([
            dbc.Col([html.Label("Table of like , View, Comment count of Video's", className='bg-secondary')],
                    width={"size": 10, "offset": 5})
        ]),
        dbc.Row([html.Br()]),
        dbc.Row([
            dbc.Col([
                html.Div(id='table-div', children="")
            ], width=6),
            dbc.Col([
                html.Div(id='table-div-2', children="")
            ], width={"size": 6, "offset": 0})
        ]),
        dbc.Row([html.Br()]),
        dbc.Row([
            dbc.Col(
                [html.Label("Duration of video's Vs Average like ,View and Comment counts", className='bg-secondary')],
                width={"size": 10, "offset": 4})
        ]), dbc.Row([html.Br()]),
        dbc.Row(
            [
                dbc.Col([dcc.RadioItems(id="rad_v_bar_2", options=[{'label': 'likes', 'value': 'likeCount'},
                                                                   {'label': 'Views', 'value': 'viewCount'},
                                                                   {'label': 'Comments', 'value': 'commentCount'}],
                                        value='likeCount', inline=True)], width={"offset": 3}),
                dbc.Col([dcc.RadioItems(id="rad_v_bar_3", options=[{'label': 'likes', 'value': 'likeCount'},
                                                                   {'label': 'Views', 'value': 'viewCount'},
                                                                   {'label': 'Comments', 'value': 'commentCount'}],
                                        value='likeCount', inline=True)], width={"offset": 3})
            ]),
        dbc.Row(
            [
                dbc.Col([dcc.Graph(id="bar_v_1", config={'displayModeBar': False})], width={"size": 6}),
                dbc.Col([dcc.Graph(id="bar_v_2", config={'displayModeBar': False})], width={"size": 6})
            ]
        ), dbc.Row([html.Br()]),

        dbc.Row([
            dbc.Col([html.Label("Video count based on duration of video in seconds", className='bg-secondary')],
                    width={"size": 10, "offset": 4})
        ]), dbc.Row([html.Br()]),

        dbc.Row(
            [
                dbc.Col([dcc.Graph(id="hist_th", config={'displayModeBar': False})], width={"size": 6}),
                dbc.Col([dcc.Graph(id="hist_th_2", config={'displayModeBar': False})], width={"size": 6})
            ]
        ), dbc.Row([html.Br()]),

        dbc.Row([
            dbc.Col([html.Label("Video count based on published day", className='bg-secondary')],
                    width={"size": 10, "offset": 4})
        ]), dbc.Row([html.Br()]),
        dbc.Row(
            [
                dbc.Col([dcc.Graph(id="bar_v_3", config={'displayModeBar': False})], width={"size": 6}),
                dbc.Col([dcc.Graph(id="bar_v_4", config={'displayModeBar': False})], width={"size": 6, "offset": 0})
            ]
        )
    ]
)


@callback(
    Output('bar_v_1', 'figure'),
    Output('bar_v_2', 'figure'),
    Output('hist_th', 'figure'),
    Output('hist_th_2', 'figure'),
    Output('bar_v_3', 'figure'),
    Output('bar_v_4', 'figure'),
    Output('table-div', 'children'),
    Output('table-div-2', 'children'),
    Output('header', 'children'),
    Output('header_2', 'children'),
    Input('hit-button', 'n_clicks'),
    State('input-handle', 'value'),
    State('input-handle-2', 'value'),
    Input('rad_v_bar_2', 'value'),
    Input('rad_v_bar_3', 'value')
    # Input('rad_v_bar_4', 'value'),
    # Input('rad_v_bar_5', 'value')
)
def update_graph(nclicks, ch_id_text, ch_id_text_2, rad_v_2, rad_v_3):
    channel_collect = []

    def data_read_csv(ch_id):
        channel_name = youtube_dff.get_data_youtube_channel(ch_id)
        if channel_name not in channel_collect:
            channel_collect.append(channel_name)
        data = pd.read_csv(f'assets/youtubechannel_{channel_name}.csv')
        return data

    def nclicks_fig_v_bar(channel_id, rad_but):
        dff = data_read_csv(channel_id)
        dff_durationmins = dff.groupby(['durationmins']).mean()
        fig_v_bar = px.bar(data_frame=dff_durationmins, x=dff_durationmins.index, y=rad_but)
        fig_v_bar.update_xaxes(categoryorder='total descending')
        fig_v_bar.update_layout(margin=dict(l=0, r=0, t=10, b=0))
        return fig_v_bar

    def nclicks_fig_hist(df):
        dff = df
        fig_hist = px.histogram(data_frame=dff, x="durationSecs", nbins=50)
        fig_hist.update_layout(margin=dict(l=0, r=0, t=10, b=0))
        return fig_hist

    def nclicks_fig_v_bar_2(df):
        dff = df
        day_df = pd.DataFrame(dff['pushblishDayName'].value_counts())
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_df = day_df.reindex(weekdays)
        fig_v_bar = px.bar(data_frame=day_df, x=day_df.index, y='pushblishDayName',
                           labels={"index":"pushblishday","pushblishDayName":"count"})
        fig_v_bar.update_layout(margin=dict(l=0, r=0, t=10, b=0))
        return fig_v_bar

    def nclicks_fig_bar(df, rad_but):
        dff = df
        dff_durationmins = dff.groupby(['durationmins']).mean()
        fig_v_bar = px.bar(data_frame=dff_durationmins, x=dff_durationmins.index, y=rad_but)
        fig_v_bar.update_xaxes(categoryorder='total descending')
        fig_v_bar.update_layout(margin=dict(l=0, r=0, t=10, b=0))
        return fig_v_bar

    if nclicks > 0:


        fig_v_bar_1 = nclicks_fig_v_bar(ch_id_text, rad_v_2)
        fig_v_bar_2 = nclicks_fig_v_bar(ch_id_text_2, rad_v_3)

        first = channel_collect[0]
        second = channel_collect[1]
        # def get_channel():
        #     return first,second
        df_1 = pd.read_csv(f'assets/youtubechannel_{first}.csv')
        df_2 = pd.read_csv(f'assets/youtubechannel_{second}.csv')

        fig_hist_1 = nclicks_fig_hist(df_1)
        fig_hist_2 = nclicks_fig_hist(df_2)

        fig_v_bar_3 = nclicks_fig_v_bar_2(df_1)
        fig_v_bar_4 = nclicks_fig_v_bar_2(df_2)

        comb = first + ' ' + second

        f = open('channel_name.txt', 'w')
        f.write(comb)
        f.close()




        table_1 = dash_table.DataTable(
            id='datatable-trends',
            columns=[
                {"name": i, "id": i} for i in df_1.columns
                if i == "title" or i == "viewCount" or i == "likeCount" or i == "commentCount"

            ],
            data=df_1.to_dict('records'),
            page_action='native',
            sort_action="native",
            sort_mode="multi",
            page_size=5,
            fixed_rows={'headers': True},
            style_table={'height': 400},
            style_cell={
                'whiteSpace': 'normal',
                'height': 'auto',
                'overflow': 'hidden',
                'minWidth': '50px', 'width': '80px', 'maxWidth': '120px',
            },
        )
        table_2 = dash_table.DataTable(
            id='datatable-trends',
            columns=[
                {"name": i, "id": i} for i in df_2.columns
                if i == "title" or i == "viewCount" or i == "likeCount" or i == "commentCount"

            ],
            data=df_2.to_dict('records'),
            page_action='native',
            sort_action="native",
            sort_mode="multi",
            page_size=5,
            fixed_rows={'headers': True},
            style_table={'height': 400},
            style_cell={
                'whiteSpace': 'normal',
                'height': 'auto',
                'overflow': 'hidden',
                'minWidth': '50px', 'width': '80px', 'maxWidth': '120px',
            },
        )

        return fig_v_bar_1, fig_v_bar_2, fig_hist_1, fig_hist_2, fig_v_bar_3, fig_v_bar_4, table_1, table_2, first.capitalize(), second.capitalize()

    elif nclicks == 0:
        file = open('channel_name.txt', 'r')
        f = file.readline()
        file.close()
        lst_channel_name = f.split(' ')
        first = lst_channel_name[0]
        second = lst_channel_name[1]
        left_channel_name = 'assets/youtubechannel_' + lst_channel_name[0] + '.csv'
        right_channel_name = 'assets/youtubechannel_' + lst_channel_name[1] + '.csv'


        df_left = pd.read_csv(left_channel_name)
        df_right = pd.read_csv(right_channel_name)

        fig_v_bar_1 = nclicks_fig_bar(df_left, rad_v_2)
        fig_v_bar_2 = nclicks_fig_bar(df_right, rad_v_3)

        fig_hist_1 = nclicks_fig_hist(df_left)
        fig_hist_2 = nclicks_fig_hist(df_right)

        fig_v_bar_3 = nclicks_fig_v_bar_2(df_left)
        fig_v_bar_4 = nclicks_fig_v_bar_2(df_right)

        table_1 = dash_table.DataTable(
            id='datatable-trends',
            columns=[
                {"name": i, "id": i} for i in df_left.columns
                if i == "title" or i == "viewCount" or i == "likeCount" or i == "commentCount"

            ],
            data=df_left.to_dict('records'),
            page_action='native',
            sort_action="native",
            sort_mode="multi",
            page_size=5,
            fixed_rows={'headers': True},
            style_table={'height': 400},
            style_cell={
                'whiteSpace': 'normal',
                'height': 'auto',
                'overflow': 'hidden',
                'minWidth': '50px', 'width': '80px', 'maxWidth': '120px',
            },
        )
        table_2 = dash_table.DataTable(
            id='datatable-trends',
            columns=[
                {"name": i, "id": i} for i in df_right.columns
                if i == "title" or i == "viewCount" or i == "likeCount" or i == "commentCount"

            ],
            data=df_right.to_dict('records'),
            page_action='native',
            sort_action="native",
            sort_mode="multi",
            page_size=5,
            fixed_rows={'headers': True},
            style_table={'height': 400},
            style_cell={
                'whiteSpace': 'normal',
                'height': 'auto',
                'overflow': 'hidden',
                'minWidth': '50px', 'width': '80px', 'maxWidth': '120px',
            },
        )

        return fig_v_bar_1, fig_v_bar_2, fig_hist_1, fig_hist_2, fig_v_bar_3, fig_v_bar_4, table_1, table_2, first.capitalize(), second.capitalize()
