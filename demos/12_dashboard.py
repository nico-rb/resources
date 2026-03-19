import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Mini Dashboard", page_icon="📊", layout="wide")

st.title("📊 Mini Dashboard de Ventas")

# --- Sidebar: filtros ---
st.sidebar.header("Filtros")
n_meses = st.sidebar.slider("Meses a mostrar", 3, 24, 12)
categorias = st.sidebar.multiselect(
    "Categorías",
    ["Electrónica", "Ropa", "Alimentación", "Hogar"],
    default=["Electrónica", "Ropa", "Alimentación", "Hogar"],
)

# --- Generar datos ---
np.random.seed(42)
fechas = pd.date_range("2024-01-01", periods=n_meses, freq="ME")
datos = pd.DataFrame({
    "Fecha": np.tile(fechas, len(categorias)),
    "Categoría": np.repeat(categorias, n_meses),
    "Ventas": np.random.randint(5000, 50000, n_meses * len(categorias)),
    "Unidades": np.random.randint(100, 2000, n_meses * len(categorias)),
})

# --- Métricas ---
total_ventas = datos["Ventas"].sum()
total_unidades = datos["Unidades"].sum()
ticket_medio = total_ventas / total_unidades if total_unidades > 0 else 0

col1, col2, col3 = st.columns(3)
col1.metric("Ventas totales", f"{total_ventas:,.0f} €")
col2.metric("Unidades vendidas", f"{total_unidades:,}")
col3.metric("Ticket medio", f"{ticket_medio:.2f} €")

st.divider()

# --- Gráficos ---
col_izq, col_der = st.columns(2)

with col_izq:
    st.subheader("Evolución de ventas")
    pivot = datos.pivot_table(index="Fecha", columns="Categoría", values="Ventas")
    st.line_chart(pivot)

with col_der:
    st.subheader("Ventas por categoría")
    resumen = datos.groupby("Categoría")["Ventas"].sum().reset_index()
    st.bar_chart(resumen.set_index("Categoría"))

# --- Tabla de datos ---
with st.expander("Ver datos en detalle"):
    st.dataframe(datos, use_container_width=True)
