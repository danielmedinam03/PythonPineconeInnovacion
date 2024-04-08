import streamlit as st
from PIL import Image

# Streamlit de presentación, con titulo y resumen de proyecto

st.set_page_config(
    page_title="Aplicacion de RRHH",
    page_icon=":chart_with_upwards_trend:"
)

st.title("Análisis de Perfiles")

st.write("""
Este proyecto MVP tiene como objetivo obtener a los candidatos ideales de SOAINT con respecto a un requerimiento 
por parte del equipo de de Preventa y/o Operaciones.\n
Esto permitirá al  equipo de RRHH identificar aquellos perfiles requeridos de forma inmediata 
para dar soporte tanto a las ventas como la operativa del negocio.\n
Se realizo previamente la carga de la data de las hojas de vida de los candidatos que sirven como data para el análisis. \n
A continuación, se explica brevemente cada uno de los módulos del sistema
""")

image = Image.open("images/rrhh.jpg")
st.image(image, use_column_width=True)

st.header("Módulos del Sistema")

st.write("""
- **Wiki:** En esta sección se explica todo lo referente a la aplicación.

- **Análisis de Perfil:** En esta sección ingrese su documento de requerimiento, procese el archivo para tener un perfil más completo, 
luego solicite los candidatos que se ajusten a dichos requerimientos.
Por ultimo dejenos su feedback sobre el resultados obtenidos.

- **Carga de Archivos:** En esta sección podrá cargar hojas de vida nuevas para el procesamiento de perfiles.
""")
