from datetime import date
from os import name
from wordcloud import WordCloud
import en_core_web_sm
from PIL import Image
import time
import dash
from dash_bootstrap_components import icons
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import Services as sv
from plotly import graph_objects as go


app = dash.Dash(name=__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.config.suppress_callback_exceptions=True
api = sv.Service()
# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
#CONFIG
num_years = 4
max_date_allowed = date.today();
min_date_allowed = date(max_date_allowed.year-num_years, max_date_allowed.month,max_date_allowed.day)
alice_mask = np.array(Image.open('./'+app.get_asset_url('cloudblack.png')))
#--------------COMPONENTS-----------
#NAVBAR
navbarDash =dbc.NavbarSimple(children=
    [
        dbc.NavLink("VENTAS", href="/ventas", active="exact"),
                dbc.NavLink("TOP 10", href="/top", active="exact"),
                dbc.NavLink("COMENTARIOS", href="/comentarios", active="exact"),
    ],
    className='navbarStyle',
    brand="DASHBOARD ALIEXPRES",
    brand_href="#",
    color="#1E3D58",
    dark=True,
    ) 

#---------------MAIN CONTENT-----------------
contentDash = html.Div(id="page-content", children=[])
#VENTAS PRECIO
contentVentas = dbc.Container([
    dbc.Row(
        dbc.Col(
                html.H2(children='VENTAS Y PRECIOS POR FECHA'),
            className="mt-4 mb-2"
        )
    ),
    dbc.Row([
        dbc.Col(dbc.Input(id='inputProductVentas',type='text')
            ,className="col-md-4 col-12 p-3 text-center"),
        dbc.Col(
            dcc.DatePickerRange(
                id='date-range',
                minimum_nights=5,
                clearable=True,
                with_portal=True,
                end_date=max_date_allowed,
                max_date_allowed=max_date_allowed,
                min_date_allowed=min_date_allowed,
                )
            ,className="col-md-6 col-12 p-3 text-center"),
        dbc.Col(dbc.Button('ACEPTAR',id='btnVentas')
            ,className="col-md-2 col-12 p-3 text-center")
     ] ,style={'maxWidth':'800px'}),
    dbc.Spinner( html.Div(id='productVentas', children='Ingrese los datos para mostrar la grafica'),spinner_style={"width": "3rem", "height": "3rem"}),
],
style = {'color' : '#E8EEF1'}
)
#TOP 10
options = [
    {"label": "Evaluacion Ascendente", "value": "EVALUATE_RATE_ASC"},
    {"label": "Evaluacion Descendente", "value": "EVALUATE_RATE_DESC"},
    {"label": "Reviews Ascendente", "value": "REVIEW_TREND_ASC"},
    {"label": "Reviews Descendente", "value": "REVIEW_TREND_DESC"},
]
#LAST_VOLUME_ASC,LAST_VOLUME_DESC,PRICE_TREND_ASC,PRICE_TREND_DESC,REVIEW_TREND_ASC,REVIEW_TREND_DESC,SALE_PRICE_DESC,SALE_PRICE_ASC,SALE_TREND_ASC,SALE_TREND_DESC
contentTop = dbc.Container([
    dbc.Row(
        dbc.Col(
                html.H2(children='TOP 10 ARTICULOS'),
            className="mt-4 mb-2"
        )
    ),
    dbc.Row([
        dbc.Col(dbc.Input(id='inputProductTop',type='text')
            ,className="col-md-4 col-12 p-3 text-center"),
        dcc.Dropdown(id="my-dynamic-dropdown",options=options),
        dbc.Col(dbc.Button('ACEPTAR',id='btnTop')
            ,className="col-md-2 col-12 p-3 text-center")
     ] ,style={'maxWidth':'800px'}),
    dbc.Spinner( html.Div(id='topten', children='Ingrese producto'),spinner_style={"width": "3rem", "height": "3rem"}),
],
style = {'color' : '#E8EEF1'}
)
#COMENTARIOS
contentComentarios = dbc.Container([
    dbc.Row(
        dbc.Col(
                html.H2(children='QUE SE DICE DEL ARTICULO'),
            className="mt-4 mb-2"
        )
    ),
    dbc.Row([
        dbc.Col(dbc.Input(id='inputProductComentario',type='text')
            ,className="col-md-4 col-12 p-3 text-center"),
        dbc.Col(dbc.Button('ACEPTAR',id='btnComentario')
            ,className="col-md-2 col-12 p-3 text-center")
     ] ,style={'maxWidth':'800px'}),
    dbc.Spinner( html.Div(id='comentarios', children='Ingrese producto'),spinner_style={"width": "3rem", "height": "3rem"}),
],
style = {'color' : '#E8EEF1'}
)
#FOTTER INFO
footerDash = dbc.Container([
        dbc.Row([   
            dbc.Col([
                dbc.Row([html.P("RapisApi, Magic Aliexpress: https://rapidapi.com/b2g.corporation/api/magic-aliexpress1/")]),
                dbc.Row([html.P("© 2021 Copyright: Ibsan Morales")])
                ]),
        ])
], className="footer text-center p-3    12")

app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    navbarDash,
    contentDash,
    footerDash,
])
#------------CALLBACKS-----------------
#NAVIGATIONS
@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/ventas" or pathname == "/":
        return [
                contentVentas
                ]
    elif pathname == "/top":
        return [
                contentTop
                ]
    elif pathname == "/comentarios":
        return [
                contentComentarios
                ]
    else:
        return [
            html.Div(
            [ 
                dbc.Container([
                    dbc.Row([
                        dbc.Col([
                            html.Span("404", className="text-danger display-1 d-block"),
                            html.Hr(),
                            html.Div(f"El path {pathname} no fue reconocido ...",className="mb-4 lead"),
                        ], className="col-md-12 text-center"),
                    ],className="justify-content-center"),
                ]),
            ],
            className="page-wrap d-flex flex-row align-items-cente"
        )
        ]

