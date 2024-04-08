import streamlit as st
import fitz  # PyMuPDF
from dotenv import load_dotenv
import openai
import os
import docx  # Importa el módulo completo en lugar de solo 'Document'
import app_pinecone
import app_db_mongo

Mensaje_feedback=""

informacion_recopilar = '''
Datos Personales
Identificación:
Datos que permiten identificar a un postulante.
Fecha Modificación: Fecha en que se modifica el registo.
Pais: País donde vive el postulante.
Nombres: Uno o mas nombres de pila del postulante, puede incluir Abreviaciones.
Apellidos: Principalmente el Apellido Paterno, puede incluir el apellido Materno
Tipo Identificación: Identificación del estado, depende del país emisor, puede ser [
    "rut",
    "dni",
    "cedula",
    "Pasaporte",
    "Número de seguridad Social",
    "Número Licencia de Conducir"
]
Identificación: Número de identificación, serial de identificación, puede contener números, letras y dígitos de verificación.
Edad: Edad del Postulante al momento de guardar el registro, puede ser calculada a partir de la fecha de nacimiento.

Contacto
Datos que permiten contactar al postulante.
Fecha Modificación: Fecha en que se modifica el registo.
Ciudad: Ciudad donde vive el postulante.
Comuna: Comuna donde vive el postulante
Dirección: Dirección donde vive el postulante
Mail: Mail personal del postulante, puede ser un mail corporativo.
Telefono: Puede ser el Celular o teléfono fijo.

Redes
Datos relativos a redes sociales, comunidades en líneas, blogs en línea, Páginas personales, Portafolios personales.
Fecha Modificación: : Fecha en que se modifica el registo.
tipo red: Puede incluir [
    "linkedin",
    "Facebook",
    "gitlab",
    "docker"
]
enlace link usuario: Enlace o link a la red social o nombre de usuario.

Perfil Profesional
Datos referentes a los estudios realizados por el postulante o a su experiencia empírica.
Perfil de estudios: Estudios realizados por el postulante.
Fecha Modificación: Fecha en que se modifica el registo.
 Nivel más alto: Nivel de estudio mas alto alcanzado por el postulante en orden de importancia son [
    "Post Doctorado",
    "Doctorado",
    "Maestría",
    "Carrera Universitaria Completa",
    "Carrera Universitaria Inconpleta",
    "Carrera Técnica Completa",
    "Carrera Técnica Inconpleta",
    "Autodidacta",
    "Estudiante"
]
 Título: Título obtenido, nombre del curso, Nombre de la carrera, Nombre de la especialización.
 Año de finalización: Año en que termina el curso.
 Años de experiencia: Años en que ha tenido experiencia en campo después de obter el Título a partir del año de finalización

Auto percepción profesional
Como se presenta o persibe el postulante de acuerdo a su propia descripción. Puede ser el cargo al que postula, Cargo al que es recomendado, cargo más alto alcanzado según su experiencia profesional.
Fecha Modificación: Fecha en que se modifica el registo.

Objetivos: Texto escrito por el aspirante donde declara sus objetivos, metas a largo y corto plazo, como se visualiza en la empresa, que aportará a la empresa, que desea hacer en el futuro.
Habilidades: rasgos interpersonales indicados por el postulante que ha desarrollado con el tiempo basado en su experiencia profesional, pueden ser comunicación acertiva, liderazgo, comunicación y escucha activa, planificación y Gestión del tiempo, flexibilidad, negociación.
Intereses: Intereses profesionales del postulante.

Conocimientos
Conocimientos específicos del postulante para su desarrollo profesional.
Fecha Modificación Fecha en que se modifica el registo.
Tecnologías": """Herramientas": """Certificado": """Años de experiencia": """Clasificación de experiencia": ""

Perfil Psicológico
Datos de la conducta del postulante o que permitan determinar su empleabilidad segura en la sociedad.
Fecha Modificación: Fecha en que se modifica el registo.
Deportes: Deportes que practica, o clubes deportivos a los que pertenece.
Aficiones pasatiempos: Aficciones pasatiempos hobbies.
Familia: Actividades que realiza el postulante en familia, datos sobre su familia o su iteración con esta, como se describe el postulante con respecto a su familia, lo que comenta el postulante sobre la familia.
Sociedad: Actividades que realiza el postulante en la sociedad diferente a deportes, como conciertos, comidas, actividades al aire libre,  actividades religiosas, actividads altruistas, clubes sociales.

Competencias y Habilidades
Competencias y habilidades blandas.
Fecha Modificación: Fecha en que se modifica el registo.
Habilidades blandas: habilidades descritas en las funciones o experiencia profesional pueden ser [
    "Adaptabilidad",
    "Pensamiento Crítico",
    "Pensamiento Creativo",
    "Trabajo en Equipo",
    "Resolución de Problemas",
    "Etica Laboral",
    "Liderazgo",
    "Gestión del tiempo"
]

Idiomas
Conocimientos de idiomas del postulante
Fecha Modificación: Fecha en que se modifica el registo.
Nivel: medición del grado de compresión del idioma del postulante puede ser  [
    "Nativo",
    "Avanzado",
    "Medio",
    "Básico"
]

Experiencia
Experiencia profesional del postulante
Fecha Modificación: Fecha en que se modifica el registo.
Administración: Tipo de empresa según su administración puede ser [
    "Privado",
    "Público",
    "Mixto"
]
Sector: Clasificación de la empresa según su actividad económica Sector primario: Empresas dedicadas a extraer y aprovechas materias primas Ejemplo agricultura, ganadería, pesca, minería, caza, recursos forestales.
Sector secundario: Empresas dedicadas a la manipulación de los recursos naturales, transformación bienes en tros más útiles Ejemplo industria, contrucción, fábricas
Sector terciario: Empresas dedicadas a prestar servicios Ejemplo: Telefonía, comercio, transporte y comunicaciones
Sector cuaternario: Empresas dedicadas a investigación y tecnología
Sector quinario: Empresas dedicadas a  educación salud y cultura
Nombre Empresa:Nombre de la empresa en que laboró el postulante
Cargo: último cargo que desempeñó el postulante.
Principales Funciones: Principales funcionaes realizadas por el postulante
Meses ejerciendo: Cantidad de meses que postulante trabajó en la emrpesa
Cantidad de personas a cargo: cantidad de personas bajo el mando o administración del postulante.



Proyectos
Proyectos en los que ha participado el postulante
Fecha Modificación Fecha en que se modifica el registo.
Tipo de proyecto: Tipo o Nombre del proyecto en el que participó.
 Jefe de proyecto: Nombre del jefe del proyecto o encargado del proyecto o jefe inmediato.
Facturable: Si el proyecto fué facturable o no [
    "Si",
    "No"
]
Cargo en el proyecto: Cargo del postulante en el proyecto puede ser [
    "Implementador",
    "Analista de Mesa de Servicio",
    "Consultor Técnico",
    "Implementador",
    "Lider Técnico Arquitecto de Soluciones"
]
Fecha Inicio: Fecha en que inicia el proyecto
Fecha Finalización: Fecha en que finaliza el proyecto

Referencias
Recomendaciones de compañeros, familiares, exjefes o personas a cargo.
Fecha Modificación Fecha en que se modifica el registo.
Nombre quien refiere: Nombre de la persona que recomienda o refiere.
Mail quien refiere: Mail de la persona que recomienda o refiere.
 Cargo quien refiere: Cargo de la persona que recomienda o refiere.
 Cargo al que aspira: Cargo al que se postula
 Fecha de referencia: Fecha en que se realiza la recomendación
'''

