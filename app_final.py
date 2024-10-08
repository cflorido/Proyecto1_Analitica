import dash
from dash import dcc  # dash core components
from dash import html # dash html components 
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
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
        
        html.H6("Introduzca los valores promedios para cada factor para determinar la rentabilidad máxima",style={
        'backgroundColor': '#f8d7da',  # Fondo de color rojo pastel suave
        'border': '2px solid #f5c6cb',  # Borde de color rojo más oscuro
        'borderRadius': '10px',  # Bordes redondeados
        'padding': '15px',  # Espaciado interno
        'marginTop': '40px',  # Margen superior
        'boxShadow': '2px 2px 5px rgba(0,0,0,0.1)',  # Sombra de caja
        'color': '#721c24',  # Texto de color rojo oscuro
        'fontWeight': 'bold',  # Texto en negrita
        'fontFamily': 'Arial, sans-serif',  # Fuente
        'textAlign': 'center',  # Centrar el texto
    }),  # Añade espacio entre el título y el contenido

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
        html.Div(
            style={'display': 'flex', 'justifyContent': 'center'},
            children=[
                html.Div(
                    [
                        html.Label("Ingrese la velocidad del viento (m/s):"),
                        dcc.Input(id='windSpeed', value=3, type='number', min=0, step=0.1)
                    ],
                    style={'padding': '10px'}
                ),
                html.Div(
                    [
                        html.Label("Ingrese el nivel de Radiación Solar (MJ/m2)"),
                        dcc.Input(id='solar', value=4, type='number', min=0, step=0.1)
                    ],
                    style={'padding': '10px'}
                ),
                html.Div(
                    [
                        html.Label("Ingrese el porcentaje de humedad"),
                        dcc.Input(id='humidity', value=0.5, type='number', min=0, max=1)
                    ],
                    style={'padding': '10px'}
                ),
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
        dcc.Graph(id='bicycle_time_graph'),
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
box_style2 = {
    'backgroundColor': '#fff8e1',  # Fondo de la caja (un amarillo claro para advertencia)
    'border': '2px solid #ffa726',  # Borde naranja
    'borderRadius': '10px',  # Bordes redondeados
    'padding': '15px',  # Espaciado interno
    'margin': '10px 0',  # Margen externo
    'boxShadow': '2px 2px 5px rgba(0,0,0,0.1)',  # Sombra de caja
    'textAlign': 'center',  # Centrar el texto
    'fontFamily': 'Arial, sans-serif',  # Fuente
    'color': '#d32f2f',  # Color del texto en rojo oscuro para advertencia
}
@app.callback(
    [
        Output('sensitivity_graph', 'figure'),
        Output('sensitivity_graph2', 'figure'),
        Output('productivity_summary', 'children'),
        Output('bicycle_time_graph', 'figure')
    ],
    [
        Input('hour', 'value'),
        Input('temperature', 'value'),
        Input('humidity', 'value'),
        Input('windSpeed', 'value'),
        Input('solar', 'value'),        
        Input('rainfall', 'value'),               
        Input('season', 'value'),
        Input('holiday', 'value'),
        Input('pesos', 'value'),
        Input('won', 'value'),
        Input('cpesos', 'value'),
        Input('cwon', 'value')
    ]
)
def update_figure(hour, temperature, humidity, windSpeed, solar, rainfall, season, holiday,pesos, won,cpesos, cwon):
    # Inicializa la variable 'season_effect' según la estación seleccionada
    
    #Definir lambda
    lamBox = 0.2730547113417922
    season_effect = 0
    if season == 'spring':
        season_effect = -1.687640
    elif season == 'summer':
        season_effect = -1.488615
    elif season == 'winter':
        season_effect = -4.054296
    # Otoño ya es el valor por defecto con coeficiente 0 (sin ajuste)

    # Ajusta el valor del festivo
    holiday_effect = 1.585232 if holiday == 'yes' else 0
    
    # Definir coeficientes por hora
    hour_effects = {
        1: -1.022797, 2: -2.538409, 3: -4.148855, 4: -5.410030,
        5: -5.296757, 6: -2.483916, 7: 0.828508, 8: 3.554421,
        9: 0.628419, 10: -1.619980, 11: -1.346580, 12: -1.081500,
        13: -1.224894, 14: -1.344771, 15: -0.655167, 17: 1.726126,
        18: 4.402927, 19: 2.902046, 20: 2.622502, 21: 2.697714, 22: 2.181438}
    
    # Calcular el efecto de la hora seleccionada
    hour_effect = hour_effects.get(hour, 0)  # Valor por defecto es 0 si no se encuentra

    # Calcular la cantidad de bicicletas con los nuevos coeficientes
    bici = round(((18.863284
                 + hour_effect
                 + temperature * 0.210172
                 + humidity * -0.072198
                 + windSpeed * -0.140848
                 + solar * 0.397738
                 + rainfall * -1.161975
                 + season_effect
                 + holiday_effect)*lamBox + 1)**(1/lamBox)-1)
    
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
            'marker': {'color': 'rgba(186, 85, 211, 0.7)', 'line': {'color': 'rgba(148, 0, 211, 1)', 'width': 2}}},
        ],
        'layout': {
            'title': 'Análisis de Sensibilidad - Precio vs Rentabilidad (WON)',
            'xaxis': {'title': 'Precio (WON)', 'tickangle': -45},
            'yaxis': {'title': 'Rentabilidad (WON)'},
            'plot_bgcolor': 'rgba(245, 245, 245, 1)',  # Fondo de la gráfica
            'paper_bgcolor': 'rgba(255, 255, 255, 1)',  # Fondo del papel
        }
    }
    # Nueva gráfica para cantidad de bicicletas según el rango de horas
    hours_range = list(range(1, hour + 1))
    # Cálculo de bicicletas por hora utilizando los coeficientes categóricos
    bici_per_hour = [
        round(((18.863284
            + hour_effects.get(h, 0)  # Aplicar el coeficiente de la hora categórica
            + temperature * 0.210172
            + humidity * -0.072198
            + windSpeed * -0.140848
            + solar * 0.397738
            + rainfall * -1.161975
            + season_effect
            + holiday_effect)*lamBox + 1)**(1/lamBox)-1)
        for h in hours_range
    ]

    bicycle_time_graph = {
        'data': [
            {
                'x': bici_per_hour,  # La cantidad de bicicletas ahora va en el eje X
                'y': [f'Hora {h}' for h in hours_range],  # Las horas ahora van en el eje Y
                'type': 'bar',
                'orientation': 'h',  # Esto hace que las barras sean horizontales
                'marker': {
                    'color': 'rgba(255, 182, 193, 0.7)',  # Color pastel azul claro
                    'line': {'color': 'rgba(255, 105, 180, 1)', 'width': 2}  # Color del borde azul más fuerte
                }
            }
        ],
        'layout': {
            'title': 'Cantidad de Bicicletas vs Hora',
            'xaxis': {'title': 'Cantidad de Bicicletas'},
            'yaxis': {'title': 'Hora del Día', 'tickangle': 0},  # Mantén las etiquetas de las horas sin rotación
            'plot_bgcolor': 'rgba(245, 245, 245, 1)',  # Fondo de la gráfica en gris claro
            'paper_bgcolor': 'rgba(255, 255, 255, 1)',  # Fondo del papel en blanco
            'bargap': 0.15,  # Espacio entre barras
            'barmode': 'group',  # Modo de agrupación para las barras
            'font': {
                'family': 'Arial, sans-serif',
                'color': '#333333'  # Color de fuente en gris oscuro
            }
        }
    }
    total_bici_range = sum(bici_per_hour)
    summary = html.Div([
        html.H4("Resumen del Análisis"),
        html.P(f"Suma del rango de bicicletas: {total_bici_range:.2f} unidades"),
        html.P(f"Rentabilidad en COP: {rentabilidad_pesos:.2f}"),
        html.P(f"Rentabilidad en KRW: {rentabilidad_won:.2f}"),
        
        # Caja de advertencia
        html.Div([
            html.H5("Advertencia del Modelo", style={'color': '#d32f2f'}),
            html.P("Incumple con el supuesto de Homocedasticidad y Especificación"),
        ], style=box_style2)
        
    ], style=box_style)

    return figure_sensitivity, figure_sensitivity2,summary, bicycle_time_graph

if __name__ == '__main__':
    app.run_server(debug=True)