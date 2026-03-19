import streamlit as st
import pandas as pd
import time

st.title("Caché en Streamlit")


@st.cache_data
def cargar_datos_lento():
    """Simula una carga de datos costosa (solo se ejecuta una vez)."""
    time.sleep(3)  # Simula latencia
    return pd.DataFrame({
        "x": range(100),
        "y": [i ** 2 for i in range(100)],
    })


st.write("La primera vez tardará 3 segundos. Después será instantáneo.")

with st.spinner("Cargando datos..."):
    df = cargar_datos_lento()

st.success("¡Datos cargados!")
st.line_chart(df.set_index("x"))

# Parámetro ttl (time to live) para expirar la caché
st.header("Caché con TTL")
st.code("""
@st.cache_data(ttl=600)  # Expira después de 10 minutos
def obtener_datos_api():
    return requests.get("https://api.ejemplo.com/datos").json()
""")

# Limpiar caché manualmente
if st.button("Limpiar caché"):
    st.cache_data.clear()
    st.success("Caché limpiada. La próxima carga tardará 3s de nuevo.")