# Seteo de Ruta completa
directorio_actual = os.getcwd()
dir_F = f'{directorio_actual}/CV'
carpeta = dir_F
# print("El directorio actual es:", directorio_actual)
# Asegúrate de que la ruta sea absoluta si la carpeta no está en el mismo directorio que tu script de Streamlit

# Configuración inicial
load_dotenv(".env")
openai.api_key = os.getenv("OPENAI_API_KEY")

# Variable globales
contenido_total = ""  # Variable para acumular el contenido de todos los archivos
contenido_perfiles = ""
archivos_subidos = ""
prompt_personalizado = ""
promp_PP = ""


# Funciones de lectura adaptadas

##Cargar A Embeding
def embedding_text(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-3-small"
    )

    print(response.data[0].embedding)
    return response.data[0].embedding


def consult_openai(text):
    prompt = (
        f"puedes enlistar los perfiles que se requieren por cubrir junto con la tecnologia:  \n  --Inicio Documento -- \n {text} \n  --Fin Documento -- \n")
    prompt = prompt

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user",
             "content": f"{prompt}"}
        ],
        max_tokens=1000,
        temperature=0.7,
    )

    return response.choices[0].message.content


# ----------Funciones de lectura de documentos----

def consult_openai_personalizada(text, plantilla):
    promp_PP = 'Del siguiente CV, identifica y  formatea la salida a la plantilla que te voy a compartir,en cuanto no encuentres algún elemento , coloca el sig texto "N/A":'
    promp_p = (
        f"{promp_PP} : \n--Inicio CV-- \n{text} \n--Fin CV-- \n \n--Inicio Plantilla--\n {plantilla} \n --Fin Plantilla--\n")
    response_personalizada = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user",
             "content": f"{promp_p}"}
        ],
        max_tokens=1000,
        temperature=0.7,
    )

    return response_personalizada.choices[0].message.content