#GET DATA FROM ID PRODUCT
@app.callback(
    Output('productVentas', 'children'),
    Input('btnVentas', 'n_clicks'),
    State('inputProductVentas', 'value'),
    State("date-range", "start_date"),
    State("date-range", "end_date"),
)
def update_output(n_clicks, value,start_date,end_date):
    if n_clicks is not None and n_clicks > 0:
        if ( all([value, start_date, end_date])) : 
            if not value.isspace() and ( len(value) and len(start_date) and len(end_date) ) : 
                #GET VOLUMN
                val = value.replace(' ', '%20')
                volumnHistory = api.getProductVolumenHistory(val,start_date,end_date)
                if "error" in volumnHistory:
                    return html.P('Algo salio mal con la peticion',className='text-danger')
                if 'sales' in volumnHistory['data']:
                    return html.P('No se encontro registros de volumen',className='text-secondary')
                #NORMALIZE DICT 
                dfVolumn = pd.json_normalize(data=volumnHistory['data'], record_path=['sales'])
                volumns = dfVolumn[['lastest_volume','modificationDate']].drop_duplicates()
                time.sleep(3)
                #GET PRICES
                priceHistory = api.getProductPriceHistory(value,start_date,end_date)
                print(priceHistory)
                if "error" in priceHistory:
                    return html.P('Algo salio mal con la peticion',className='text-danger')
                if 'prices' in priceHistory['data']:
                    return html.P('No se encontro registros precios',className='text-secondary')
                #NORMALIZE DICT 
                dfPrices = pd.json_normalize(data=priceHistory['data'], record_path=['prices'])
                prices = dfPrices[['sale_price','modificationDate']].drop_duplicates()
                #merge
                dfPriceVolumn = volumns.merge(prices, on='modificationDate', how='outer').sort_values(by='modificationDate')
                #RENAME
                dfPriceVolumn.rename(columns={'modificationDate':'Fecha','lastest_volume':'Volumen','sale_price':'Precio'}, inplace = True)
                dfPriceVolumn.set_index("Fecha", inplace = True)
                #MEAN
                avgPrice = dfPriceVolumn['Precio'].mean()
                avgVolumn = dfPriceVolumn['Volumen'].mean()
                #MAKE PLOT FIG
                contentGraph = makePriceVolumn(dfPriceVolumn,avgPrice,avgVolumn)
                #if result!= 
                return contentGraph
            else: return html.P('no se permiten campos vacios',className='text-danger')
        else:
            return html.P('Se require fecha y producto ID',className='text-danger')
    return html.P('Buscar para mostrar resultados',className='text-secondary')
