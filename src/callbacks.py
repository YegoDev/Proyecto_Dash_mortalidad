from dash import Input, Output, dcc
import plotly.express as px
import pandas as pd
import json
import dash.dash_table as dt
import os

def registrar_callbacks(app, df):
    @app.callback(
        #Output("grafico-principal", "figure"),
        Output("contenedor-visualizacion", "children"),
        Input("selector-grafico", "value")
    )
    def mostrar_grafico(tipo): #Mapa
        if tipo == "mapa":

            # Agrupar total de muertes por departamento
            df_muertes = df.groupby(["COD_DEPARTAMENTO", "DEPARTAMENTO"]).size().reset_index(name="TOTAL_MUERTES")

            # Cargar GeoJSON
            ruta_geojson = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "Colombia_geojson.json"))
            with open(ruta_geojson, encoding="utf-8") as f:
                geojson = json.load(f)

            # Crear choropleth
            fig = px.choropleth(
                df_muertes,
                geojson=geojson,
                featureidkey="properties.DPTO",
                locations="COD_DEPARTAMENTO",
                color="TOTAL_MUERTES",
                hover_name="DEPARTAMENTO",  # 👈 esto es lo que se mostrará como título del tooltip
                hover_data={"COD_DEPARTAMENTO": False, "TOTAL_MUERTES": True},
                color_continuous_scale="Reds",
                title="Distribución total de muertes por departamento."
            )
            fig.update_geos(fitbounds="locations", visible=False)
            fig.update_layout(margin={"r":0,"t":50,"l":0,"b":0})
            #return fig
            return dcc.Graph(figure=fig)

        elif tipo == "muertes_mes":  #Lineas
            # Agrupar por mes
            df_mensual = df.groupby("MES").size().reset_index(name="TOTAL_MUERTES")
            df_mensual = df_mensual.sort_values("MES")

            fig = px.line(
                df_mensual,
                x="MES",
                y="TOTAL_MUERTES",
                markers=True,
                title="Total de muertes por mes y sus variaciones a lo largo del año.",
                labels={"MES": "Mes", "TOTAL_MUERTES": "Muertes"}
            )
            fig.update_layout(xaxis=dict(dtick=1))
            #return fig
            return dcc.Graph(figure=fig)
        
        elif tipo == "top_homicidios": #Barras
            # Filtrar homicidios con código CIE-10 X95*
            df_homicidios = df[df["COD_MUERTE"].str.startswith("X95")]

            # Agrupar por municipio y contar
            df_top = df_homicidios.groupby("MUNICIPIO").size().reset_index(name="TOTAL_HOMICIDIOS")
            df_top = df_top.sort_values("TOTAL_HOMICIDIOS", ascending=False).head(5)

            fig = px.bar(
                df_top,
                x="MUNICIPIO",
                y="TOTAL_HOMICIDIOS",
                title="Top 5 de ciudades más violentas, considerando homicidios (códigos X95).",
                labels={"MUNICIPIO": "Ciudad", "TOTAL_HOMICIDIOS": "Cantidad de homicidios"},
                text_auto=True
            )
            #return fig
            return dcc.Graph(figure=fig)
        
        elif tipo == "top_menor_mortalidad": #Circular
            # Agrupar por ciudad
            df_municipios = df[df["MUNICIPIO"].notna()]  # excluir nulos
            df_bajas = df_municipios.groupby("MUNICIPIO").size().reset_index(name="TOTAL_MUERTES")
            df_bajas = df_bajas.sort_values("TOTAL_MUERTES", ascending=True).head(10)

            fig = px.pie(
                df_bajas,
                names="MUNICIPIO",
                values="TOTAL_MUERTES",
                title="Top 10 de ciudades con menor número de muertes."
            )
            #return fig
            return dcc.Graph(figure=fig)
        
        elif tipo == 'top_causas_muerte': #Tabla
            # Agrupar y ordenar causas por frecuencia
            df_causas = (
                df.groupby(["CODIGO_CIE10_4C", "DESCRIPCION_CIE_4C"])
                .size()
                .reset_index(name="TOTAL_CASOS")
                .sort_values("TOTAL_CASOS", ascending=False)
                .head(10)
            )

            return dt.DataTable(
                columns=[
                    {"name": "Código CIE-10", "id": "CODIGO_CIE10_4C"},
                    {"name": "Descripción", "id": "DESCRIPCION_CIE_4C"},
                    {"name": "Total de Casos", "id": "TOTAL_CASOS", "type": "numeric", "format": {"locale": {"group": ","}}}
                ],

                data=df_causas.to_dict("records"),
                style_table={"overflowX": "auto"},
                style_cell={"padding": "6px", "textAlign": "left"},
                style_header={
                    "backgroundColor": "#f0f0f0",
                    "fontWeight": "bold"
                },
                page_size=10
            )
        
        elif tipo == "muertes_edad": #Histograma
            df_edad = df[df["GRUPO_EDAD1"].notna()]

            bins = list(range(0, 90, 5)) + [150]
            labels = [f"{i}-{i+4}" for i in range(0, 85, 5)] + ["85+"]

            df_edad["RANGO_EDAD"] = pd.cut(df_edad["GRUPO_EDAD1"], bins=bins, labels=labels, right=False)
            df_rangos = df_edad["RANGO_EDAD"].value_counts().sort_index().reset_index()
            df_rangos.columns = ["RANGO_EDAD", "TOTAL_MUERTES"]
            fig = px.bar(
                df_rangos,
                x="RANGO_EDAD", 
                y="TOTAL_MUERTES",
                title="Distribución de muertes por rango de edad (quinquenales)",
                labels={"RANGO_EDAD": "Rango de Edad", "TOTAL_MUERTES": "Total de Muertes"},
                text_auto=True
            )

            fig.update_layout(xaxis_title="Rango de Edad", yaxis_title="Total de Muertes")

            return dcc.Graph(figure=fig)
    
        elif tipo == "sexo_departamento": #Barras apiladas
            df_sexo = df[df["SEXO"].isin([1, 2, 3, "1", "2", "3"])].copy() #Homologo 1-Hombre, 2-Mujer 
            df_sexo.loc[:, "SEXO"] = df_sexo["SEXO"].replace({
                "1": "Hombre",
                "2": "Mujer", 
                "3": "Sin identificar"
            })

            df_sexo["COD_DEPARTAMENTO"] = df_sexo["COD_DEPARTAMENTO"].astype(str).str.zfill(2)

            # Agrupar por departamento y sexo
            df_sexo_agg = (
                df_sexo.groupby(["DEPARTAMENTO", "SEXO"])
                .size()
                .reset_index(name="TOTAL_MUERTES")
            )

            # Crear gráfico de barras apiladas
            fig = px.bar(
                df_sexo_agg,
                x="DEPARTAMENTO",
                y="TOTAL_MUERTES",
                color="SEXO",
                barmode="stack",
                title="Comparación del total de muertes por sexo en cada departamento",
                labels={"TOTAL_MUERTES": "Total de Muertes", "DEPARTAMENTO": "Departamento"},
            )

            fig.update_layout(xaxis_tickangle=-45)

            return dcc.Graph(figure=fig)