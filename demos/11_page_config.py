import streamlit as st

# DEBE ser la primera llamada a Streamlit
st.set_page_config(
    page_title="Mi App",        # Título de la pestaña del navegador
    page_icon="🚀",             # Icono de la pestaña
    layout="wide",               # "centered" (default) o "wide"
    initial_sidebar_state="expanded",  # "auto", "expanded", "collapsed"
)

st.title("App con configuración personalizada")
st.write("Esta app usa `layout='wide'` para aprovechar todo el ancho de la pantalla.")

col1, col2 = st.columns(2)
with col1:
    st.header("Panel izquierdo")
    st.write("Más espacio disponible gracias al layout wide.")
with col2:
    st.header("Panel derecho")
    st.write("Ideal para dashboards y apps con mucho contenido.")
