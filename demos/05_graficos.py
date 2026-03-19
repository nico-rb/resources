import streamlit as st
import pandas as pd
import numpy as np

st.title("Gráficos en Streamlit")

# Generar datos de ejemplo
np.random.seed(42)
datos = pd.DataFrame(
    np.random.randn(50, 3),
    columns=["Serie A", "Serie B", "Serie C"],
).cumsum()

# --- Gráficos nativos de Streamlit ---
st.header("Gráficos nativos")

st.subheader("st.line_chart")
st.line_chart(datos)

st.subheader("st.area_chart")
st.area_chart(datos)

st.subheader("st.bar_chart")
st.bar_chart(datos.tail(10))

st.subheader("st.scatter_chart")
scatter_data = pd.DataFrame({
    "x": np.random.randn(100),
    "y": np.random.randn(100),
    "grupo": np.random.choice(["A", "B"], 100),
})
st.scatter_chart(scatter_data, x="x", y="y", color="grupo")

# --- Matplotlib ---
st.header("Matplotlib")
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.hist(np.random.randn(500), bins=30, edgecolor="black")
ax.set_title("Histograma con Matplotlib")
ax.set_xlabel("Valor")
ax.set_ylabel("Frecuencia")
st.pyplot(fig)

# --- Plotly (si está instalado) ---
st.header("Plotly")
try:
    import plotly.express as px

    df_plotly = px.data.gapminder().query("year == 2007")
    fig_plotly = px.scatter(
        df_plotly, x="gdpPercap", y="lifeExp",
        size="pop", color="continent",
        hover_name="country", log_x=True,
        title="Esperanza de vida vs PIB per cápita (2007)",
    )
    st.plotly_chart(fig_plotly, use_container_width=True)
except ImportError:
    st.info("Instala plotly para ver este gráfico: `pip install plotly`")