def makePriceVolumn(dfPriceVolumn,avgPrice,avgVolumn):
    #PRECIO 
    figPrices = px.scatter(dfPriceVolumn,dfPriceVolumn.index,dfPriceVolumn['Precio'], color="Precio", color_continuous_scale='bluered')
    figPrices.update_yaxes(title_text="<b>PRECIO</b> Dolar")
    figPrices.update_xaxes(title_text="FECHA")
    figPrices.update_traces(marker=dict(size=5,
                                line=dict(width=1,
                                            color='DarkSlateGrey')),
                    selector=dict(mode='markers')) 
    figPrices.update_coloraxes(showscale=False)   
    graphPrice = dcc.Graph(
        id='example-graph',
        figure=figPrices
            )
    #VOLUMEN
    figVolumn = px.scatter(dfPriceVolumn,dfPriceVolumn.index,dfPriceVolumn['Volumen'], color="Volumen", color_continuous_scale='portland')
    figVolumn.update_yaxes(title_text="<b>VOLUMEN</b> Unidades")
    figVolumn.update_xaxes(title_text="FECHA")
    figVolumn.update_traces(marker=dict(size=5,
                                line=dict(width=1,
                                            color='DarkSlateGrey')),
                    selector=dict(mode='markers'))
    figVolumn.update_coloraxes(showscale=False)   
    graphVolumn = dcc.Graph(
        id='example-graph',
        figure=figVolumn
            )
    allGraphContent = dbc.Container([
        dbc.Row([   
            dbc.Col([graphPrice],className="col-md-10 text-center align-middle"),
            dbc.Col([makeCardComponent(avgPrice,"Dolar")],className="col-md-2 col-sm-10 mx-auto")
        ],className="align-items-center text-center"),
         dbc.Row([   
            dbc.Col([graphVolumn],className="col-md-10 text-center align-middle"),
            dbc.Col([makeCardComponent(avgVolumn,"Unidades")],className="col-md-2 col-sm-10 mx-auto")
        ],className="align-items-center text-center")
    ])

    return allGraphContent
#GET TOP 10
@app.callback(
    Output('topten', 'children'),
    Input('btnTop', 'n_clicks'),
    State('inputProductTop', 'value'),
    State("my-dynamic-dropdown", "value"),
)
def update_output(n_clicks, value_input,value_dropdown):
    if n_clicks is not None and n_clicks > 0:
        if ( all([value_input, value_dropdown])) :
            if not value_input.isspace() and ( len(value_input) and len(value_dropdown) ) : 
                val = value_input.replace(' ', '%20')
                topArticulos = api.getProductsbyBestSales(val,value_dropdown)
                if "error" in topArticulos:
                    return html.P('Algo salio mal con la peticion',className='text-danger')
                if topArticulos['data']['totalDocs'] == 0:
                    return html.P('No se encontro registros',className='text-secondary')
                #JSON to DATAFRAME
                dfTop = pd.json_normalize(data=topArticulos['data'], record_path=['docs'])
                #Drop Duplicates
                dfTop.drop_duplicates(subset=['product_id'], inplace=True)
                #SELECTE TOP 10 and COlUMNS
                dfTop10 = dfTop[:10]
                dfTop10["product_id"] = dfTop10["product_id"].astype('object')
                shortTop10 = dfTop10[["product_id", "product_title","sale_price","evaluate_rate","lastest_volume","product_main_image_url"]].sort_values("sale_price").reset_index(drop=True)
                contentTop = makeTop10Grap(shortTop10)
                return contentTop

            else: return html.P('no se permiten campos vacios',className='text-danger')
    return html.P('Llene campos para realizar la busqueda',className='text-secondary')
