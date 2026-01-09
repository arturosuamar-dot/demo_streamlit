
import streamlit as st
import yaml
import random
from datetime import datetime, date
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import re
from pathlib import Path
from pandas.api.types import (
    is_datetime64_any_dtype,
    is_object_dtype,
    is_numeric_dtype
)

# ==========================
# Configuración general
# ==========================
st.set_page_config(page_title="DQaaS - Bunge Global SA", page_icon="🌐", layout="wide")

if "perfilado_iniciado" not in st.session_state:
    st.session_state.perfilado_iniciado = False

# ==========================
# CSS inicial (Portada)
# ==========================
if not st.session_state.perfilado_iniciado:
    st.markdown("""
        <style>
        .main .block-container {
            max-width: 980px;
            margin-left: auto;
            margin-right: auto;
            padding-top: 6vh;
        }
        html, body, .stApp {
            font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
        }
        div.stButton > button {
            width: 340px;
            height: 56px;
            font-size: 20px;
            font-weight: 600;
            background-color: #004C97;
            color: white;
            border-radius: 10px;
            border: none;
            transition: 0.25s;
        }
        div.stButton > button:hover {
            background-color: #003366;
            transform: translateY(-1px);
        }
        footer { text-align: center; color: #6b6b6b; margin-top: 48px; }
        </style>
    """, unsafe_allow_html=True)

# ==========================
# PORTADA
# ==========================
if not st.session_state.perfilado_iniciado:

    st.markdown("""
        <div style="text-align: center;">
            <img src="https://delivery.bunge.com/-/jssmedia/Feature/Components/Basic/Icons/NewLogo.ashx?iar=0&hash=F544E33B7C336344D37599CBB3053C28"
                 style="width:180px; margin-bottom:18px;" />
            <h1 style="color:#004C97; font-size:42px; font-weight:800;">
                DQaaS - Data Quality as a Service
            </h1>
            <p style="color:#003366; font-size:20px; font-weight:600;">
                Bunge Global SA - Viterra Data Products Squad Extension
            </p>
        </div>
    """, unsafe_allow_html=True)

    col_btn = st.columns([1.2,1,1.2])
    with col_btn[1]:
        if st.button("🚀 Iniciar Perfilado de Datos", key="start", use_container_width=True):
            st.session_state.perfilado_iniciado = True
            st.rerun()

    st.markdown("<footer>© 2025 Bunge Global SA - Todos los derechos reservados</footer>", unsafe_allow_html=True)


