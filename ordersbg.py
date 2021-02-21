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
'''
cards component 
navbar 
from io import BytesIO --> for image processing

'''
#import os 
#os.chdir('C:\\Users\Iveta\Desktop\PROGRAMMING\IBS Data Analytics')

import io
import base64
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import pandas as pd
import dateutil
import datetime
import tzlocal



stylesheet = 'https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/darkly/bootstrap.min.css'

app = dash.Dash(__name__, external_stylesheets = [stylesheet])
#app = dash.Dash(__name__, external_stylesheets = [dbc.themes.SUPERHERO])
server = app.server

app.layout = html.Div([
    dbc.Row([
        html.Div(
            id = 'hidden-div', 
            style = {'display': 'none'}
        ),
        dbc.Col([
            html.Br(),
            html.H1('Вашите данни визуализирани',                 
                style = {'textAlign': 'center'}),
            html.Br()],
            width = {'size':6, 'offset':1}),
        dbc.Col([
            html.Br(),
            dcc.Upload(
                id = 'upload-data',
                children = html.Div([
                    'Дръпнете тук желания файл']),
                style={
            'width': '80%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
                multiple = False
                )
            ])
        ]),
    dbc.Row(
        dbc.Col(
            dcc.Loading(
                id = "loading-file-info",
                type = 'graph',
                fullscreen = True,
                children = html.Div(
                    id = 'file-info'),
                style = {'fontColor': 'blue'}
            ),
        width = {'size': 3, 'offset': 1})
        ),
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.Br(),
            html.H2('Вижте продажби за даден клиент по месеци и години',
                    style = {'textAlign': 'left'}),
            html.Br()],
            width = {'size':4, 'offset':1}),
        dbc.Col([
            html.Br(),
            html.H2('Вижте топ 10 клиенти за даден времеви период')],
            width = {'size':4, 'offset':2})
            ]),   
    dbc.Row([
        dbc.Col(
            html.Div([   
                html.Label('Изберете клиент'),
                dcc.Loading(
                    id = 'loading-customer-choice', 
                    type = 'circle',
                    children = dcc.Dropdown(
                    id = 'customer-choice',
                    placeholder = 'Изберете клиент',
                    )),
                html.Br(),
                html.Br(),
                dcc.Loading(id = 'loading-client-summary', 
                            type = 'circle',
                            children = html.Div(
                    id = 'client-summary')),
                html.Br(),
                html.Br(),
                dcc.Loading(id = 'loading-client-month-plot', 
                            type = 'circle',
                            children = html.Div(
                    id = 'client-month-plot')),]), 
        width = {'size': 3, 'offset':1, 'order': 1}
                ),
        dbc.Col([
            html.Label('Период по години'), 
                dcc.Loading(id = "loading-year-checklist", 
                            type = 'circle',
                            children = dcc.Checklist(
                    id = 'year-checklist',
                    labelStyle = dict(display = 'block')                    
                    )),
            html.Br(),
            html.Label('Период по месеци'),
                dcc.RangeSlider(
                    id = 'slider-month',
                    min = 1,
                    max = 12,
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
                        for n in [5,10,20,50]
                        ]
                    ),
                html.Br(),
                html.Button('Обнови', id = 'top-client-btn', n_clicks = 0)
                ]),
            html.Br(),
            html.Br(),
            dcc.Loading(id = 'loading-top-clients', 
                        type = 'circle', 
                        children = html.Div(
                id = 'top-clients'))
            ],
        width = {'size': 4, 'offset':3, 'order': 2}
        )
    ]), 
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col(
            html.H2('Вижте информация за всички клиенти'),
            width = {'size':4, 'offset': 1, 'order':1}),
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
            dcc.Loading(id = 'loading-client-graph-container', 
                        type = 'circle',
                        children =
            html.Div(
                id='client-graph-container')),
            width = {'size':6, 'offset':1}),
        dbc.Col(
            dcc.Loading(id = 'loading-table', 
                        type = 'circle',
                        children = 
            html.Div(
                dash_table.DataTable(
                    id = 'table',                      
                    style_cell={'textAlign': 'center',
                                'fontWeight':'bold',
                                'padding': '15px'},
                    style_header={'fontWeight': 'bold'},
                    
                    page_current=0,
                    page_size= 15,
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
                )),
            width = {'size':4, 'offset':0})
        ]),
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col(
            dcc.Loading(id = 'loading-time-graph-container', 
                        type = 'circle', 
                        children =
            html.Div(
                id='time-graph-container')),
            width = {'size': 5, 'offset': 1}),
        dbc.Col(
            dcc.Loading(id = 'loading-table-time',
                        type= 'circle',
                        children =
            html.Div(
                dash_table.DataTable(
                    id = 'table-time',
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
                )),
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


def get_dataframe_months_years(data, value):
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

def get_dataframe_clients(data, value):
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

def get_client_df(data, client):
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

def check_columns(data_columns):       # if current data columns do not match the expected ones, return False
    expected_columns = ['CodeCustomers', 'NameCustomers', 'SumOrder', 'Date Order']
    return all(column in expected_columns for column in data_columns)

def check_format(content_string, time, tz):
    try:
        decoded = base64.b64decode(content_string)         # if file type is fine, output the new file
        data = pd.read_excel(io.BytesIO(decoded))
        fileInfo = 'В момента разглеждате данните за файл, последно обновен на {}. Местно време: {}.'.format(time, tz)
    except:                                                     # if file type is wrong, output test file
        fileInfo = "Грешка: неправилен формат на файла. Качването неуспешно: в момента разглеждате тестов файл."
        data = pd.read_excel('Test.xls')
    finally:
        return data, fileInfo

"""CallBacks"""

@app.callback( ## output json in hidden div
    [Output('hidden-div', 'children'),
    Output('file-info', 'children')],
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified')
)
def parse_contents(contents, filename, unix_time):
    if contents is None:          ## level 1: if nothing is uploaded, the contents are the test file
        data = pd.read_excel('Test.xls')
        fileInfo = 'В момента разглеждате данните за предишен файл. Моля дръпнете желания от Вас файл в кутийката отгоре.'
    else: 
        content_type, content_string = contents.split(',')
        local_timezone = tzlocal.get_localzone()   ## get tz timezone
        time = datetime.datetime.fromtimestamp(unix_time, local_timezone).strftime('%d-%m-%Y  %H:%M:%S')
        data, fileInfo = check_format(content_string, time, local_timezone)   # level 2: format. Returns uploaded file if format ok, test file if wrong format => works
        if check_columns(data.columns):    ## level 3: columns. If columns ok (TRUE), keep data and fileInfo from above
            pass
        else:              ## if columns wrong (FALSE), replace data with test file again and fileInfo with suitable error message
            data = pd.read_excel('Test.xls')
            fileInfo = "Грешкa в имената на колоните. Качването неуспешно: в момента разглеждате тестов файл."
    #
    # process data
    # delete rows with NА values
    data.dropna(axis = 0, 
                how = 'any',
                thresh = None,
                subset = None, 
                inplace = True)
    #if Date is a string, convert it to a datetime format for further processing
    if type(data['Date Order']) is str: 
        data['Date Order'] = data['Date Order'].apply(dateutil.parser.parse, dayfirst = True)
    else: 
        pass 
    data['month'] = data['Date Order'].dt.month.astype('int64')
    data['year'] = data['Date Order'].dt.year.astype('int64')
    data['day'] = data['Date Order'].dt.day.astype('int64')
    data['date'] = data['Date Order'].dt.date.astype('category')      ##date is an object, Date Order is a datetime object

    return data.to_json(), fileInfo  ## json string format used for transporting data

@app.callback(   ## this will populate the individual components
    Output('customer-choice','options'),
    Input('hidden-div','children'))
def get_customer_names(contents):
    df = pd.read_json(contents)
    options = [ {'label': l, 'value': l} 
               for l in df['NameCustomers'].unique()
                        ]
    return options

@app.callback(   ## this will populate the individual components
    [Output('year-checklist','options'),
     Output('year-checklist', 'value')],
    Input('hidden-div','children'))
def get_years(contents):
    df = pd.read_json(contents)
    options = [{'label': str(y), 'value': y, 'disabled':False} 
               for y in df['year'].unique()]
    value = [x for x in df['year'].unique()]
             
    return options, value

@app.callback(
    Output('top-clients', 'children'),
    [Input('hidden-div', 'children'),  ## contents
     Input('top-client-btn','n_clicks'),  ## clicks
     State('slider-month','value'),
     State('year-checklist','value'),
     State('n-clients-dropdown','value')]
    )
def show_top_clients(contents, n_clicks, months, years, n):
    df = pd.read_json(contents)
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
    [Input('hidden-div', 'children'),
     Input('customer-choice','value')
     ]
    )
def print_client_summary(contents, client):
    mean_all = int()
    sum_all = int()
    df = pd.read_json(contents)   ## extract data from uploaded file
    dfall, dfmean, dfsum, dfmin, dfmax = get_client_df(df, client)
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
    [Input('hidden-div', 'children'),
     Input('customer-choice','value')
     #Input('year-checklist','value'),
     #Input('slider-month','value')
     ]
    )
