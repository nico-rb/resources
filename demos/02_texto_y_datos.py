import streamlit as st
import pandas as pd

st.title("Mostrar texto y datos")

# --- Texto ---
st.header("Texto")
st.markdown("Puedes usar **negrita**, *cursiva* y `código inline`.")
st.code("""
def saludo(nombre):
    return f"Hola, {nombre}"
""", language="python")
st.latex(r"E = mc^2")

# --- Datos ---
st.header("Datos")

df = pd.DataFrame({
    "Ciudad": ["Madrid", "Barcelona", "Valencia", "Sevilla"],
    "Población (M)": [3.3, 1.6, 0.8, 0.7],
    "Comunidad": ["Madrid", "Cataluña", "C. Valenciana", "Andalucía"],
})

st.subheader("st.dataframe (interactiva)")
st.dataframe(df, use_container_width=True)

st.subheader("st.table (estática)")
st.table(df)

# --- Métricas ---
st.header("Métricas")
col1, col2, col3 = st.columns(3)
col1.metric("Temperatura", "22 °C", "+1.5 °C")
col2.metric("Humedad", "65%", "-3%")
col3.metric("Viento", "12 km/h", "0 km/h")

# --- JSON ---
st.header("JSON")
st.json({"nombre": "Streamlit", "version": "1.x", "lenguaje": "Python"})
