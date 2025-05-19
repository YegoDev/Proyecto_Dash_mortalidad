## **APLICACIÓN WEB INTERACTIVA**
Yeison Esteven García Olaya  
Repositorio del proyecto: https://github.com/YegoDev/Proyecto_Dash_mortalidad.git

### Tabla de Contenido

1. [Introducción](#introducción)
2. [Estructura](#Estructura)
3. [Visualizaciones](#visualizaciones)
4. [Despliegue de la aplicación](#despliegue)

## Nota:  
Este fichero no reeplaza el informe realizado, el cual fue enviado por la actividad de Moodle. 

## Introducción  
Se detallará el uso de Dash para la construcción de una aplicación web compuesta por siete gráficos, relacionados con los datos de fallecimientos registrados en Colombia para el año 2019. En este sentido, se describirá la estructura y el funcionamiento del proyecto desarrollado, así como el procedimiento llevado a cabo para su despliegue en la plataforma Render, accesible a través del enlace: https://proyecto-dash-mortalidad.onrender.com.

## Estructura  
Pensando en el despliegue de las aplicaciones en Render, es necesario garantizar la existencia de la carpeta ***src/*** que contendrá, como mmínimo, el modulo ***app.py***. Asi mismo, en la raiz de proyecto se tendran los ficheros ***requirements.txt*** y ***render.yaml**. 

- proyecto_DASH_mortalidad/
  - README.md
  - requirements.txt 
  - render.yaml
  - data/
    - anexo1.csv
    - Anexo2.CodigosDeMuerte_CE_15-03-23.csv
    - Anexo3.Divipola_CE_15-03-23.csv
    - Colombia_geojson.json
  - src/
    - app.py
    - callbacks.py
    - carga_datos.py
    - estilos.py
    - layout.py 
  - utilitarios/
    - valida_geojson.py
    - xls_a_csv.py

## Visualizaciones  
El presente proyecto permitira análizar 7 gráficas referentes a la mortalidad en colombia para el 2019:  
   - mapa - muertes por departamento 
   - puntos - muertes por mes 
   - Barras - ciudades más violentas 
   - Torta - ciudades con menos número de muertes 
   - Tabla - Principales causas de muerte 
   - Histograma - muertes por rango de edad 
   - Barras apiladas - muertes por genero y departamento  

## Despliegue  
El despliegue de realizo a tráves de la paltaforma como servicio - Render, para lo cual se realizaron los pasos: 

- Validación de la estructura del proyecto 
- Validación de dependencias minimas en requirements.txt:  
dash==3.0.4  
pandas==2.2.3  
plotly==6.0.1  
gunicorn==20.1.0  
openpyxl==3.1.5
- Validación de configuraciones minimas del render.yaml  
services:
  - type: web  
  name: desplegar-dash-mortalidad  
  env: python  
  buildCommand: pip install -r requirements.txt  
  startCommand: gunicorn --chdir src app:server  
  plan: free 
- Creación  de web service en render.com
- Selección del repositorio 
- Inicio del despliegue 
- Validación de despliegue: service is alive
- Confirmación de la URL 