def client_month_plot(contents, client):
    df = pd.read_json(contents)
    _, _, dfsum, _, _ = get_client_df(df, client)
    dff = dfsum
    title = 'Общи продажби зa {}'.format(client)
    if client:
        return html.Div(         ## return the graph
                [
                    dcc.Graph(
                        figure={
                            "data":[
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
    
    
    

# =============================================================================
# @app.callback(
#     Output('client-graph', 'children')
#     [Input('customer-choice','value'),
#      Input('year-checklist','value'),
#      Input('slider-month','value')]
#     )
# def client_linegraph()
# =============================================================================

@app.callback(
    [Output('table-time', 'data'),
    Output('table-time', 'columns')],             ## update table when changes happen (here only sorting)
   [Input('hidden-div','children'),
    Input('table-time', "sort_by"),
    Input('display-type','value'),
    State('display-type','value')])
def sort_time_table(contents, sort_by,display_input,display_state):
    df = pd.read_json(contents)
    dff = get_dataframe_months_years(df, display_state)
    columns = [{'name': i, 'id': i} for i in (dff.columns)]
    if len(sort_by):
        dff = dff.sort_values(
            [col['column_id'] for col in sort_by],
            ascending=[
                col['direction'] == 'asc'
                for col in sort_by
            ],
            inplace=False
        )
    return dff.to_dict('records'), columns
        

@app.callback(                      ## update table when change page, filter or sort by
    [Output('table', "data"),
    Output('table', "columns")],
    [Input('hidden-div','children'),
     Input('table', "page_current"),
     Input('display-type','value'),
     Input('table', "page_size"),
     Input('table', "sort_by"),
     Input('table', "filter_query"),
     State('display-type','value')])
def update_table(contents, page_current, display_input, page_size, sort_by, filter, display_state):
    df = pd.read_json(contents)
    filtering_expressions = filter.split(' && ')
    dff = get_dataframe_clients(df, display_state)
    columns = [{'name': i, 'id': i} for i in (dff.columns)]
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
    ].to_dict('records'), columns


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
                            'x': dff.loc[dff['year'] == y]['month'],
                            'y': dff.loc[dff['year'] == y]['SumOrder'],
                            'type': 'bar',
                            'name': str(y)}
                            for y in dff['year'].unique()
                            
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
    Input('table', "data"),
    State('display-type','value')
    )
def update_graph(rows, display_state):
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