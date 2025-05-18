from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px

#Crear la aplicación dash 
app = Dash()

#Cargar el conjunto de datos 
df = px.data.gapminder()

app.layout = html.Div([
    #Título principal 
    html.H1("Esto es un dashboard", style={'textAlign':'center'}), 
    dcc.Dropdown(
        df.country.unique(),
        'Colombia',
        id='dropdown-pais' 
    ),

    dcc.Graph(id='grafico-lineal')
])

@callback(
    Output('grafico-lineal', 'figure'), 
    Input('dropdown-pais', 'value')
)
def actualizar_grafico(pais): 
    df_filtrado = df[df['country'] == pais]

    fig = px.line(df_filtrado, x='year', y='gdpPercap', 
                title=f'PIB per capita de {pais}', 
                labels={'year':'año', 'gdpPercap': 'PIB per capita '})

    return fig

if __name__ == '__main__': 
    app.run(debug=True)
