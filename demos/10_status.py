import streamlit as st
import time

st.title("Mensajes de estado y progreso")

# Mensajes estáticos
st.success("Operación completada correctamente.")
st.error("Ha ocurrido un error.")
st.warning("Cuidado, esto podría fallar.")
st.info("Esto es un mensaje informativo.")

# Barra de progreso
st.header("Barra de progreso")
if st.button("Iniciar proceso"):
    barra = st.progress(0, text="Procesando...")
    for i in range(100):
        time.sleep(0.02)
        barra.progress(i + 1, text=f"Procesando... {i + 1}%")
    st.success("¡Proceso completado!")

# Spinner
st.header("Spinner")
if st.button("Cargar datos"):
    with st.spinner("Cargando datos..."):
        time.sleep(2)
    st.success("Datos cargados.")

# Toast
st.header("Toast")
if st.button("Mostrar toast"):
    st.toast("¡Notificación!", icon="🎉")
