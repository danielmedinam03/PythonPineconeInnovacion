import streamlit as st
from dotenv import load_dotenv
import openai
import os
import app_pinecone
import boto3
import io
from PyPDF2 import PdfReader
import docx2txt as d2t_reader

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

# Configuración inicial
load_dotenv(".env")
openai.api_key = os.getenv("OPENAI_API_KEY")

# Example usage for reading from S3
bucket_name = 'soaint-repository'
aws_access_key_id = os.getenv("AWS_ACCESS_KEY")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
folder_name = "CV/"


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
    text = d2t_reader.process(io.BytesIO(archivo))
    return text


##Funcion para leer Fichero
def leer_pdf(archivo):
    texto = ""
    doc = PdfReader(io.BytesIO(archivo))
    for pagina in doc.pages:
        texto += pagina.extract_text()
    return texto


st.title('Módulo de Carga de Archivos')
st.markdown(
    'Se muestran los archivos listos para procesar:')
st.info(
    f"!!IMPORTANTE!!: Para poder analzar los CV, deberas cargar los archivos dentro de la siguiente ruta:\n "
    f"https://soaint-repository.s3.amazonaws.com",
    icon="👾",
)

response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_name)
files_s3_raw = response.get("Contents")
print(files_s3_raw)
files_s3 = []

for file in files_s3_raw:
    if file['Key'] != folder_name:
        files_s3.append(file['Key'])

if len(files_s3) <= 0:
    st.error(
        "Por el momento no contamos con archivos pendientes de procesar. Revise si la carpeta se encuentra vacía",
        icon="😞"
    )

else:
    for idx, file in enumerate(files_s3):
        st.write(f"Archivo {idx + 1}: {file.split('/', 1)[-1]}")

# for idx,archivo in enumerate(os.listdir(carpeta)):
# st.write(f"Archivo {idx+1}: {archivo}")

if st.button('Procesar Archivos'):
    with st.spinner("Cargando CVs... Esto puede tomar unos minutos. Por favor espere"):
        contenido_total = ""
        # Esto podría ser mejor manejado como un diccionario si quieres mantener un mapeo directo
        # entre el nombre del archivo y su contenido.
        nombres_archivos = []
        for archivo in files_s3:
            if archivo.endswith('.pdf') or archivo.endswith('.docx'):
                nombres_archivos.append(archivo)  # Guarda el nombre del archivo para uso posterior
                # ruta_completa = os.path.join(carpeta, archivo)
                obj = s3.get_object(Bucket=bucket_name, Key=archivo)
                body = obj['Body'].read()
                # Aquí agregas un separador único o algo que te permita dividir fácilmente luego
                contenido_total += f"----- Separador de CV: {archivo} -----\n"
                if archivo.endswith('.pdf'):
                    contenido_total += leer_pdf(body) + "\n"
                else:  # archivo.endswith('.docx')
                    contenido_total += leer_docx(body) + "\n"
        if contenido_total:
            # Suponiendo que consult_openai_personalizada ahora devuelve algo que puedes dividir
            # en secciones individuales por CV.
            response_personalizada = contenido_total
            # Asumiendo que response_personalizada es un texto donde cada CV está separado por un marcador único.
            cv_secciones = response_personalizada.split(
                "----- Separador de CV")  # Ajusta según sea necesario

            # --CREACION DEL INDICE no se va recrear todo--#
            # app_pinecone.create_index()
            list_text_resume = []
            for seccion in cv_secciones[1:]:  # [1:] para saltar el primer elemento si está vacío
                nombre_cv, contenido_cv = seccion.split("-----", 1)
                # Divide en nombre y contenido
                text_AF = contenido_cv.strip()
                formateo = consult_openai_personalizada(text_AF, informacion_recopilar)
                list_text_resume.append(formateo)

            app_pinecone.insert_records(list_text_resume)

        # st.session_state['records_inserted'] = True
    st.success("Los registros se han insertado con éxito.")

# if st.session_state.get('records_inserted', False):
# Código que se ejecuta si los registros se insertaron correctamente
# st.success("Los registros se han insertado con éxito.")
