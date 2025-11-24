
import streamlit as st
import yaml
import random
from datetime import datetime, date
import plotly.express as px
import plotly.graph_objects as go

# ==========================
# Configuración de la página
# ==========================
st.set_page_config(page_title="DQaaS - Bunge Global SA", page_icon="🌐", layout="wide")

# ==========================
# Estado inicial
# ==========================
if "perfilado_iniciado" not in st.session_state:
    st.session_state.perfilado_iniciado = False

# ==========================
# CSS condicional para el ancho del contenedor
# ==========================
if not st.session_state.perfilado_iniciado:
    st.markdown("""
        <style>
        .block-container {
            max-width: 900px;
            margin-left: auto;
            margin-right: auto;
        }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        .block-container {
            max-width: 1200px;
            margin-left: auto;
            margin-right: auto;
        }
        </style>
    """, unsafe_allow_html=True)

# ==========================
# Pantalla inicial
# ==========================
if not st.session_state.perfilado_iniciado:
    st.markdown("""
        <div style="text-align: center; margin-top: 80px;">
            https://delivery.bunge.com/-/jssmedia/Feature/Components/Basic/Icons/NewLogo.ashx?iar=0&hash=F544E33B7C336344D37599CBB3053C28
            <h1 style="color: #004C97; font-size: 48px; font-weight: bold;">DQaaS - Data Quality as a Service</h1>
            <p style="color: #003366; font-size: 22px; font-weight: bold;">
                Bunge Global SA - Viterra Data Products Squad Extension
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <style>
        div.stButton > button {
            width: 300px;
            height: 60px;
            font-size: 24px;
            font-weight: bold;
            background-color: #004C97;
            color: white;
            border-radius: 10px;
            border: none;
            transition: 0.3s;
        }
        div.stButton > button:hover {
            background-color: #003366;
            transform: scale(1.05);
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    col_left, col_center, col_right = st.columns([3, 2, 5.3])
    with col_center:
        if st.button("🚀 Iniciar Perfilado de Datos", key="start_button", use_container_width=True):
            st.session_state.perfilado_iniciado = True
            st.rerun()

else:
    # ==========================
    # Encabezado con logo y título
    # ==========================
    st.markdown("""
        <div style="text-align: center; margin-bottom: 30px;">
            https://delivery.bunge.com/-/jssmedia/Feature/Components/Basic/Icons/NewLogo.ashx?iar=0&hash=F544E33B7C336344D37599CBB3053C28
            <h1 style="color: #004C97; font-size: 48px; font-weight: bold; margin: 0;">DQaaS - Data Quality as a Service</h1>
            <p style="color: #003366; font-size: 22px; font-weight: bold; margin-top: 10px;">
                Bunge Global SA - Viterra Data Products Squad Extension
            </p>
        </div>
    """, unsafe_allow_html=True)

    # ==========================
    # Estilos (solo títulos y footer)
    # ==========================
    st.markdown("""
        <style>
        .subtitle { font-size: 24px; font-weight: bold; color: #004C97; margin-bottom: -10px; }
        footer { text-align: center; color: #6b6b6b; margin-top: 40px; }
        </style>
    """, unsafe_allow_html=True)

    # ==========================
    # Único Dataproduct -> CSV local
    # ==========================
    DATASETS = {
        "Dataproduct_Prueba": "./datos_prueba.csv",
    }

    st.markdown('<p class="subtitle">Seleccione el dataproduct:</p>', unsafe_allow_html=True)
    dataproduct_visible = st.selectbox("", list(DATASETS.keys()))
    path_csv = DATASETS[dataproduct_visible]

    # ==========================
    # Utilidades de perfilado (global/segmento)
    # ==========================
    import pandas as pd
    import numpy as np
    import re
    from pathlib import Path
    from pandas.api.types import (
        is_datetime64_any_dtype, is_object_dtype, is_numeric_dtype
    )

    @st.cache_data(show_spinner=False)
    def load_csv_local(path_str: str) -> pd.DataFrame:
        p = Path(path_str)
        if not p.exists():
            raise FileNotFoundError(f"No se encuentra el archivo: {p.resolve()}")
        try:
            return pd.read_csv(p)
        except UnicodeDecodeError:
            return pd.read_csv(p, encoding="latin-1")

    def infer_types(df: pd.DataFrame):
        # Normaliza strings
        for col in df.columns:
            if is_object_dtype(df[col]):
                df[col] = df[col].astype(str).str.strip()

        # Detecta & convierte columnas datetime desde object si >=60% parseables
        def maybe_to_datetime(series: pd.Series) -> bool:
            try:
                parsed = pd.to_datetime(series, errors="coerce", infer_datetime_format=True)
                return parsed.notna().mean() >= 0.6
            except Exception:
                return False

        for col in df.columns:
            if is_object_dtype(df[col]) and maybe_to_datetime(df[col]):
                df[col] = pd.to_datetime(df[col], errors="coerce", infer_datetime_format=True)

        numeric_cols = [c for c in df.columns if is_numeric_dtype(df[c])]
        datetime_cols = [c for c in df.columns if is_datetime64_any_dtype(df[c])]
        categorical_cols = [c for c in df.columns
                            if (df[c].dtype.name in ("object", "category")) and c not in datetime_cols]
        return df, numeric_cols, datetime_cols, categorical_cols

    def derive_default_keys(df: pd.DataFrame):
        id_like = [c for c in df.columns if re.search(r"\bid\b", c, flags=re.IGNORECASE)]
        if id_like:
            return id_like
        elif any(is_numeric_dtype(df[c]) for c in df.columns):
            num_local = [c for c in df.columns if is_numeric_dtype(df[c])]
            return [num_local[0]]
        else:
            return [df.columns[0]] if len(df.columns) > 0 else []

    # ---- Parámetros por defecto fijos ----
    P_LOW_DEFAULT = 5.0       # Percentil inferior para rangos numéricos
    P_HIGH_DEFAULT = 95.0     # Percentil superior para rangos numéricos
    MAX_CAT_DEFAULT = 20      # Top-N categorías permitidas en categóricas
    ALLOW_FUTURE_DEFAULT = False  # Fechas futuras no permitidas

    def make_rules_and_metrics(df: pd.DataFrame,
                               numeric_cols: list,
                               datetime_cols: list,
                               categorical_cols: list,
                               key_cols: list,
                               p_low: float,
                               p_high: float,
                               max_cat: int,
                               allow_future_dates: bool):
        n_rows, n_cols = df.shape
        reglas = []

        # No nulos
        for col in df.columns:
            reglas.append({
                "name": f"{col}_not_null",
                "description": f"{col} no debe ser nulo",
                "condition": f"{col} IS NOT NULL",
                "dimension": "Completitud"
            })

        # Unicidad por columnas clave (si existe alguna inferida)
        if key_cols:
            reglas.append({
                "name": f"unique_key_{'_'.join(key_cols)}",
                "description": f"Clave única basada en columnas: {', '.join(key_cols)}",
                "condition": f"UNIQUE({', '.join(key_cols)})",
                "dimension": "Unicidad"
            })

        # Rangos y no-negatividad
        for col in numeric_cols:
            q_low = df[col].quantile(p_low / 100.0)
            q_high = df[col].quantile(p_high / 100.0)
            reglas.append({
                "name": f"{col}_range",
                "description": f"{col} entre P{p_low:.1f}={q_low:.3f} y P{p_high:.1f}={q_high:.3f}",
                "condition": f"{col} BETWEEN {q_low:.3f} AND {q_high:.3f}",
                "dimension": "Validez"
            })
            reglas.append({
                "name": f"{col}_non_negative",
                "description": f"{col} ≥ 0 (si aplica)",
                "condition": f"{col} >= 0",
                "dimension": "Validez"
            })

        # Fechas no futuras
        for col in datetime_cols:
            reglas.append({
                "name": f"{col}_not_future",
                "description": f"{col} no puede ser futura",
                "condition": f"{col} <= CURRENT_DATE",
                "dimension": "Validez"
            })

        # Categóricas: top-N permitidas
        for col in categorical_cols:
            top_vals = df[col].value_counts(dropna=True).head(max_cat).index.tolist()
            reglas.append({
                "name": f"{col}_allowed_values",
                "description": f"{col} dentro de las {len(top_vals)} categorías más frecuentes",
                "condition": f"{col} IN {top_vals}",
                "dimension": "Consistencia"
            })

        # Métricas
        total_cells = n_rows * n_cols if n_rows and n_cols else 0
        completeness = (df.notna().sum().sum() / total_cells * 100.0) if total_cells > 0 else 0.0

        if key_cols:
            keys_non_null = df[key_cols].notna().all(axis=1)
            key_tuples = [tuple(x) for x in df[key_cols].values]
            unique_count = len(set(key_tuples))
            uniqueness = (unique_count / n_rows * 100.0) if n_rows > 0 else 0.0
            integrity_key = keys_non_null.mean() * 100.0
        else:
            uniqueness = (df.drop_duplicates().shape[0] / n_rows * 100.0) if n_rows > 0 else 0.0
            integrity_key = 0.0

        validity_scores = []
        for col in numeric_cols:
            q_low = df[col].quantile(p_low / 100.0)
            q_high = df[col].quantile(p_high / 100.0)
            mask_range = df[col].between(q_low, q_high, inclusive="both")
            mask_nonneg = df[col] >= 0
            validity_scores.append(mask_range.mean() * 100.0 if n_rows > 0 else 0.0)
            validity_scores.append(mask_nonneg.mean() * 100.0 if n_rows > 0 else 0.0)
        for col in datetime_cols:
            if allow_future_dates:
                validity_scores.append(100.0)
            else:
                mask_date = df[col] <= pd.Timestamp(date.today())
                validity_scores.append(mask_date.mean() * 100.0 if n_rows > 0 else 0.0)
        validity = round(np.mean(validity_scores), 2) if validity_scores else 0.0

        consistency_scores = []
        for col in categorical_cols:
            top_vals = df[col].value_counts(dropna=True).head(max_cat).index.tolist()
            consistency_scores.append(df[col].isin(top_vals).mean() * 100.0 if n_rows > 0 else 0.0)
        consistency = round(np.mean(consistency_scores), 2) if consistency_scores else 0.0

        accuracy_scores = []
        for col in numeric_cols:
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
            accuracy_scores.append(df[col].between(low, high, inclusive="both").mean() * 100.0 if n_rows > 0 else 0.0)
        accuracy = round(np.mean(accuracy_scores), 2) if accuracy_scores else 0.0

        metrics = {
            "Completitud": round(completeness, 2),
            "Unicidad": round(uniqueness, 2),
            "Consistencia": round(consistency, 2),
            "Validez": round(validity, 2),
            "Integridad Clave": round(integrity_key, 2),
            "Exactitud": round(accuracy, 2)
        }
        return reglas, metrics

    # ==========================
    # Carga + perfilado (Global/Segmento según selección inmediata)
    # ==========================
    try:
        df = load_csv_local(path_csv)
        df, numeric_cols, datetime_cols, categorical_cols = infer_types(df)

        # ---- Selección inmediata de campo de filtro y segmento (SIN DEFAULTS) ----
        # Campo de filtro sugerido: 'Country' si existe, sino primer categórico o la primera columna
        default_filter_col = "Country" if "Country" in df.columns else (categorical_cols[0] if categorical_cols else df.columns[0])
        st.markdown('<p class="subtitle">🎯 Segmentación</p>', unsafe_allow_html=True)
        col_f1, col_f2 = st.columns([1, 2])
        with col_f1:
            seg_col = st.selectbox(
                "Campo de filtro",
                options=df.columns.tolist(),
                index=df.columns.tolist().index(default_filter_col) if default_filter_col in df.columns else 0,
                key="filter_col_immediate"
            )
        with col_f2:
            # SIN preselección de valores (global por defecto)
            unique_vals = sorted(df[seg_col].dropna().unique().tolist())
            seg_vals = st.multiselect(f"Valores para {seg_col}", options=unique_vals, default=[], key="seg_vals_immediate")

        # ---- Dataset actual según selección ----
        df_current = df[df[seg_col].isin(seg_vals)].copy() if seg_vals else df.copy()

        # ---- Inferir tipos y construir reglas/métricas sobre el ámbito actual ----
        df_current, num_cur, dt_cur, cat_cur = infer_types(df_current)
        key_cols_cur = derive_default_keys(df_current)

        reglas_cur, metricas_cur = make_rules_and_metrics(
            df_current, num_cur, dt_cur, cat_cur,
            key_cols_cur, P_LOW_DEFAULT, P_HIGH_DEFAULT, MAX_CAT_DEFAULT, ALLOW_FUTURE_DEFAULT
        )

        # Regla de contexto si hay segmento seleccionado
        if seg_vals:
            reglas_cur.insert(0, {
                "name": f"segment_filter_{seg_col}",
                "description": f"Reglas calculadas sobre el segmento: {seg_col} IN {seg_vals}",
                "condition": f"{seg_col} IN {seg_vals}",
                "dimension": "Contexto"
            })

        # Umbral para métricas
        umbral = 90

        # ==========================
        # Pestañas principales (reflejan el ámbito actual)
        # ==========================
        scope_label = "Global" if not seg_vals else f"Segmento: {seg_col} ∈ {seg_vals}"
        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            ["📋 Reglas", "📊 Métricas", "📈 Gráficos", "⬇️ Descargar YAML", "📂 Vista de datos"]
        )

        # --- Reglas (Ámbito actual) ---
        with tab1:
            st.markdown(f'<p class="subtitle">📋 Reglas ({scope_label})</p>', unsafe_allow_html=True)
            st.table(reglas_cur)

        # --- Métricas (Ámbito actual) ---
        with tab2:
            st.markdown(f'<p class="subtitle">📊 Métricas ({scope_label})</p>', unsafe_allow_html=True)
            cols = st.columns(len(metricas_cur))
            for i, (k, v) in enumerate(metricas_cur.items()):
                color = "normal" if v >= umbral else "inverse"
                estado = "✅" if v >= umbral else "⚠️"
                cols[i].metric(label=k, value=f"{v}% {estado}", delta="", delta_color=color)

        # --- Gráficos (Ámbito actual) ---
        with tab3:
            st.markdown(f'<p class="subtitle">📈 Gráficos ({scope_label})</p>', unsafe_allow_html=True)
            fig_bar = px.bar(
                x=list(metricas_cur.keys()), y=list(metricas_cur.values()),
                color=list(metricas_cur.keys()),
                title=f"Métricas de Calidad — {dataproduct_visible} ({scope_label})",
                labels={"x": "Dimensión", "y": "Porcentaje"}
            )
            st.plotly_chart(fig_bar, use_container_width=True)

            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=list(metricas_cur.values()), theta=list(metricas_cur.keys()),
                fill='toself', name='Calidad'
            ))
            min_axis = max(0, min(metricas_cur.values()) - 10) if metricas_cur else 0
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[min_axis, 100])),
                showlegend=False, title=f"Radar de Calidad — {dataproduct_visible} ({scope_label})"
            )
            st.plotly_chart(fig_radar, use_container_width=True)

        # --- Descargar YAML (Ámbito actual) ---
        with tab4:
            if not seg_vals:
                # YAML Global
                yaml_current = {
                    "metadata": {
                        "company": "Bunge Global SA",
                        "generated_by": "DQaaS Streamlit App",
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "source_system": f"Local file ({dataproduct_visible})"
                    },
                    "dataset": {
                        "name": dataproduct_visible,
                        "source": path_csv,
                        "rows": int(len(df_current)),
                        "columns": int(len(df_current.columns)),
                        "numeric_columns": num_cur,
                        "datetime_columns": dt_cur,
                        "categorical_columns": cat_cur,
                        "key_columns_inferred": key_cols_cur
                    },
                    "rules": reglas_cur,
                    "quality_metrics": metricas_cur,
                    "parameters": {
                        "percentile_low": P_LOW_DEFAULT,
                        "percentile_high": P_HIGH_DEFAULT,
                        "max_allowed_categories": MAX_CAT_DEFAULT,
                        "allow_future_dates": ALLOW_FUTURE_DEFAULT
                    },
                    "filter_field": seg_col
                }
                file_name = f"csv_quality_profile_global_{dataproduct_visible.replace(' ', '_')}.yaml"
                button_label = f"Descargar YAML (Global) — {dataproduct_visible}"
            else:
                # YAML Segmento
                yaml_current = {
                    "metadata": {
                        "company": "Bunge Global SA",
                        "generated_by": "DQaaS Streamlit App",
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "source_system": f"Local file ({dataproduct_visible})"
                    },
                    "segment": {
                        "column": seg_col,
                        "values": seg_vals,
                        "rows": int(len(df_current)),
                        "columns": int(len(df_current.columns))
                    },
                    "dataset_columns": {
                        "numeric": num_cur,
                        "datetime": dt_cur,
                        "categorical": cat_cur,
                        "key_columns_inferred": key_cols_cur
                    },
                    "rules": reglas_cur,
                    "quality_metrics": metricas_cur,
                    "parameters": {
                        "percentile_low": P_LOW_DEFAULT,
                        "percentile_high": P_HIGH_DEFAULT,
                        "max_allowed_categories": MAX_CAT_DEFAULT,
                        "allow_future_dates": ALLOW_FUTURE_DEFAULT
                    }
                }
                file_name = f"csv_quality_profile_segment_{dataproduct_visible}_{seg_col}.yaml"
                button_label = f"Descargar YAML (Segmento) — {dataproduct_visible}"

            yaml_str = yaml.dump(yaml_current, allow_unicode=True, sort_keys=False)
            st.download_button(
                label=button_label,
                data=yaml_str,
                file_name=file_name,
                mime="text/yaml"
            )

        # --- Vista de datos (Ámbito actual) ---
        with tab5:
            st.markdown(f'<p class="subtitle">📂 Vista CSV ({scope_label})</p>', unsafe_allow_html=True)
            if seg_vals:
                st.caption(f"Filas segmento: {len(df_current):,} / {len(df):,} [{seg_col} ∈ {seg_vals}]")
            else:
                st.caption(f"Global: mostrando dataset completo ({len(df):,} filas)")
            if len(df_current) == 0:
                st.warning("El segmento seleccionado no tiene filas. Ajusta los valores del filtro.")
            else:
                st.dataframe(df_current, use_container_width=True, height=520)

    except Exception as e:
        st.error(f"Error procesando el CSV: {e}")
        st.info("Verifica que 'datos_prueba.csv' exista al mismo nivel que 'streamlit_app.py' y que tenga un formato CSV válido.")

    # ==========================
    # Footer
    # ==========================
    st.markdown('<footer>© 2025 Bunge Global SA - Todos los derechos reservados</footer>', unsafe_allow_html=True)
