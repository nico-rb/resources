import streamlit as st

st.title("Layout en Streamlit")

# --- Sidebar ---
st.sidebar.header("Sidebar")
st.sidebar.write("El sidebar es ideal para controles y filtros.")
filtro = st.sidebar.selectbox("Filtrar por:", ["Todos", "Opción A", "Opción B"])
st.sidebar.write(f"Filtro seleccionado: **{filtro}**")

# --- Columnas ---
st.header("Columnas")
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Columna 1")
    st.write("Contenido de la primera columna.")
    st.metric("Ventas", "1,234", "+12%")

with col2:
    st.subheader("Columna 2")
    st.write("Contenido de la segunda columna.")
    st.metric("Usuarios", "567", "+5%")

with col3:
    st.subheader("Columna 3")
    st.write("Contenido de la tercera columna.")
    st.metric("Errores", "3", "-2")

# --- Tabs ---
st.header("Tabs (pestañas)")
tab1, tab2, tab3 = st.tabs(["Datos", "Gráfico", "Configuración"])

with tab1:
    st.write("Aquí irían los datos.")

with tab2:
    st.write("Aquí iría un gráfico.")

with tab3:
    st.write("Aquí irían opciones de configuración.")

# --- Expander ---
st.header("Expander")
with st.expander("Haz clic para ver más detalles"):
    st.write("Este contenido está oculto por defecto.")
    st.write("Es útil para información secundaria o avanzada.")
    st.code("print('Código dentro de un expander')")

# --- Container ---
st.header("Container")
with st.container(border=True):
    st.write("Este contenido está dentro de un container con borde.")
    st.write("Útil para agrupar elementos visualmente.")
