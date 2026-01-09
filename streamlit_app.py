
# ==========================
# 📑 TAB: Hallazgos del Excel (Reglas DQ Consolidadas)
# ==========================

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.markdown('<p class="subtitle">📑 Hallazgos del Excel — Reglas Consolidadas</p>', unsafe_allow_html=True)

# --- Carga del Excel de reglas
df_rules = pd.read_excel("dataplex_dq_rules_consolidado.xlsx", engine="openpyxl")

# --- Cálculos base
total_rules = len(df_rules)
dims = df_rules["dimension"].value_counts()
perc = (dims / total_rules * 100).round(2)

summary_dim = pd.DataFrame({
    "Dimensión": dims.index,
    "Reglas": dims.values,
    "Porcentaje": perc.values
})

# --- KPIs estilo Bunge
st.write("### 🔍 Resumen general")
col_a, col_b, col_c = st.columns(3)

col_a.metric(
    label="📦 Total reglas",
    value=f"{total_rules:,}",
    delta=""
)
col_b.metric(
    label="📘 Completitud (%)",
    value=f"{perc.get('COMPLETENESS', 0)}%",
    delta=""
)
col_c.metric(
    label="📙 Validez (%)",
    value=f"{perc.get('VALIDITY', 0)}%",
    delta=""
)

# --- Tabla resumen
st.write("### 📊 Reglas por dimensión")
st.dataframe(summary_dim, use_container_width=True)

# --- Gráfico de barras
st.write("### 📈 Distribución de reglas por dimensión")
fig_dim = px.bar(
    summary_dim,
    x="Dimensión",
    y="Reglas",
    color="Dimensión",
    text="Reglas",
    title="Distribución de reglas por Dimensión",
    color_discrete_sequence=["#004C97", "#003366", "#0073CF"]
)
fig_dim.update_layout(margin=dict(l=10, r=10, t=50, b=10))
st.plotly_chart(fig_dim, use_container_width=True)

# --- Radar
st.write("### 🧭 Radar porcentual por dimensión")
fig_radar = go.Figure()
fig_radar.add_trace(go.Scatterpolar(
    r=summary_dim["Porcentaje"],
    theta=summary_dim["Dimensión"],
    fill='toself',
    name="Porcentaje",
    line_color="#004C97"
))
fig_radar.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
    showlegend=False,
    margin=dict(l=10, r=10, t=50, b=10),
    title="Porcentaje de reglas por dimensión"
)
st.plotly_chart(fig_radar, use_container_width=True)

# --- Comentarios ejecutivos
st.write("### 📝 Conclusiones clave")
st.markdown("""
- **Completitud** es la dimensión más fuerte (45.61%), lo que refleja un foco claro en asegurar presencia de valores críticos.  
- **Validez** también tiene un peso muy alto (42.08%), mostrando fuerte enfoque en catálogos, dominios y rangos.  
- **Unicidad** presenta valores menores (12.31%), lo que sugiere:  
  - Muchos intentos rechazados en las recomendaciones automáticas.  
  - Potencial oportunidad para revisar PKs y CDEs críticos.  
""")

st.markdown('<footer>© 2026 Bunge Global SA — Todos los derechos reservados</footer>', unsafe_allow_html=True)
