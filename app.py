import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import numpy as np
from pathlib import Path

# --- Config ---
st.set_page_config(page_title="Monitor de Anomalías", layout="wide")
st.title("Monitor de Anomalías")

DATA_PATH = Path(__file__).parent / "data" / "private" / "dataset_sintetico.csv"

FEATURES = {
    "actividad": "Actividad (requests)",
    "http_4xx": "Errores HTTP 4xx",
    "http_5xx": "Errores HTTP 5xx",
    "sum_downloadTime": "Tiempo de descarga total (ms)",
    "avg_downloadTime": "Tiempo de descarga promedio (ms)",
}


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH, parse_dates=["timestamp_local"])
    return df


@st.cache_data
def generate_mock_alerts(df: pd.DataFrame) -> pd.DataFrame:
    """Genera alertas sintéticas basadas en percentiles altos de cada feature."""
    rng = np.random.default_rng(42)
    alerts = []

    for col in FEATURES:
        threshold = df[col].quantile(0.97)
        anomalous = df[df[col] > threshold].copy()
        sampled = anomalous.sample(n=min(len(anomalous), 30), random_state=42)

        for _, row in sampled.iterrows():
            alerts.append({
                "timestamp": row["timestamp_local"],
                "feature": FEATURES[col],
                "valor": round(row[col], 2),
                "threshold": round(threshold, 2),
                "severidad": rng.choice(["Alta", "Media", "Baja"], p=[0.5, 0.35, 0.15]),
            })

    alerts_df = pd.DataFrame(alerts).sort_values("timestamp", ascending=False).reset_index(drop=True)
    return alerts_df


@st.cache_data
def generate_mock_explainability() -> pd.DataFrame:
    """Genera valores SHAP sintéticos para simular explicabilidad."""
    rng = np.random.default_rng(123)
    shap_values = {
        "Feature": list(FEATURES.values()),
        "SHAP Value (media |valor|)": [
            round(v, 4) for v in sorted(rng.uniform(0.05, 0.45, size=len(FEATURES)), reverse=True)
        ],
    }
    return pd.DataFrame(shap_values)


# --- Load data ---
df = load_data()

# --- Sidebar filters ---
st.sidebar.header("Filtros")

date_range = st.sidebar.date_input(
    "Rango de fechas",
    value=(df["timestamp_local"].min().date(), df["timestamp_local"].max().date()),
    min_value=df["timestamp_local"].min().date(),
    max_value=df["timestamp_local"].max().date(),
)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
    mask = (df["timestamp_local"].dt.date >= start_date) & (df["timestamp_local"].dt.date <= end_date)
    df_filtered = df[mask]
else:
    df_filtered = df

selected_features = st.sidebar.multiselect(
    "Features a visualizar",
    options=list(FEATURES.keys()),
    default=list(FEATURES.keys()),
    format_func=lambda x: FEATURES[x],
)

aggregation = st.sidebar.selectbox(
    "Agregación temporal",
    options=["5min (raw)", "1h", "1d"],
    index=1,
)

# --- Aggregate ---
if aggregation == "1h":
    df_plot = df_filtered.set_index("timestamp_local").resample("1h").agg({
        "actividad": "sum",
        "http_4xx": "sum",
        "http_5xx": "sum",
        "sum_downloadTime": "sum",
        "avg_downloadTime": "mean",
    }).reset_index()
elif aggregation == "1d":
    df_plot = df_filtered.set_index("timestamp_local").resample("1D").agg({
        "actividad": "sum",
        "http_4xx": "sum",
        "http_5xx": "sum",
        "sum_downloadTime": "sum",
        "avg_downloadTime": "mean",
    }).reset_index()
else:
    df_plot = df_filtered.copy()


# =============================================================================
# SECTION 1: Gráficos de Features Principales
# =============================================================================
st.header("1. Gráficos de Features Principales")

