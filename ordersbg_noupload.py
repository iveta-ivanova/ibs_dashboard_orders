# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 15:41:17 2020

@author: Iveta
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 09:40:56 2020

@author: Iveta
"""
#from whitenoise import WhiteNoise
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import pandas as pd
import dateutil
import numpy as np
import datetime
from datetime import date

app = dash.Dash(__name__)
server = app.server
#server.wsgi_app = WhiteNoise(server.wsgi_app, root=‘static/’)

data = pd.read_excel('Test.xls')        ## can use Sqlite, posgresSQL, API....

columns_list = ['CodeCustomers','NameCustomers','SumOrder','Date Order']
for col in columns_list: 
    if col not in data.columns: 
        break
    
#data['Date Order'] = data['Date Order'].apply(dateutil.parser.parse, dayfirst = True)

data['month'] = data['Date Order'].dt.month.astype('int64')
data['year'] = data['Date Order'].dt.year.astype('int64')
data['day'] = data['Date Order'].dt.day.astype('int64')
data['date'] = data['Date Order'].dt.date.astype('category')      ##date is an object, Date Order is a datetime object


## create group object by customer name 
dfMeanClientAll = data.groupby(['NameCustomers']).agg({'SumOrder': 'mean'}).fillna(0).reset_index().round(0)
dfMeanClientByMonthYear = data.groupby(['NameCustomers', 'month','year']).agg({'SumOrder': 'mean'}).fillna(0).reset_index().round(0)
dfMeanByMonthYear = data.groupby(['month','year']).agg({'SumOrder': 'mean'}).fillna(0).reset_index().round(0)

#dfSumClientAll = data.groupby(['NameCustomers']).agg({'SumOrder': 'sum'}).fillna(0).reset_index()
#dfSumClientByMonthYear = data.groupby(['NameCustomers', 'month','year']).agg({'SumOrder': 'sum'}).fillna(0).reset_index()
#dfSumByMonthYear = data.groupby(['month','year']).agg({'SumOrder': 'sum'}).fillna(0).reset_index()

#dfMinClientAll = data.groupby(['NameCustomers']).agg({'SumOrder': 'min'}).fillna(0).reset_index()
#dfMinClientByMonthYear = data.groupby(['NameCustomers', 'month','year']).agg({'SumOrder': 'min'}).fillna(0).reset_index()
#dfMinByMonthYear = data.groupby(['month','year']).agg({'SumOrder': 'min'}).fillna(0).reset_index()

#dfMaxClientAll = data.groupby(['NameCustomers']).agg({'SumOrder': 'max'}).fillna(0).reset_index()
#dfMaxClientByMonthYear = data.groupby(['NameCustomers', 'month','year']).agg({'SumOrder': 'max'}).fillna(0).reset_index()
#dfMaxByMonthYear = data.groupby(['month','year']).agg({'SumOrder': 'max'}).fillna(0).reset_index()

PAGE_SIZE = 15



app.layout = html.Div([
    dbc.Row(
        dbc.Col([
            html.Br(),
            html.H1('Вашите данни визуализирани',                 
                style = {'textAlign': 'center'}),
            html.Br()],
            width = {'size':11, 'offset':1}
                ),
            ),
    dbc.Row([
        dbc.Col([
            html.Br(),
            html.H2('Вижте продажби за даден клиент по месеци и години',
                    style = {'textAlign': 'left'}),
            html.Br()],
            width = {'size':4, 'offset':1}),
        dbc.Col([
            html.Br(),
            html.H2('Вижте топ клиенти за даден времеви период')],
            width = {'size':4, 'offset':2})
            ]),   
    dbc.Row([
        dbc.Col(
            html.Div([   
                html.Label('Изберете клиент'),
                dcc.Dropdown(
                    id = 'customer-choice',
                    options = [
                        {'label': l, 'value': l} 
                        for l in data['NameCustomers'].unique()
                        ],
                    #multi = True,
                    placeholder = 'Изберете клиент',
                    ),
                html.Br(),
                html.Br(),
                html.Div(
                    id = 'client-summary'),
                html.Br(),
                html.Br(),
                html.Div(
                    id = 'client-month-plot'),]), 
        width = {'size': 3, 'offset':1, 'order': 1}
                ),
        dbc.Col([
            html.Label('Период по години'), 
                dcc.Checklist(
                    id = 'year-checklist',
                    options = [
                        {'label': str(y), 'value': y, 'disabled':False} 
                        for y in data['year'].unique()
                        ],
                    labelStyle = dict(display = 'block'),
                    value = [x for x in data['year'].unique()]                     ## figure out how NOT to hard code this 
                    ),
            html.Br(),
            html.Label('Период по месеци'),
                dcc.RangeSlider(
                    id = 'slider-month',
                    min = data['month'].min(),
                    max = data['month'].max(), 
                    #marks = {int(i):str(j) for i,j in zip(range(len(df2)), df2['month'])},
                    marks = {
                        1: {'label': 'Януари', 'style': {'transform': 'rotate(60deg)'}},
                        2: {'label': 'Февруари', 'style': {'transform': 'rotate(60deg)'}},
                        3: {'label': 'Март', 'style': {'transform': 'rotate(60deg)'}},
                        4: {'label': 'Април', 'style': {'transform': 'rotate(60deg)'}},
                        5: {'label': 'Май', 'style': {'transform': 'rotate(60deg)'}},
                        6: {'label': 'Юни', 'style': {'transform': 'rotate(60deg)'}},
                        7: {'label': 'Юли', 'style': {'transform': 'rotate(60deg)'}},
                        8: {'label': 'Август', 'style': {'transform': 'rotate(60deg)'}},
                        9: {'label': 'Септември', 'style': {'transform': 'rotate(60deg)'}},
                        10: {'label': 'Октомври', 'style': {'transform': 'rotate(60deg)'}},
                        11: {'label': 'Ноември', 'style': {'transform': 'rotate(60deg)'}},
                        12: {'label': 'Декември', 'style': {'transform': 'rotate(60deg)'}}
                        },
                    value = [1,12]),
            html.Br(),
            html.Br(),
            html.Div([
                html.Label('Изберете брой топ клиенти'),
                dcc.Dropdown(
                    id = 'n-clients-dropdown',
                    options = [
                        {'label': str(n), 'value': n, 'disabled': False}
                        for n in n_clients_list
                        ]
                    ),
                html.Br(),
                html.Button('Обнови', id = 'top-client-btn', n_clicks = 0)
                ]),
            html.Br(),
            html.Br(),
            html.Div(
                id = 'top-clients')],
            width = {'size': 4, 'offset':3, 'order': 2}),
    ]), 
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col(
            html.H2('Вижте информация за всички клиенти'),
            width = {'size':4, 'offset': 1, 'order': 1}),
        dbc.Col(
            dcc.RadioItems(
                    id = 'display-type',
                    options = [
                        {'label': 'сумарно', 'value': 'сумарно'},
                        {'label': 'средно', 'value': 'средно'},
                        {'label': 'максимално', 'value': 'максимално'},
                        {'label': 'минимално', 'value': 'минимално'}],
                    value = 'средно'),
                width = {'size':1, 'order':2}),
        ]),
    html.Br(),
    dbc.Row([
        dbc.Col(
            html.Div(
                id='client-graph-container'),
            width = {'size':6, 'offset':1}),
        dbc.Col(
            html.Div(
                dash_table.DataTable(
                    id = 'table',  
                    data = [],
                    columns = [{'name': i, 'id': i} for i in (dfMeanClientAll.columns)],
                    style_cell={'textAlign': 'center',
                                'fontWeight':'bold',
                                'padding': '15px'},
                    style_header={'fontWeight': 'bold'},
                    
                    page_current=0,
                    page_size= PAGE_SIZE,
                    page_action='custom',
    
                    filter_action='custom',
                    filter_query='',
    
                    sort_action='custom',
                    sort_mode='multi',
                    sort_by=[],
                    fixed_rows={'headers': True},
                    style_as_list_view=True,
                    style_table = {'height': '420px',
                                   'overflowY': 'auto',
                                   'width': '400px'},
                    style_cell_conditional=[
                        {'if': {'column_id': 'SumOrder'},
                         'width': '50%'},
                        {'if': {'column_id': 'NameCustomers'},
                         'width': '50%'}]
                ), 
                ),
            width = {'size':4, 'offset':0})
        ]),
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col(
            html.Div(
                id='time-graph-container'),
            width = {'size': 5, 'offset': 1}),
        dbc.Col(
            html.Div(
                dash_table.DataTable(
                    id = 'table-time',
                    data = [],
                    columns = [{'name': i, 'id': i} for i in (dfMeanByMonthYear.columns)],
                    style_cell={'textAlign': 'center',
                                'fontWeight':'bold',
                                'padding': '15px'},
                    style_header={'fontWeight': 'bold'},
                    sort_action='custom',
                    sort_mode='multi',
                    sort_by=[], 
                    fixed_rows={'headers': True},
                    style_as_list_view=True,
                    style_table = {'height': '400px',
                                   'overflowY': 'auto',
                                   'width': '330px'},
                    style_cell_conditional=[
                        {'if': {'column_id': 'SumOrder'},
                         'width': '33%'},
                        {'if': {'column_id': 'month'},
                         'width': '33%'},
                        {'if': {'column_id': 'year'},
                         'width': '33%'}]
                ),
                ),
            width = {'size': 4, 'offset': 1})
        ])
])         

""" Useful functions """

operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]

def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3


def get_dataframe_months_years(value):
    dff = pd.DataFrame()
    if value == 'сумарно': 
        dff = data.groupby(['month','year']).agg({'SumOrder': 'sum'}).fillna(0).reset_index()
    if value == 'минимално':
        dff = data.groupby(['month','year']).agg({'SumOrder': 'min'}).fillna(0).reset_index()
    if value == 'максимално': 
        dff = data.groupby(['month','year']).agg({'SumOrder': 'max'}).fillna(0).reset_index()
    if value == 'средно': 
        dff = data.groupby(['month','year']).agg({'SumOrder': 'mean'}).fillna(0).reset_index().round()
    return dff 

def get_dataframe_clients(value):
    dff = pd.DataFrame()
    if value == 'сумарно': 
        dff = data.groupby(['NameCustomers']).agg({'SumOrder': 'sum'}).fillna(0).reset_index()
    if value == 'минимално':
        dff = data.groupby(['NameCustomers']).agg({'SumOrder': 'min'}).fillna(0).reset_index()
    if value == 'максимално': 
        dff = data.groupby(['NameCustomers']).agg({'SumOrder': 'max'}).fillna(0).reset_index()
    if value == 'средно': 
        dff = data.groupby(['NameCustomers']).agg({'SumOrder': 'mean'}).fillna(0).reset_index().round()
    return dff 

def get_client_df(client): 
    # here data holds the csv file read on the first file
    dfAll = data.loc[data['NameCustomers']==client]
    dfmean = data.groupby(['NameCustomers', 'month','year']).agg({'SumOrder': 'mean'}).fillna(0).reset_index().round(0)
    dfsum = data.groupby(['NameCustomers', 'month','year']).agg({'SumOrder': 'sum'}).fillna(0).reset_index()
    dfmin = data.groupby(['NameCustomers', 'month','year']).agg({'SumOrder': 'min'}).fillna(0).reset_index()
    dfmax = data.groupby(['NameCustomers', 'month','year']).agg({'SumOrder': 'max'}).fillna(0).reset_index()
    dfMean = dfmean.loc[dfmean['NameCustomers'] == client] ## entire table for this client
    dfSum = dfsum.loc[dfsum['NameCustomers'] == client]
    dfMin = dfmin.loc[dfmin['NameCustomers'] == client]
    dfMax = dfmax.loc[dfmax['NameCustomers'] == client]
    #dfMeanYears = dfMeanClientByMonthYear.loc[dfMeanClientByMonthYear['NameCustomers'] == client]['year']
    #dfMeanMonths = dfMeanClientByMonthYear.loc[dfMeanClientByMonthYear['NameCustomers'] == client]['month']
    return dfAll, dfMean, dfSum, dfMin, dfMax


"""CallBacks"""

@app.callback(
    Output('top-clients', 'children'),
    [Input('top-client-btn','n_clicks'),
     Input('n-clients-dropdown','value'),
     State('slider-month','value'),
     State('year-checklist','value'),
     ]
    )
def show_top_clients(clicks, n, months, years): 
    # slider and checklist value is a list [ x , x]
    # months[0] (min) --> months[1] (max)
        df = data
        if months and years and n:
            if len(months) == 1:    
                months.append(months[0])
            if len(years) == 1: 
                years.append(years[0])                
            df1 = df[(df['month'] >= months[0]) & (df['month'] <= months[1])]
            df2 = df1[(df1['year'] >= years[0]) & (df1['year'] <= years[1])] 
            #if n > len(df2['NameCustomers'].unique()): 
            #    n = len(df2['NameCustomers'].unique())
            dfgraph = df2.groupby(['NameCustomers']).agg({'SumOrder': 'sum'}).fillna(0).reset_index().round(0).sort_values('SumOrder', ascending = True).tail(n)
            title = 'Топ {} клиенти по общи продажби'.format(n)
            height = int(0)
            if  n== 5: 
                height = 350
            if n== 10: 
                height = 500
            if n== 20: 
                height = 1000
            if n== 50: 
                height = 1200
            return html.Div(
                dcc.Graph(
                        figure={
                            "data": [
                                {
                                    "x": dfgraph['SumOrder'],    
                                    "y": dfgraph['NameCustomers'],
                                    "type": "bar",
                                    'orientation': 'h',
                                }, 
                            ],
                            "layout": {
                                'title': {'text': title},
                                "xaxis": {"automargin": True},
                                "yaxis": {"automargin": True},
                                'height': height,
                                'width':500,
                                "margin": {"t": 50, "l":200, "r": 0}, 
                                'autosize': True
                            }
                        },
                    ),
                style = {'overflowY': 'scroll',
                                          'height': 450,
                                          'width': 600})
    
@app.callback(
    Output('client-summary', 'children'),
    [Input('customer-choice','value')
     ]
    )
def print_client_summary(client): 
    mean_all = int()
    sum_all = int()
    dfall, dfmean, dfsum, dfmin, dfmax = get_client_df(client)
    total_sales = len(dfall)
    if client:
        mean_all = round(dfall['SumOrder'].mean())
        sum_all = dfall['SumOrder'].sum()
    return """{} има общо 
    {} продажби за дадения период, за общо {} лв.
    - средна стойност за целия период - 
    {} лв.""".format(client, total_sales, sum_all, mean_all)

@app.callback(
    Output('client-month-plot','children'),
    [Input('customer-choice','value')
     #Input('year-checklist','value'),
     #Input('slider-month','value')
     ]
    )
def client_month_plot(client):
    _, _, dfsum, _, _ = get_client_df(client)
    dff = dfsum
    title = 'Общи продажби зa {}'.format(client)
    if client:
         return html.Div(         ## return the graph
         [dcc.Graph(
                        figure={
                            "data": [
                                {
                                    "x": dff.loc[dff['year']==y]['month'],    
                                    "y": dff.loc[dff['year']==y]['SumOrder'],
                                    "type": "lines",
                                    'name': str(y)
                                } for y in dff['year'].unique() 

                            ],
                            "layout": {
                                'title': {'text': title},
                                "xaxis": {"automargin": True},
                                "yaxis": {"automargin": True},
                                "height": 400,
                                'width':650,
                                "margin": {"t": 50, "l": 0, "r": 0},
                            },
                        },
                    )
                ]
            )
    

@app.callback(
    Output('table-time', 'data'),             ## update table when changes happen (here only sorting)
   [Input('table-time', "sort_by"),
    Input('display-type','value'),
    State('display-type','value')])
def sort_time_table(sort_by,display_input,display_state):
        dff = get_dataframe_months_years(display_state)
        if len(sort_by):
            dff = dff.sort_values(
                [col['column_id'] for col in sort_by],
                ascending=[
                    col['direction'] == 'asc'
                    for col in sort_by
                ],
                inplace=False
            )
        return dff.to_dict('records')
        
@app.callback(                      ## update table when change page, filter or sort by
    Output('table', "data"),
    [Input('table', "page_current"),
     Input('display-type','value'),
     Input('table', "page_size"),
     Input('table', "sort_by"),
     Input('table', "filter_query"),
     State('display-type','value')])
def update_table(page_current, display_input, page_size, sort_by, filter, display_state):
        dff = get_dataframe_clients(display_state)    
        filtering_expressions = filter.split(' && ')
        for filter_part in filtering_expressions:
            col_name, operator, filter_value = split_filter_part(filter_part)
    
            if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
                # these operators match pandas series operator method names
                dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
            elif operator == 'contains':
                dff = dff.loc[dff[col_name].str.contains(filter_value)]
            elif operator == 'datestartswith':
                # this is a simplification of the front-end filtering logic,
                # only works with complete fields in standard format
                dff = dff.loc[dff[col_name].str.startswith(filter_value)]
        if len(sort_by):
            dff = dff.sort_values(
                [col['column_id'] for col in sort_by],
                ascending=[
                    col['direction'] == 'asc'
                    for col in sort_by
                ],
                inplace=False
            )
    
        return dff.iloc[ 
            page_current*page_size: (page_current + 1)*page_size
        ].to_dict('records')


@app.callback(
    Output('time-graph-container', "children"),    ## 
    [Input('table-time', "data"),
     State('display-type','value')
     ]
    )
def update_time_graph(rows, display_state):             ## rows = data (from above)
    dff = pd.DataFrame(rows)        ## in new variable, store the input table
    title = 'Продажби за всички клиенти, {} по месеци и години'.format(display_state)
    return html.Div(         ## return the graph
        [
            dcc.Graph(
                figure={
                    "data": [
                                {
                                    "x": dff.loc[dff['year']==y]['month'],    
                                    "y": dff.loc[dff['year']==y]['SumOrder'],
                                    "type": "bar",
                                    'name': str(y)
                                } for y in dff['year'].unique() 
                    ],
                    "layout": {
                        'title': {'text': title},
                        "xaxis": {"automargin": True},
                        "yaxis": {"automargin": True},
                        "height": 400,
                        "margin": {"t": 50, "l": 0, "r": 0},
                    },
                },
            )
        ]
    )

@app.callback(
    Output('client-graph-container', "children"),
    [Input('table', "data"),
     State('display-type','value')
     ]
    )
def update_graph(rows, display_state):         ## rows = data (from table)
    dff = pd.DataFrame(rows)
    title = 'Общи продажби по клиенти, {}'.format(display_state)
    return html.Div(
        [
            dcc.Graph(
                id=column,
                figure={
                    "data": [
                        {
                            "x": dff["NameCustomers"],
                            "y": dff[column] if column in dff else [],
                            "type": "bar",
                            "marker": {"color": "#0074D9"},
                        }
                    ],
                    "layout": {
                        'title': {'text':  title },
                        "xaxis": {"automargin": True},
                        "yaxis": {"automargin": True},
                        "height": 400,
                        "margin": {"t": 50, "l": 0, "r": 0},
                    },
                },
            )
            for column in ["SumOrder"]
        ]
    )


if __name__ == '__main__':
    app.run_server(debug=True)