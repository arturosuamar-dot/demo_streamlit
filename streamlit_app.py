
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
            <img src="https://delivery.bunge.com/-/jssmedia/Feature/Components/Basic/Icons/NewLogo.ashx?iar=0&hash=F544E33B7C336344D37599CBB3053C28"
                 width="180" style="margin-bottom: 20px;">
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
            <img src="https://delivery.bunge.com/-/jssmedia/Feature/Components/Basic/Icons/NewLogo.ashx?iar=0&hash=F544E33B7C336344D37599CBB3053C28"
                 width="180" style="margin-bottom: 10px;">
            <h1 style="color: #004C97; font-size: 48px; font-weight: bold; margin: 0;">DQaaS - Data Quality as a Service</h1>
            <p style="color: #003366; font-size: 22px; font-weight: bold; margin-top: 10px;">
                Bunge Global SA - Viterra Data Products Squad Extension
            </p>
        </div>
    """, unsafe_allow_html=True)

    # ==========================
    # Mapeo de dataproducts (demo)
    # ==========================
    dataproducts_map = {"Clientes": "clientes", "Ventas": "ventas", "Productos": "productos", "Proveedores": "proveedores", "Pedidos": "pedidos"}

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
    # Select dataproduct (demo)
    # ==========================
    st.markdown('<p class="subtitle">Seleccione el dataproduct:</p>', unsafe_allow_html=True)
    dataproduct_visible = st.selectbox("", list(dataproducts_map.keys()))
    dataproduct_seleccionada = dataproducts_map[dataproduct_visible]

    # ==========================
    # Reglas por dataproduct (demo)
    # ==========================
    reglas_por_dataproduct = {
        "clientes": [
            {"name": "no_null_id", "description": "ID no debe ser nulo", "condition": "id IS NOT NULL", "dimension": "Completitud"},
            {"name": "email_format", "description": "Formato de email válido", "condition": "email LIKE '%@%'", "dimension": "Consistencia"},
            {"name": "country_valid", "description": "Código país válido", "condition": "pais IN ('BR','US','AR','ES')", "dimension": "Consistencia"},
            {"name": "tipo_cliente_valid", "description": "Tipo de cliente válido", "condition": "tipo_cliente IN ('Mayorista','Minorista')", "dimension": "Validez"}
        ],
        "ventas": [
            {"name": "positive_amount", "description": "Monto positivo", "condition": "amount > 0", "dimension": "Validez"},
            {"name": "valid_currency", "description": "Moneda válida (USD, BRL, EUR)", "condition": "currency IN ('USD','BRL','EUR')", "dimension": "Consistencia"},
            {"name": "date_not_future", "description": "Fecha no puede ser futura", "condition": "sale_date <= CURRENT_DATE", "dimension": "Validez"}
        ],
        "productos": [
            {"name": "unique_code", "description": "Código único", "condition": "code IS UNIQUE", "dimension": "Unicidad"},
            {"name": "price_range", "description": "Precio entre 100 y 2000 USD/ton", "condition": "price BETWEEN 100 AND 2000", "dimension": "Validez"},
            {"name": "category_not_null", "description": "Categoría no nula", "condition": "category IS NOT NULL", "dimension": "Completitud"}
        ],
        "proveedores": [
            {"name": "country_valid", "description": "Código país ISO válido", "condition": "country IN ('BR','US','AR','ES')", "dimension": "Consistencia"},
            {"name": "contact_email", "description": "Email de contacto válido", "condition": "contact_email LIKE '%@%'", "dimension": "Consistencia"},
            {"name": "tipo_proveedor_valid", "description": "Tipo proveedor válido", "condition": "tipo_proveedor IN ('Local','Internacional')", "dimension": "Validez"}
        ],
        "pedidos": [
            {"name": "status_valid", "description": "Estado válido (PENDIENTE, COMPLETADO)", "condition": "status IN ('PENDIENTE','COMPLETADO')", "dimension": "Consistencia"},
            {"name": "delivery_date_check", "description": "Fecha entrega >= fecha pedido", "condition": "delivery_date >= order_date", "dimension": "Validez"},
            {"name": "quantity_min", "description": "Cantidad mínima 100 toneladas", "condition": "quantity >= 100", "dimension": "Validez"}
        ]
    }

    # ==========================
    # Datos demo
    # ==========================
    clientes_data = [
        {"id": 101, "nombre": "Agroexport SA", "email": "contacto@agroexport.com", "pais": "AR", "tipo_cliente": "Mayorista"},
        {"id": 102, "nombre": "Granos del Sur", "email": "ventas@granosur.com", "pais": "BR", "tipo_cliente": "Minorista"},
        {"id": 103, "nombre": "Bunge Brasil", "email": "info@bunge.com.br", "pais": "BR", "tipo_cliente": "Mayorista"}
    ]
    ventas_data = [
        {"id": 201, "cliente_id": 101, "amount": 150000, "currency": "USD", "sale_date": "2025-11-15"},
        {"id": 202, "cliente_id": 102, "amount": 98000, "currency": "EUR", "sale_date": "2025-11-18"},
        {"id": 203, "cliente_id": 103, "amount": 250000, "currency": "USD", "sale_date": "2025-11-20"}
    ]
    productos_data = [
        {"code": "SOY2025", "name": "Soja Premium", "price": 520, "category": "Oleaginosas", "unidad_medida": "ton"},
        {"code": "MAIZ2025", "name": "Maíz Amarillo", "price": 320, "category": "Cereales", "unidad_medida": "ton"},
        {"code": "TRIGO2025", "name": "Trigo Pan", "price": 410, "category": "Cereales", "unidad_medida": "ton"}
    ]
    proveedores_data = [
        {"id": 301, "nombre": "Proveedor Norte", "country": "ES", "contact_email": "norte@proveedor.com", "tipo_proveedor": "Local"},
        {"id": 302, "nombre": "Proveedor Sur", "country": "BR", "contact_email": "sur@proveedor.com", "tipo_proveedor": "Internacional"}
    ]
    pedidos_data = [
        {"id": 401, "cliente_id": 101, "producto_code": "SOY2025", "status": "PENDIENTE", "order_date": "2025-11-10", "delivery_date": "2025-11-15", "quantity": 120},
        {"id": 402, "cliente_id": 102, "producto_code": "MAIZ2025", "status": "COMPLETADO", "order_date": "2025-11-05", "delivery_date": "2025-11-12", "quantity": 200}
    ]

    # ==========================
    # Métricas demo
    # ==========================
    def generar_metricas():
        return {
            "Completitud": random.randint(85, 99),
            "Unicidad": random.randint(80, 98),
            "Consistencia": random.randint(82, 97),
            "Validez": random.randint(83, 96),
            "Integridad Referencial": random.randint(75, 95),
            "Exactitud": random.randint(78, 94)
        }

    metricas = generar_metricas()
    umbral = 90

    # ==========================
    # Pestañas principales
    # ==========================
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        ["📋 Reglas", "📊 Métricas", "📈 Gráficos", "⬇️ Descargar YAML", "📂 Datos de prueba", "📄 CSV adjunto (auto)"]
    )

    # --- Reglas (demo) ---
    with tab1:
        st.markdown('<p class="subtitle">Reglas para la dataproduct seleccionada:</p>', unsafe_allow_html=True)
        st.table(reglas_por_dataproduct[dataproduct_seleccionada])

    # --- Métricas (demo) ---
    with tab2:
        st.markdown('<p class="subtitle">Métricas de calidad:</p>', unsafe_allow_html=True)
        cols = st.columns(len(metricas))
        for i, (k, v) in enumerate(metricas.items()):
            color = "normal" if v >= umbral else "inverse"
            estado = "✅" if v >= umbral else "⚠️"
            cols[i].metric(label=k, value=f"{v}% {estado}", delta="", delta_color=color)

    # --- Gráficos (demo) ---
    with tab3:
        st.markdown('<p class="subtitle">Visualización de métricas:</p>', unsafe_allow_html=True)
        fig_bar = px.bar(x=list(metricas.keys()), y=list(metricas.values()), color=list(metricas.keys()),
                         title="Métricas de Calidad", labels={"x": "Dimensión", "y": "Porcentaje"})
        st.plotly_chart(fig_bar, use_container_width=True)

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=list(metricas.values()), theta=list(metricas.keys()), fill='toself', name='Calidad'))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[70, 100])), showlegend=False, title="Radar de Calidad")
        st.plotly_chart(fig_radar, use_container_width=True)

    # --- Descargar YAML (demo) ---
    with tab4:
        yaml_data = {
            "metadata": {
                "company": "Bunge Global SA",
                "generated_by": "DQaaS Streamlit App",
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "source_system": "GCP BigQuery"
            },
            "table": dataproduct_seleccionada,
            "rules": reglas_por_dataproduct[dataproduct_seleccionada],
            "quality_metrics": metricas
        }
        yaml_str = yaml.dump(yaml_data, allow_unicode=True)
        st.download_button(label="Descargar reglas y métricas en YAML", data=yaml_str,
                           file_name=f"{dataproduct_seleccionada}_quality.yaml", mime="text/yaml")

    # --- Datos de prueba (demo) ---
    with tab5:
        st.markdown(f"**Datos de la dataproduct {dataproduct_visible}:**")
        if dataproduct_seleccionada == "clientes":
            st.table(clientes_data)
        elif dataproduct_seleccionada == "ventas":
            st.table(ventas_data)
        elif dataproduct_seleccionada == "productos":
            st.table(productos_data)
        elif dataproduct_seleccionada == "proveedores":
            st.table(proveedores_data)
        elif dataproduct_seleccionada == "pedidos":
            st.table(pedidos_data)

    # ========= 📄 CSV adjunto (auto): Selector local =========
    with tab6:
        st.markdown('<p class="subtitle">CSV adjunto: perfilado automático (global y por segmento)</p>', unsafe_allow_html=True)

        import pandas as pd
        import numpy as np
        import re
        from pathlib import Path

        # ---- Catálogo local ----
        DATASETS = {
            # Usa el nombre legible como clave y la ruta relativa como valor
            "datos_prueba.csv": "./datos_prueba.csv",
            # Puedes añadir más si quieres:
            # "otro_dataset.csv": "./otro_dataset.csv",
        }

        fuente = st.selectbox("Selecciona dataset CSV (local)", options=list(DATASETS.keys()))
        path_csv = DATASETS[fuente]

        # ---- Utilidades de carga y tipado ----
        @st.cache_data(show_spinner=False)
        def load_csv_local(path_str: str) -> pd.DataFrame:
            p = Path(path_str)
            if not p.exists():
                raise FileNotFoundError(f"No se encuentra el archivo: {p.resolve()}")
            # Si conoces el separador explícitamente, usa sep="," para mayor rendimiento
            return pd.read_csv(p)

        def infer_types(df: pd.DataFrame):
            # Normaliza strings
            for col in df.select_dtypes(include=["object"]).columns:
                df[col] = df[col].astype(str).str.strip()

            # Detecta columnas datetime en objetos (>=60% parseables)
            def try_parse_datetime(series: pd.Series) -> bool:
                try:
                    parsed = pd.to_datetime(series, errors="coerce")
                    return parsed.notna().mean() >= 0.6
                except Exception:
                    return False

            datetime_candidates = []
            for col in df.columns:
                if df[col].dtype == "object" and try_parse_datetime(df[col]):
                    datetime_candidates.append(col)
            for col in datetime_candidates:
                df[col] = pd.to_datetime(df[col], errors="coerce")

            numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
            datetime_cols = df.select_dtypes(include=["datetime64[ns]", "datetime64[ns, tz]"]).columns.tolist()
            categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
            return df, numeric_cols, datetime_cols, categorical_cols

        def derive_default_keys(df: pd.DataFrame, numeric_cols: list):
            id_like = [c for c in df.columns if re.search(r"\bid\b", c, flags=re.IGNORECASE)]
            if id_like:
                return id_like
            elif numeric_cols:
                return [numeric_cols[0]]
            else:
                return [df.columns[0]] if len(df.columns) > 0 else []

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

            # No nulos por columna
            for col in df.columns:
                reglas.append({
                    "name": f"{col}_not_null",
                    "description": f"{col} no debe ser nulo",
                    "condition": f"{col} IS NOT NULL",
                    "dimension": "Completitud"
                })

            # Unicidad por columnas clave
            if key_cols:
                reglas.append({
                    "name": f"unique_key_{'_'.join(key_cols)}",
                    "description": f"Clave única basada en columnas: {', '.join(key_cols)}",
                    "condition": f"UNIQUE({', '.join(key_cols)})",
                    "dimension": "Unicidad"
                })

            # Rangos por percentiles para numéricas
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

            # Categóricas: top-N permitidas por frecuencia
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

        # ---- Principal CSV (selector local) ----
        try:
            df = load_csv_local(path_csv)
            df, numeric_cols, datetime_cols, categorical_cols = infer_types(df)
            default_keys = derive_default_keys(df, numeric_cols)

            # Configuración global
            with st.expander("⚙️ Configurar reglas (Global)"):
                key_cols_global = st.multiselect("Columnas clave (unicidad)", options=df.columns.tolist(), default=default_keys)
                c1, c2, c3 = st.columns(3)
                p_low_global = c1.slider("Percentil inferior (rangos numéricos)", 0.0, 20.0, 5.0, 0.5)
                p_high_global = c2.slider("Percentil superior (rangos numéricos)", 80.0, 100.0, 95.0, 0.5)
                max_cat_global = c3.slider("Máx. categorías permitidas (top-N)", 5, 50, 20, 1)
                allow_future_global = st.checkbox("Permitir fechas futuras", value=False, key="allow_future_global")

            # Subpestañas: Global / Segmento
            gtab1, gtab2 = st.tabs(["🌍 Global (CSV completo)", "🎯 Segmento (filtrar por columna/valor)"])

            # ----- GLOBAL -----
            with gtab1:
                reglas_global, metricas_global = make_rules_and_metrics(
                    df, numeric_cols, datetime_cols, categorical_cols,
                    key_cols_global, p_low_global, p_high_global, max_cat_global, allow_future_global
                )
                umbral_csv = 90

                # Reglas
                st.markdown('<p class="subtitle">📋 Reglas (Global)</p>', unsafe_allow_html=True)
                st.table(reglas_global)

                # Métricas
                st.markdown('<p class="subtitle">📊 Métricas (Global)</p>', unsafe_allow_html=True)
                cols = st.columns(len(metricas_global))
                for i, (k, v) in enumerate(metricas_global.items()):
                    color = "normal" if v >= umbral_csv else "inverse"
                    estado = "✅" if v >= umbral_csv else "⚠️"
                    cols[i].metric(label=k, value=f"{v}% {estado}", delta="", delta_color=color)

                # Gráficos
                st.markdown('<p class="subtitle">📈 Gráficos (Global)</p>', unsafe_allow_html=True)
                fig_bar_csv = px.bar(x=list(metricas_global.keys()), y=list(metricas_global.values()),
                                     color=list(metricas_global.keys()), title="Métricas de Calidad (Global)",
                                     labels={"x": "Dimensión", "y": "Porcentaje"})
                st.plotly_chart(fig_bar_csv, use_container_width=True)
                fig_radar_csv = go.Figure()
                fig_radar_csv.add_trace(go.Scatterpolar(
                    r=list(metricas_global.values()), theta=list(metricas_global.keys()),
                    fill='toself', name='Calidad Global'
                ))
                min_axis = max(0, min(metricas_global.values()) - 10)
                fig_radar_csv.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[min_axis, 100])),
                    showlegend=False, title="Radar de Calidad (Global)"
                )
                st.plotly_chart(fig_radar_csv, use_container_width=True)

                # YAML
                st.markdown('<p class="subtitle">⬇️ Descargar YAML (Global)</p>', unsafe_allow_html=True)
                yaml_global = {
                    "metadata": {
                        "company": "Bunge Global SA",
                        "generated_by": "DQaaS Streamlit App",
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "source_system": f"Local file ({fuente})"
                    },
                    "dataset": {
                        "name": fuente,
                        "source": path_csv,
                        "rows": int(len(df)),
                        "columns": int(len(df.columns)),
                        "numeric_columns": numeric_cols,
                        "datetime_columns": datetime_cols,
                        "categorical_columns": categorical_cols,
                        "key_columns": key_cols_global
                    },
                    "rules": reglas_global,
                    "quality_metrics": metricas_global,
                    "parameters": {
                        "percentile_low": p_low_global,
                        "percentile_high": p_high_global,
                        "max_allowed_categories": max_cat_global,
                        "allow_future_dates": allow_future_global
                    }
                }
                yaml_str_global = yaml.dump(yaml_global, allow_unicode=True, sort_keys=False)
                st.download_button(
                    label="Descargar YAML (Global)",
                    data=yaml_str_global,
                    file_name=f"csv_quality_profile_global_{fuente.replace(' ', '_')}.yaml",
                    mime="text/yaml"
                )

                # Vista de datos (Global)
                st.markdown('<p class="subtitle">📂 Vista CSV (Global)</p>', unsafe_allow_html=True)
                st.dataframe(df, use_container_width=True, height=520)

            # ----- SEGMENTO -----
            with gtab2:
                st.markdown('<p class="subtitle">🎯 Configurar segmento</p>', unsafe_allow_html=True)
                default_segment_col = "Country" if "Country" in df.columns else (categorical_cols[0] if categorical_cols else df.columns[0])
                seg_col = st.selectbox("Columna de segmento", options=df.columns.tolist(),
                                       index=df.columns.tolist().index(default_segment_col) if default_segment_col in df.columns else 0)

                unique_vals = sorted(df[seg_col].dropna().unique().tolist())
                default_vals = ["Spain"] if seg_col == "Country" and "Spain" in unique_vals else []
                seg_vals = st.multiselect(f"Valores para {seg_col}", options=unique_vals, default=default_vals)

                with st.expander("⚙️ Configurar reglas (Segmento)"):
                    key_cols_seg = st.multiselect("Columnas clave (unicidad, segmento)", options=df.columns.tolist(), default=default_keys, key="key_cols_seg")
                    c1, c2, c3 = st.columns(3)
                    p_low_seg = c1.slider("Percentil inferior (segmento)", 0.0, 20.0, 5.0, 0.5, key="p_low_seg")
                    p_high_seg = c2.slider("Percentil superior (segmento)", 80.0, 100.0, 95.0, 0.5, key="p_high_seg")
                    max_cat_seg = c3.slider("Máx. categorías permitidas (segmento)", 5, 50, 20, 1, key="max_cat_seg")
                    allow_future_seg = st.checkbox("Permitir fechas futuras (segmento)", value=False, key="allow_future_seg")

                df_segment = df[df[seg_col].isin(seg_vals)].copy() if seg_vals else df.copy()
                df_segment, num_seg, dt_seg, cat_seg = infer_types(df_segment)

                reglas_seg, metricas_seg = make_rules_and_metrics(
                    df_segment, num_seg, dt_seg, cat_seg,
                    key_cols_seg, p_low_seg, p_high_seg, max_cat_seg, allow_future_seg
                )

                if seg_vals:
                    reglas_seg.insert(0, {
                        "name": f"segment_filter_{seg_col}",
                        "description": f"Reglas calculadas sobre el segmento: {seg_col} IN {seg_vals}",
                        "condition": f"{seg_col} IN {seg_vals}",
                        "dimension": "Contexto"
                    })

                st.markdown('<p class="subtitle">📋 Reglas (Segmento)</p>', unsafe_allow_html=True)
                st.table(reglas_seg)

                umbral_seg = 90
                st.markdown('<p class="subtitle">📊 Métricas (Segmento)</p>', unsafe_allow_html=True)
                cols = st.columns(len(metricas_seg))
                for i, (k, v) in enumerate(metricas_seg.items()):
                    color = "normal" if v >= umbral_seg else "inverse"
                    estado = "✅" if v >= umbral_seg else "⚠️"
                    cols[i].metric(label=k, value=f"{v}% {estado}", delta="", delta_color=color)

                st.markdown('<p class="subtitle">📈 Gráficos (Segmento)</p>', unsafe_allow_html=True)
                fig_bar_seg = px.bar(x=list(metricas_seg.keys()), y=list(metricas_seg.values()),
                                     color=list(metricas_seg.keys()), title=f"Métricas de Calidad (Segmento: {seg_col})",
                                     labels={"x": "Dimensión", "y": "Porcentaje"})
                st.plotly_chart(fig_bar_seg, use_container_width=True)
                fig_radar_seg = go.Figure()
                fig_radar_seg.add_trace(go.Scatterpolar(
                    r=list(metricas_seg.values()), theta=list(metricas_seg.keys()),
                    fill='toself', name='Calidad Segmento'
                ))
                min_axis_seg = max(0, min(metricas_seg.values()) - 10)
                fig_radar_seg.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[min_axis_seg, 100])),
                    showlegend=False, title=f"Radar de Calidad (Segmento: {seg_col})"
                )
                st.plotly_chart(fig_radar_seg, use_container_width=True)

                st.markdown('<p class="subtitle">⬇️ Descargar YAML (Segmento)</p>', unsafe_allow_html=True)
                yaml_seg = {
                    "metadata": {
                        "company": "Bunge Global SA",
                        "generated_by": "DQaaS Streamlit App",
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "source_system": f"Local file ({fuente})"
                    },
                    "segment": {
                        "column": seg_col,
                        "values": seg_vals,
                        "rows": int(len(df_segment)),
                        "columns": int(len(df_segment.columns))
                    },
                    "dataset_columns": {
                        "numeric": num_seg,
                        "datetime": dt_seg,
                        "categorical": cat_seg,
                        "key_columns": key_cols_seg
                    },
                    "rules": reglas_seg,
                    "quality_metrics": metricas_seg,
                    "parameters": {
                        "percentile_low": p_low_seg,
                        "percentile_high": p_high_seg,
                        "max_allowed_categories": max_cat_seg,
                        "allow_future_dates": allow_future_seg
                    }
                }
                yaml_str_seg = yaml.dump(yaml_seg, allow_unicode=True, sort_keys=False)
                st.download_button(
                    label="Descargar YAML (Segmento)",
                    data=yaml_str_seg,
                    file_name=f"csv_quality_profile_segment_{seg_col}.yaml",
                    mime="text/yaml"
                )

                st.markdown('<p class="subtitle">📂 Vista CSV (Segmento)</p>', unsafe_allow_html=True)
                if seg_vals:
                    st.caption(f"Filas segmento: {len(df_segment):,} / {len(df):,} [{seg_col} ∈ {seg_vals}]")
                else:
                    st.caption(f"Sin valores seleccionados: mostrando dataset completo ({len(df):,} filas)")
                st.dataframe(df_segment, use_container_width=True, height=520)

        except Exception as e:
            st.error(f"Error procesando el CSV: {e}")
            st.info("Verifica que 'datos_prueba.csv' exista al mismo nivel que 'streamlit_app.py' y que tenga un formato CSV válido.")

    # ==========================
    # Footer
    # ==========================
    st.markdown('<footer>© 2025 Bunge Global SA - Todos los derechos reservados</footer>', unsafe_allow_html=True)
