from dash import Dash, dcc
from carga_datos import cargar_datos, transformar_datos
from layout import generar_layout
from callbacks import registrar_callbacks

df_hechos, df_causa, df_loc = cargar_datos()
df = transformar_datos(df_hechos, df_causa, df_loc)

app = Dash(__name__, title="Mortalidad en Colombia - 2019")
server = app.server

#app.layout = generar_layout()
app.layout = dcc.Loading(
    id="spinner-inicial",
    type="circle",
    fullscreen=True,
    children=generar_layout()
)
registrar_callbacks(app, df)

if __name__ == "__main__":
    app.run(debug=True)