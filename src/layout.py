from dash import html, dcc
from estilos import dropdown_style, contenedor_principal_style, footer_style, titulo_principal_style, descripcion_app_style

def generar_layout():
    return html.Div([
        html.H1("Gráficas de mortalidad en Colombia para el año 2019", style=titulo_principal_style),
        html.Div("Esta aplicación permite visualizar y explorar datos de mortalidad registrados en Colombia, con diferentes filtros como causas de muerte, edad, sexo y distribución geográfica.", style=descripcion_app_style),

        # Selector de tipo de gráfico
        dcc.Dropdown(
            options=[
                {"label": "Mapa de muertes por departamento", "value": "mapa"},
                {"label": "Muertes por mes en Colombia", "value": "muertes_mes"}, 
                {"label": "Top 5 ciudades más violentas, por homicidios", "value": "top_homicidios"},
                {"label": "Top 10 ciudades con menor mortalidad", "value": "top_menor_mortalidad"}, 
                {"label": "Listado de 10 principales causas de muerte", "value": "top_causas_muerte"}, 
                {"label": "Distribución de muertes por rango de edad quinquenal", "value": "muertes_edad"}, 
                {"label": "Muertes por sexo y departamento", "value": "sexo_departamento"}
            ],
            value="mapa",
            id="selector-grafico", 
            style=dropdown_style
        ),

        #dcc.Graph(id="grafico-principal"),
        html.Div(id="contenedor-visualizacion"),
        html.Hr(),
        generar_footer()
    ], style=contenedor_principal_style)

def generar_footer():
    return html.Footer([
        html.P("Desarrollador por: Yeison Esteven García Olaya"),
        html.P("Aplicaciones I - 2025"),
        html.P("Maestría en IA - Universidad de la Salle")
    ], style=footer_style)