# ==========================
# APP PRICIPAL
# ==========================
else:

    # ==========================
    # CSS interno completo
    # ==========================
    st.markdown("""
        <style>
        .main .block-container {
            max-width: 1800px;
            margin-left: auto;
            margin-right: auto;
        }
        @media (min-width: 1800px) {
            .main .block-container {
                max-width: 96vw;
            }
        }
        .stTabs [data-baseweb="tab"] {
            padding: 12px 18px;
            font-size: 18px;
            white-space: nowrap;
        }
        html, body, .stApp {
            font-family: "Segoe UI", "Segoe UI Emoji", "Apple Color Emoji", "Noto Color Emoji",
                          "Helvetica Neue", Arial, sans-serif !important;
        }
        div.stButton > button {
            width: 420px;
            height: 64px;
            font-size: 24px;
            font-weight: bold;
            background-color: #004C97;
            color: white;
            border-radius: 10px;
            border: none;
        }
        div.stButton > button:hover {
            background-color: #003366;
            transform: scale(1.05);
        }
        .subtitle {
            font-size: 24px;
            font-weight: bold;
            color: #004C97;
            margin-bottom: -10px;
        }
        footer { text-align: center; color: #6b6b6b; margin-top: 40px; }
        </style>
    """, unsafe_allow_html=True)

    # ==========================
    # Encabezado
    # ==========================
    st.markdown("""
        <div style="text-align: center; margin-bottom: 30px;">
            <img src="https://delivery.bunge.com/-/jssmedia/Feature/Components/Basic/Icons/NewLogo.ashx?iar=0&hash=F544E33B7C336344D37599CBB3053C28"
                 style="width:180px; margin-bottom:20px;" />
            <h1 style="color:#004C97; font-size:48px; font-weight:bold;">DQaaS - Data Quality as a Service</h1>
            <p style="color:#003366; font-size:22px; font-weight:bold;">
                Bunge Global SA - Viterra Data Products Squad Extension
            </p>
        </div>
    """, unsafe_allow_html=True)


    # ==========================
    # CARGA DE CSV LOCAL
    # ==========================
    DATASETS = {
        "Dataproduct_Prueba": "./datos_prueba.csv",
    }

    st.markdown('<p class="subtitle">📂 Seleccione el dataproduct:</p>', unsafe_allow_html=True)

    dataproduct_visible = st.selectbox("", list(DATASETS.keys()))
    path_csv = DATASETS[dataproduct_visible]

    # ==========================
    # FUNCIONES AUXILIARES + PERFILADO
    # ==========================
    @st.cache_data(show_spinner=False)
    def load_csv_local(path_str: str) -> pd.DataFrame:
        p = Path(path_str)
        if not p.exists():
            raise FileNotFoundError(f"No se encuentra: {p.resolve()}")
        try:
            return pd.read_csv(p)
        except UnicodeDecodeError:
            return pd.read_csv(p, encoding="latin-1")


    def infer_types(df: pd.DataFrame):
        for col in df.columns:
            if is_object_dtype(df[col]):
                df[col] = df[col].astype(str).str.strip()

        def maybe_to_dt(series: pd.Series) -> bool:
            try:
                p = pd.to_datetime(series, errors="coerce")
                return p.notna().mean() >= 0.6
            except:
                return False

        for col in df.columns:
            if is_object_dtype(df[col]) and maybe_to_dt(df[col]):
                df[col] = pd.to_datetime(df[col], errors="coerce")

        numeric_cols = [c for c in df.columns if is_numeric_dtype(df[c])]
        datetime_cols = [c for c in df.columns if is_datetime64_any_dtype(df[c])]
        categorical_cols = [
            c for c in df.columns if (df[c].dtype.name in ("object", "category"))
        ]
        return df, numeric_cols, datetime_cols, categorical_cols


    def derive_default_keys(df):
        id_like = [c for c in df.columns if re.search(r"\bid\b", c, re.IGNORECASE)]
        if id_like:
            return id_like
        nums = [c for c in df.columns if is_numeric_dtype(df[c])]
        if nums:
            return [nums[0]]
        return [df.columns[0]]


    # ==========================
    # CARGA + SEGMENTACIÓN + REGLAS
    # ==========================
    df = load_csv_local(path_csv)
    df, numeric_cols, datetime_cols, categorical_cols = infer_types(df)

    # Filtro inicial
    default_filter_col = (
        "Country"
        if "Country" in df.columns
        else (categorical_cols[0] if categorical_cols else df.columns[0])
    )

    st.markdown('<p class="subtitle">🎯 Segmentación</p>', unsafe_allow_html=True)

    colf1, colf2 = st.columns([1,2])
    with colf1:
        seg_col = st.selectbox("Campo de filtro", df.columns.tolist(), index=df.columns.tolist().index(default_filter_col))

    with colf2:
        posibles = sorted(df[seg_col].dropna().unique().tolist())
        seg_vals = st.multiselect(f"Valores para {seg_col}", posibles, default=[])

    df_current = df[df[seg_col].isin(seg_vals)] if seg_vals else df

    df_current, num_cur, dt_cur, cat_cur = infer_types(df_current)
    key_cols_cur = derive_default_keys(df_current)

    # ---- Construcción de reglas & métricas
    P_LOW_DEFAULT = 5
    P_HIGH_DEFAULT = 95
    MAX_CAT_DEFAULT = 20
    ALLOW_FUTURE_DEFAULT = False

    # (Tu función "make_rules_and_metrics" completa se mantiene igual)
    # Por brevedad la omito aquí, pero debe ir ENTERA donde la tengas definida.


    # ==========================
    # GENERACIÓN DE REGLAS (Usar tu propia función)
    # ==========================

    reglas_cur, metricas_cur = make_rules_and_metrics(
        df_current,
        num_cur,
        dt_cur,
        cat_cur,
        key_cols_cur,
        P_LOW_DEFAULT,
        P_HIGH_DEFAULT,
        MAX_CAT_DEFAULT,
        ALLOW_FUTURE_DEFAULT
    )

    if seg_vals:
        reglas_cur.insert(0, {
            "name": f"segment_filter_{seg_col}",
            "description": f"Segmento: {seg_col} ∈ {seg_vals}",
            "condition": f"{seg_col} IN {seg_vals}",
            "dimension": "Contexto"
        })

    umbral = 90

    # ==========================
    # TABS PRINCIPALES
    # ==========================
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📋 Reglas",
        "📊 Métricas",
        "📈 Gráficos",
        "⬇️ Descargar YAML",
        "📂 Vista de datos",
        "📑 Hallazgos Excel"
    ])


    # ==========================
    # TAB 1 — Reglas
    # ==========================
    with tab1:
        st.markdown('<p class="subtitle">📋 Reglas</p>', unsafe_allow_html=True)
        st.table(reglas_cur)

    # ==========================
    # TAB 2 — Métricas
    # ==========================
    with tab2:
        st.markdown('<p class="subtitle">📊 Métricas</p>', unsafe_allow_html=True)
        cols = st.columns(len(metricas_cur))
        for i,(k,v) in enumerate(metricas_cur.items()):
            estado = "✅" if v >= umbral else "⚠️"
            cols[i].metric(k, f"{v}% {estado}")

    # ==========================
    # TAB 3 — Gráficos
    # ==========================
    with tab3:
        st.markdown('<p class="subtitle">📈 Gráficos</p>', unsafe_allow_html=True)

        fig_bar = px.bar(
            x=list(metricas_cur.keys()), y=list(metricas_cur.values()),
            color=list(metricas_cur.keys()),
            title=f"Métricas — {dataproduct_visible}",
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=list(metricas_cur.values()),
            theta=list(metricas_cur.keys()),
            fill='toself'
        ))
        st.plotly_chart(fig_radar, use_container_width=True)

    # ==========================
    # TAB 4 — Exportar YAML
    # ==========================
    with tab4:

        yaml_data = {
            "rules": reglas_cur,
            "metrics": metricas_cur,
            "generated_at": datetime.now().isoformat(),
            "segment": seg_vals if seg_vals else "Global"
        }

        yaml_str = yaml.dump(yaml_data, sort_keys=False, allow_unicode=True)

        st.download_button(
            label="⬇️ Descargar YAML",
            data=yaml_str,
            file_name="perfil_calidad.yaml",
            mime="text/yaml"
        )

    # ==========================
    # TAB 5 — Vista de datos
    # ==========================
    with tab5:
        st.markdown('<p class="subtitle">📂 Vista de datos</p>', unsafe_allow_html=True)
        st.dataframe(df_current, use_container_width=True, height=500)


    # ==========================
    # TAB 6 — Hallazgos Excel DQ Consolidadas
    # ==========================
    with tab6:

        st.markdown("""
            <p class="subtitle">📑 Hallazgos del Excel — Reglas Consolidadas</p>
        """, unsafe_allow_html=True)

        df_rules = pd.read_excel("dataplex_dq_rules_consolidado.xlsx", engine="openpyxl")

        total_rules = len(df_rules)
        dims = df_rules["dimension"].value_counts()
        perc = (dims / total_rules * 100).round(2)

        summary_dim = pd.DataFrame({
            "Dimensión": dims.index,
            "Reglas": dims.values,
            "Porcentaje": perc.values
        })

        st.write("### 🔍 Resumen general")
        colA, colB, colC = st.columns(3)
        colA.metric("📦 Total reglas", f"{total_rules:,}")
        colB.metric("📘 Completitud (%)", f"{perc.get('COMPLETENESS',0)}%")
        colC.metric("📙 Validez (%)", f"{perc.get('VALIDITY',0)}%")

        st.write("### 📊 Reglas por dimensión")
        st.dataframe(summary_dim, use_container_width=True)

        st.write("### 📈 Distribución de reglas por dimensión")
        fig_dim = px.bar(
            summary_dim,
            x="Dimensión",
            y="Reglas",
            color="Dimensión",
            text="Reglas",
            title="Distribución por Dimensión",
            color_discrete_sequence=["#004C97","#003366","#0073CF"]
        )
        st.plotly_chart(fig_dim, use_container_width=True)

        st.write("### 🧭 Radar porcentual")
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=summary_dim["Porcentaje"],
            theta=summary_dim["Dimensión"],
            fill='toself',
            line_color="#004C97"
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0,100])),
            showlegend=False
        )
        st.plotly_chart(fig_radar, use_container_width=True)

        st.write("### 📝 Conclusiones")
        st.markdown("""
        - **Completitud** domina (~46%), reflejando un fuerte enfoque en evitar nulls.  
        - **Validez** también es robusta (~42%), indicando un uso intensivo de catálogos, dominios y rangos.  
        - **Unicidad** es baja (~12%), lo que sugiere reglas mal configuradas o no aplicables.  
        """)

    st.markdown("<footer>© 2026 Bunge Global SA — Todos los derechos reservados</footer>", unsafe_allow_html=True)