for feature in selected_features:
    fig = px.line(
        df_plot,
        x="timestamp_local",
        y=feature,
        title=FEATURES[feature],
        labels={"timestamp_local": "Fecha", feature: FEATURES[feature]},
    )
    fig.update_layout(height=350, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)

# Correlation heatmap
if len(selected_features) > 1:
    st.subheader("Matriz de correlación")
    corr = df_filtered[selected_features].corr()
    fig_corr = px.imshow(
        corr,
        text_auto=".2f",
        x=[FEATURES[f] for f in selected_features],
        y=[FEATURES[f] for f in selected_features],
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1,
    )
    fig_corr.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig_corr, use_container_width=True)


# =============================================================================
# SECTION 2: Cuadro de Explicabilidad
# =============================================================================
st.header("2. Explicabilidad (mockup SHAP)")

st.caption("Valores SHAP sintéticos — se reemplazarán con valores reales tras el entrenamiento del modelo.")

explainability_df = generate_mock_explainability()

col1, col2 = st.columns(2)

with col1:
    fig_shap = px.bar(
        explainability_df,
        x="SHAP Value (media |valor|)",
        y="Feature",
        orientation="h",
        color="SHAP Value (media |valor|)",
        color_continuous_scale="Reds",
    )
    fig_shap.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=False,
        yaxis=dict(autorange="reversed"),
    )
    st.plotly_chart(fig_shap, use_container_width=True)

with col2:
    st.dataframe(
        explainability_df.style.bar(subset=["SHAP Value (media |valor|)"], color="#ff6b6b"),
        use_container_width=True,
        hide_index=True,
    )


# =============================================================================
# SECTION 3: Histórico de Alertas
# =============================================================================
st.header("3. Histórico de Alertas")

st.caption("Alertas sintéticas generadas a partir de percentil 97 — se reemplazarán con alertas del modelo.")

alerts_df = generate_mock_alerts(df)

# Filters for alerts
col_sev, col_feat = st.columns(2)
with col_sev:
    sev_filter = st.multiselect(
        "Filtrar por severidad",
        options=["Alta", "Media", "Baja"],
        default=["Alta", "Media", "Baja"],
    )
with col_feat:
    feat_filter = st.multiselect(
        "Filtrar por feature",
        options=list(FEATURES.values()),
        default=list(FEATURES.values()),
    )

alerts_filtered = alerts_df[
    (alerts_df["severidad"].isin(sev_filter)) & (alerts_df["feature"].isin(feat_filter))
]

# KPIs
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Total alertas", len(alerts_filtered))
kpi2.metric("Alertas Alta", len(alerts_filtered[alerts_filtered["severidad"] == "Alta"]))
kpi3.metric("Features afectadas", alerts_filtered["feature"].nunique())

# Color-coded dataframe
def color_severity(val):
    colors = {"Alta": "background-color: #ff4b4b33", "Media": "background-color: #ffa50033", "Baja": "background-color: #00cc6633"}
    return colors.get(val, "")

st.dataframe(
    alerts_filtered.style.map(color_severity, subset=["severidad"]),
    use_container_width=True,
    hide_index=True,
    height=400,
)

# Timeline chart of alerts
if not alerts_filtered.empty:
    st.subheader("Distribución temporal de alertas")
    alerts_by_day = alerts_filtered.copy()
    alerts_by_day["fecha"] = alerts_by_day["timestamp"].dt.date
    alerts_count = alerts_by_day.groupby(["fecha", "severidad"]).size().reset_index(name="count")

    fig_alerts = px.bar(
        alerts_count,
        x="fecha",
        y="count",
        color="severidad",
        color_discrete_map={"Alta": "#ff4b4b", "Media": "#ffa500", "Baja": "#00cc66"},
        labels={"fecha": "Fecha", "count": "Cantidad", "severidad": "Severidad"},
    )
    fig_alerts.update_layout(height=350, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig_alerts, use_container_width=True)