def makeTop10Grap(shortTop10):
    figTop = make_subplots(rows=3, cols=1, 
                    subplot_titles=("<b>Precio por articulo</b>", "<b>Evaluacion por articulo</b>", "<b>Volumen por articulo</b>"),
                    vertical_spacing = 0.10
                        )
    figTop.add_trace(
        go.Bar(
            name="",
            showlegend = False,
            x=shortTop10["sale_price"],
            y=shortTop10["product_id"],
            orientation = "h",
            text=shortTop10["sale_price"],
            textposition = "auto",
            hovertext=shortTop10["product_title"],
            hovertemplate="%{hovertext}",
        ),
        row=1,
        col=1,
    )
    figTop.add_trace(
        go.Bar(
            name="",
            showlegend = False,
            x=shortTop10["evaluate_rate"],
            y=shortTop10["product_id"],
            orientation = "h",
            text=shortTop10["evaluate_rate"],
            textposition = "auto",
            hovertext=shortTop10["product_title"],
            hovertemplate="%{hovertext}",
        ),
        row=2,
        col=1,
    )
    figTop.add_trace(
        go.Bar(
            name="",
            showlegend = False,
            x=shortTop10["lastest_volume"],
            y=shortTop10["product_id"],
            orientation = "h",
            text=shortTop10["lastest_volume"],
            textposition = "auto",
            hovertext=shortTop10["product_title"],
            hovertemplate="%{hovertext}"
        ),
        row=3,
        col=1,
    )
    figTop.update_traces( marker_line_width=1, opacity=0.8)
    figTop.update_layout(yaxis_type='category', plot_bgcolor  ='rgba(0,0,0,0)', hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Rockwell"
        ))
    figTop.update_layout(yaxis2_type='category', plot_bgcolor  ='rgba(0,0,0,0)', hovermode = 'closest')
    figTop.update_layout(yaxis3_type='category', plot_bgcolor  ='rgba(0,0,0,0)',)
    figTop.update_yaxes(title_text="Id Articulo", showgrid=False, row=1, col=1)
    figTop.update_yaxes(title_text="Id Articulo", showgrid=False, row=2, col=1)
    figTop.update_yaxes(title_text="Id Articulo", showgrid=False, row=3, col=1)
    figTop.update_xaxes(title_text="", showgrid=False, row=1, col=1, visible=False)
    figTop.update_xaxes(title_text="", showgrid=False, row=2, col=1, visible=False)
    figTop.update_xaxes(title_text="", showgrid=False, row=3, col=1, visible=False)
    figTop.update_layout(
        autosize=True,
        #width=500,
        height=1500)
    contentTop = dbc.Container([
        dbc.Row([
            dcc.Graph(
                id='top-graph',
                figure=figTop
                    )
        ])
    ])
    return contentTop

#GET COMENTARIOS
@app.callback(
    Output('comentarios', 'children'),
    Input('btnComentario', 'n_clicks'),
    State('inputProductComentario', 'value'),
)
def update_output(n_clicks, value):
    if n_clicks is not None and n_clicks > 0:
        if ( all([value])) : 
            if not value.isspace() and ( len(value) ) : 
                #GET VOLUMN
                idProductoCom = value.replace(' ', '%20')
                comentariosProducto = api.getFeedbacksbyProduct(idProductoCom)
                #Error Validation
                if "error" in comentariosProducto:
                    return html.P('Algo salio mal con la peticion',className='text-danger')
                if len(comentariosProducto['data']['docs']) == 0:
                    return html.P('No se encontro registros de comentarios',className='text-secondary')
                #NORMALIZE DICT 
                dfComentarios = pd.json_normalize(data=comentariosProducto['data'], record_path=['docs'])
                #Average
                ranking = dfComentarios['rating'].mean()
                #CloudWord
                contentCloud = makeWordCloud(dfComentarios)
                return  dbc.Container([
                                dbc.Row([   
                                    dbc.Col([contentCloud],className="col-md-10 text-center align-middle"),
                                    dbc.Col([makeCardComponent(ranking,"Rank")],className="col-md-2 col-sm-10 mx-auto text-center align-middle")
                                ],className="align-items-center text-center"),
                            ])
            else: return html.P('no se permiten campos vacios',className='text-danger')
        else:
            return html.P('Se require fecha y producto ID',className='text-secondary')
    return html.P('Busqueda para generar resultado',className='text-secondary')
def makeWordCloud(dfComentarios):
    words = '\n'.join(dfComentarios['content'])
    nlp = en_core_web_sm.load()
    doc = nlp(words)
    newWords = ' '.join(
    [token.norm_ for token in doc if token.pos_ in ['VERB','ADJ','NOUN','PROPN']]
    )
    wc = WordCloud(background_color="white", max_words=100, mask=alice_mask)
    wc.generate(newWords)
    figCloud = px.imshow(wc)
    figCloud.update_traces(hoverinfo='skip', hovertemplate='')
    figCloud.update_layout(coloraxis_showscale=False,autosize=True, height=500)
    figCloud.update_xaxes(showticklabels=False)
    figCloud.update_yaxes(showticklabels=False)
    contentCloud = dcc.Graph(
        id='cloud-graph',
        figure=figCloud,
        animate=True,
            )
    return contentCloud

#COMOPONENT CARD
def makeCardComponent(value,unid):
    card= html.Div(
                [
                    html.H3(f'{value:9.2f}'),
                    html.P(
                        [
                            html.Code(unid),
                        ],
                        
                    ),
                ],className="cardall card"
            )
    return card


if __name__ == '__main__':
    app.run_server()