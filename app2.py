import dash
from dash import dcc  # dash core components
from dash import html # dash html components 
from dash.dependencies import Input, Output
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div(
    style={'textAlign': 'center', 'padding': '20px'},  # Centra el contenido general
    children=[
        # Cuadro de color que contiene el título
        html.Div(
            style={'backgroundColor': '#CDE8E5', 'padding': '30px', 'borderRadius': '10px'},  # Color de fondo y borde del cuadro
            children=[
                html.H1(
                    "Análisis de Datos y Financiero para el Servicio de Bicicletas Compartidas",
                    style={'fontSize': '40px', 'fontWeight': 'bold', 'color': '#333333'}  # Ajusta el estilo del título
                )
            ]
        ),
        html.H6("Modifique el valor de los factores para determinar la rentabilidad máxima", style={'marginTop': '40px'}),  # Añade espacio entre el título y el contenido

        # Caja de texto para la hora del día
        html.Div(["Ingrese la hora del día: ",
                  dcc.Input(id='hour', value=12, type='number', min=0, max=23)]),
        html.Br(),
        # Slider para la temperatura
        html.Div("Seleccione la temperatura (°C):"),
        dcc.Slider(
            id='temperature',
            min=-20,
            max=40,
            step=5,
            value=20,
            marks={i: f'{i}°C' for i in range(-20, 41, 10)},
        ),
        html.Br(),
        # Caja de texto para humedad
        html.Div(["Ingrese el porcentaje de humedad: ",
                  dcc.Input(id='humidity', value=0.5, type='number', min=0, max=1)]),
        html.Br(),

        html.Div(
            style={'display': 'flex', 'justifyContent': 'center'},
            children=[
                html.Div(
                    [
                        html.Label("Ingrese la velocidad del viento (m/s):"),
                        dcc.Input(id='windSpeed', value=3, type='number', min=0, step=1)
                    ],
                    style={'padding': '10px'}
                ),
                html.Div(
                    [
                        html.Label("Ingrese el nivel de Radiación Solar (MJ/m2)"),
                        dcc.Input(id='solar', value=4, type='number', min=0, step=1)
                    ],
                    style={'padding': '10px'}
                )
            ]
        ),
        # Slider para el nivel de lluvia
        html.Div("Seleccione el nivel de lluvia (mm):"),
        dcc.Slider(
            id='rainfall',
            min=0,
            max=35,
            step=1,
            value=5,
            marks={i: f'{i} mm' for i in range(0, 36, 5)},
        ),
        # Slider para el nivel de nieve
        html.Div("Seleccione el nivel de nieve (cm):"),
        dcc.Slider(
            id='snowfall',
            min=0,
            max=35,
            step=1,
            value=5,
            marks={i: f'{i} cm' for i in range(0, 36, 5)},
        ),
        # Dropdown para seleccionar la estación del año
        html.Div("Seleccione la estación del año:"),
        dcc.Dropdown(
            id='season',
            options=[
                {'label': 'Primavera', 'value': 'spring'},
                {'label': 'Verano', 'value': 'summer'},
                {'label': 'Otoño', 'value': 'fall'},
                {'label': 'Invierno', 'value': 'winter'},
            ],
            value='spring',
            clearable=False,
        ),
        html.Br(),
        
        # Dropdown para seleccionar si es festivo
        html.Div("¿Es festivo?:"),
        dcc.Dropdown(
            id='holiday',
            options=[
                {'label': 'Sí', 'value': 'yes'},
                {'label': 'No', 'value': 'no'},
            ],
            value='no',
            clearable=False,
        ),
        html.Br(),
        
        html.Div(
            style={'display': 'flex', 'justifyContent': 'center'},
            children=[
                html.Div(
                    [
                        html.Label("Ingrese el precio en pesos colombianos:"),
                        dcc.Input(id='pesos', value=2500, type='number', min=0, step=500)
                    ],
                    style={'padding': '10px'}
                ),
                html.Div(
                    [
                        html.Label("Ingrese el precio en won surcoreano:"),
                        dcc.Input(id='won', value=3000, type='number', min=0, step=500)
                    ],
                    style={'padding': '10px'}
                )
            ]
        ),
        html.Div(
            style={'display': 'flex', 'justifyContent': 'center'},
            children=[
                html.Div(
                    [
                        html.Label("Los costos operativos unitarios en pesos colombianos:"),
                        dcc.Input(id='cpesos', value=1500, type='number', min=0, step=100)
                    ],
                    style={'padding': '10px'}
                ),
                html.Div(
                    [
                        html.Label("Los costos operativos unitarios en Won surcoreano:"),
                        dcc.Input(id='cwon', value=1000, type='number', min=0, step=100)
                    ],
                    style={'padding': '10px'}
                )
            ]
        ),
        
        # Salida del callback
        html.Div(id='my-output'),
        html.H5("Resultados de Rentabilidad"),
        dcc.Graph(id='sensitivity_graph'),  # Componente de gráfica para análisis de sensibilidad
        dcc.Graph(id='sensitivity_graph2'),
        html.Div(id='productivity_summary')  
    ]
)
box_style = {
    'backgroundColor': '#f0f8ff',  # Fondo de la caja (un azul claro)
    'border': '2px solid #8bbdd9',  # Borde azul
    'borderRadius': '10px',  # Bordes redondeados
    'padding': '15px',  # Espaciado interno
    'margin': '10px 0',  # Margen externo
    'boxShadow': '2px 2px 5px rgba(0,0,0,0.1)',  # Sombra de caja
    'textAlign': 'center',  # Centrar el texto
    'fontFamily': 'Arial, sans-serif',  # Fuente
    'color': '#333333',  # Color del texto
}
# Callback para actualizar el resultado basado en las entradas
@app.callback(
    [
        Output('sensitivity_graph', 'figure'),
        Output('sensitivity_graph2', 'figure'),
        Output('productivity_summary', 'children')
    ],
    [
        Input('hour', 'value'),
        Input('temperature', 'value'),
        Input('humidity', 'value'),
        Input('windSpeed', 'value'),
        Input('solar', 'value'),        
        Input('rainfall', 'value'),
        Input('snowfall', 'value'),               
        Input('season', 'value'),
        Input('holiday', 'value'),
        Input('pesos', 'value'),
        Input('won', 'value'),
        Input('cpesos', 'value'),
        Input('cwon', 'value')
    ]
)
def update_figure(hour, temperature, humidity, windSpeed, solar, rainfall, snowfall, season, holiday,pesos, won,cpesos, cwon):
    # Inicializa la variable 'season_effect' según la estación seleccionada
    season_effect = 0
    if season == 'spring':
        season_effect = -144.851750
    elif season == 'summer':
        season_effect = -158.982762
    elif season == 'winter':
        season_effect = -368.205780
    # Otoño ya es el valor por defecto con coeficiente 0 (sin ajuste)

    # Ajusta el valor del festivo
    holiday_effect = 128.337445 if holiday == 'yes' else 0

    # Regresión para calcular la cantidad de bicicletas según los factores
    bici = round(642.850656
            + hour * 27.804568
            + temperature * 27.191647
            + humidity * -8.631740
            + windSpeed * 16.505881
            + solar * -87.836559
            + rainfall * -68.643147
            + snowfall * 36.696809
            + season_effect
            + holiday_effect)
    
    # Cálculo de rentabilidad
    rentabilidad_pesos = (bici * pesos)-(cpesos*bici)
    rentabilidad_won = (bici * won)-(cwon*bici)

    # Análisis de sensibilidad con variación en el precio
    precios_range = list(range(max(0, pesos - 500), pesos + 501, 100))
    rentabilidad_sensibilidad = [(bici * p) - (cpesos * bici) for p in precios_range]

    # Análisis de sensibilidad con variación en el precio won
    precios_range2 = list(range(max(0, won - 500), won + 501, 100))
    rentabilidad_sensibilidad2 = [(bici * e) - (cwon * bici) for e in precios_range2]

    figure_sensitivity = {
    'data': [
        {'x': precios_range, 'y': rentabilidad_sensibilidad, 'type': 'bar', 'name': 'Rentabilidad (COP)', 
         'marker': {'color': 'rgba(55, 128, 191, 0.7)', 'line': {'color': 'rgba(55, 128, 191, 1)', 'width': 2}}},
    ],
    'layout': {
        'title': 'Análisis de Sensibilidad - Precio vs Rentabilidad (COP)',
        'xaxis': {'title': 'Precio (COP)', 'tickangle': -45},
        'yaxis': {'title': 'Rentabilidad (COP)'},
        'plot_bgcolor': 'rgba(245, 245, 245, 1)',  # Fondo de la gráfica
        'paper_bgcolor': 'rgba(255, 255, 255, 1)',  # Fondo del papel
    }
    }
    figure_sensitivity2 = {
        'data': [
            {'x': precios_range2, 'y': rentabilidad_sensibilidad2, 'type': 'bar', 'name': 'Rentabilidad (WON)', 
            'marker': {'color': 'rgba(255, 153, 51, 0.7)', 'line': {'color': 'rgba(255, 153, 51, 1)', 'width': 2}}},
        ],
        'layout': {
            'title': 'Análisis de Sensibilidad - Precio vs Rentabilidad (WON)',
            'xaxis': {'title': 'Precio (WON)', 'tickangle': -45},
            'yaxis': {'title': 'Rentabilidad (WON)'},
            'plot_bgcolor': 'rgba(245, 245, 245, 1)',  # Fondo de la gráfica
            'paper_bgcolor': 'rgba(255, 255, 255, 1)',  # Fondo del papel
        }
    }

    # Texto de resumen con predicciones
    summary = html.Div([
        html.H4("Resumen del Análisis"),
        html.P(f"Predicción de bicicletas: {bici:.2f} unidades"),
        html.P(f"Rentabilidad en COP: {rentabilidad_pesos:.2f}"),
        html.P(f"Rentabilidad en KRW: {rentabilidad_won:.2f}")
    ], style=box_style)
    return figure_sensitivity, figure_sensitivity2,summary

if __name__ == '__main__':
    app.run_server(debug=True)