def leer_docx(archivo):
    doc = docx.Document(archivo)
    texto_completo = [para.text for para in doc.paragraphs]
    return '\n'.join(texto_completo)


def leer_pdf_con_fitz(archivo):
    doc = fitz.open(stream=archivo.read(), filetype="pdf")
    texto_completo = ""
    for pagina in doc:
        texto_completo += pagina.get_text()
    return texto_completo


##Funcion para leer Fichero
def leer_pdf(archivo):
    texto = ""
    with fitz.open(archivo) as doc:
        for pagina in doc:
            texto += pagina.get_text()
    return texto


##Funcion para crear el vector
def embedding_text(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-3-small"
    )

    return response.data[0].embedding


# --------------------------------------


# Título de la aplicación y descripción
st.title('Módulo de Gestión de Perfiles')
st.markdown(
    'Ingresa a continuacion el Requerimiento de Perfil')
archivos_subidos_perfil = st.file_uploader("Carga el Documento", type=[
    'pdf', 'docx'], accept_multiple_files=True)

if 'bandera_text' not in st.session_state:
    st.session_state['bandera_text'] = ""

if archivos_subidos_perfil:
    for archivo_perfil in archivos_subidos_perfil:
        if archivo_perfil.type == "application/pdf":
            texto_perfil = leer_pdf_con_fitz(archivo_perfil)
        elif archivo_perfil.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            texto_perfil = leer_docx(archivo_perfil)
        else:
            texto_perfil = "Formato de archivo no soportado."

        # Agregar el contenido del perfil a la variable acumulativa
        contenido_perfiles += f"----- Contenido de {
        archivo_perfil.name} -----\n{texto_perfil}\n\n"
        # Mostrar los contenidos de los perfiles si se ha cargado algo
        response_perfil = ""




        if contenido_perfiles:
            st.markdown('Da click en procesar para poder extraer las keys del documento de requerimiento')
            if st.button('Procesar'):
                with st.spinner('Cargando Perfil...Por favor espere 😊'):
                    response_perfil = consult_openai(contenido_perfiles)
                    # Generar un nuevo documento, con la informacion enriquecida  y que descargue el documento por le navegador y que complemente los datos de perfiles con tecnolgia
                    text_PERFIL = st.text_area("Contenido de todos los perfiles:",
                                               value=response_perfil, height=400)
                    st.session_state['bandera_text'] = response_perfil
                    carpeta = dir_F
                    st.session_state['records_inserted'] = True

            ##SE AGREGAN LOS BOTONES

        formato_respuesta = """
        Candidato:
        -Nombre:
        -Contacto: 

        -Tecnologías Clave y Habilidades Técnicas que maneja:
        -Experiencia en el cargo o cargos que se asemejen:
        -Porcentaje de Afinidad con el Perfil:
        """
        if st.session_state.get('records_inserted', False):
            if st.button("Busca los perfiles que mas se asimilen"):
                with st.spinner('Buscando similitudes..Por favor, espere 😊'):
                    print('---inicia response perfil---')
                    print(st.session_state['bandera_text'])

                    format_question_profile = (
                        f"Puedes indicarme todos los posibles candidatos que mas se asimilan al siguiente perfil revisa que tambien cumplan las tecnologias necesarias, además define que tipo de profesional es Junior, SemiSenior, Senior, también ten en cuenta que el porcentaje de afinidad debe ser numerico, finalmente ordena la respuesta de acuerdo al porcentaje de afinidad de manera descendente :\n --Inicio formato de respuesta-- \n {formato_respuesta} \n --fin de formato de respuesta-- \n\n--Inicio Perfil--\n{st.session_state['bandera_text']}\n --Final Perfil--, no consideres en la respuesta las palabras 'Inicio formato' y 'Fin de formato' ")

                    print(format_question_profile)
                    print('---Fin response perfil---')

                    resultado_question = app_pinecone.retrieve_answer(format_question_profile,4)
                    print(f"estoy regresando de app_pinecone:\n{resultado_question}")
                    bandera_question=st.text_area("Resultado de busqueda:",
                                               value=resultado_question, height=400)

                    # SE AGREGAN LOS BOTONES DE FEEDBACK CON ÍCONOS
                    # Incluir FontAwesome para que los íconos se muestren
                    if bandera_question:
                        # Inicializar una variable de sesión para guardar el estado del botón (happy, neutral, sad)

                        # Asegurar que button_state exista en st.session_state
                        if 'button_state' not in st.session_state:
                            st.session_state.button_state = None
                        if 'mensaje_feedback' not in st.session_state:
                            st.session_state.mensaje_feedback = ""

                        # Definición de la función para cambiar el estado y mostrar mensaje
                        def set_button_state(state):
                            st.session_state.button_state = state


                        def set_button_state(state):
                            st.session_state.button_state = state

                        # Usar st.columns para crear tres columnas y botones en cada una
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.button("😊", on_click=set_button_state, args=('happy',))
                        with col2:
                            st.button("😐", on_click=set_button_state, args=('neutral',))
                        with col3:
                            st.button("☹️", on_click=set_button_state, args=('sad',))

                        # Pedir feedback
                        st.markdown("¿Podrías dejarnos tu feedback para mejorar?")

                        # Espacio para ingresar comentarios
                        comentarios_ingresados = st.text_area("Escribe tus comentarios aquí:")
                        # Luego de definir los botones y manejar el estado del botón con set_button_state:
                        if st.session_state.button_state == 'happy':
                            print("Calificacion buena")
                            app_db_mongo.save_feedback({"calificacion": 5,
                                                        "comentarios": comentarios_ingresados,
                                                        "pregunta": format_question_profile,
                                                        "respuesta": resultado_question
                                                        })
                            st.success("¡Gracias por tu feedback positivo!")
                            st.session_state.mensaje_feedback = "Feedback positivo recibido."
                        elif st.session_state.button_state == 'neutral':
                            print("Calificacion regular")
                            app_db_mongo.save_feedback({"calificacion": 3,
                                                        "comentarios": comentarios_ingresados,
                                                        "pregunta": format_question_profile,
                                                        "respuesta": resultado_question
                                                        })
                            st.warning("Gracias por tu feedback. ¡Trabajaremos en mejorar!")
                            st.session_state.mensaje_feedback = "Feedback neutral recibido."
                        elif st.session_state.button_state == 'sad':
                            print("Calificacion mala")
                            app_db_mongo.save_feedback({"calificacion": 1,
                                                        "comentarios": comentarios_ingresados,
                                                        "pregunta": format_question_profile,
                                                        "respuesta": resultado_question
                                                        })
                            st.error("Lo sentimos. Tomaremos tu feedback para mejorar.")
                            st.session_state.mensaje_feedback = "Feedback negativo recibido."



                        st.write(f"Mensaje de feedback: {st.session_state.mensaje_feedback}")