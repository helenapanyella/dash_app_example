app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in items],
                value='Value added, gross'
            ),
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in items],
                value='Final consumption expenditure'
            ),

        ],
        style={'width': '40%', 'display': 'inline-block'}),

    ]),

    dcc.Graph(id='1-graphic'),



    html.Div([

        html.Div([
            dcc.Dropdown(
                id='2xaxis-column',
                options=[{'label': i, 'value': i} for i in items],
                value='Value added, gross'
            ),
            dcc.Dropdown(
                id='2yaxis-column',
                options=[{'label': i, 'value': i} for i in countries],
                value='France'
            ),
            dcc.RadioItems(
                id='unit',
                options=[{'label': i, 'value': i} for i in units],
                value='Current prices, million euro',
                labelStyle={'display': 'inline-block'}
            )            
        ],
        style={'width': '40%', 'display': 'inline-block'}),

    ]),

    dcc.Graph(id='2-graphic'),

    dcc.Slider(
        id='year--slider',
        min=df['TIME'].min(),
        max=df['TIME'].max(),
        value=df['TIME'].max(),
        step=None,
        marks={str(year): str(year) for year in df['TIME'].unique()}
    )    

])

@app.callback(
    dash.dependencies.Output('1-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('year--slider', 'value')])


def update_graph(xaxis_column_name, yaxis_column_name,
                 year_value):
    dff = df[df['TIME'] == year_value]

    return {
        'data': [go.Scatter(
            x=dff[dff['NA_ITEM'] == xaxis_column_name]['Value'],
            y=dff[dff['NA_ITEM'] == yaxis_column_name]['Value'],
            text=dff[dff['NA_ITEM'] == yaxis_column_name]['Value'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
            },
            yaxis={
                'title': yaxis_column_name,
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

@app.callback(
    dash.dependencies.Output('2-graphic', 'figure'),
    [dash.dependencies.Input('2xaxis-column', 'value'),
     dash.dependencies.Input('2yaxis-column', 'value'),
     dash.dependencies.Input('unit', 'value')])

def update_graph(xaxis_column_name, yaxis_column_name, unit):

    dff = df[(df['GEO'] == yaxis_column_name) & (df['UNIT'] == unit)]

    return {
        'data': [go.Scatter(
            x=dff[dff['NA_ITEM'] == xaxis_column_name]['TIME'],
            y=dff[dff['NA_ITEM'] == xaxis_column_name]['Value'],
            text=dff[dff['NA_ITEM'] == yaxis_column_name]['GEO'],
            mode='lines',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
            },
            yaxis={
                'title': yaxis_column_name,


            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server()
