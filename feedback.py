import streamlit as st
def mostrar_feedback():
    # Título de la vista de retroalimentación
    st.header("Load failed")

    # Utilizar Markdown para estilos adicionales
    st.markdown("#### Cuéntanos más:")

    # Crear una serie de botones para la retroalimentación del usuario
    feedback_options = [
        "Shouldn't have run code",
        "Couldn't handle my file",
        "Don't like the style",
        "Not factually correct",
        "Didn't fully follow instructions",
        "Más..."
    ]

    for option in feedback_options:
        st.button(option)

    # Agregar un icono de 'manita abajo' con componente HTML personalizado
    thumbs_down_icon = """
    <div style="font-size: 50px; color: grey;">
        <i class="fa fa-thumbs-down"></i>
    </div>
    """
    st.markdown(thumbs_down_icon, unsafe_allow_html=True)

    # Incluir FontAwesome para que los íconos se muestren
    st.markdown(
        """
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        """,
        unsafe_allow_html=True
    )

# Botón inicial que el usuario debe presionar para cargar la vista de retroalimentación
if st.button("Presióname"):
    mostrar_feedback()