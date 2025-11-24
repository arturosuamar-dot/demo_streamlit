
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
    # Portada: contenedor más estrecho y centrado
    st.markdown("""
        <style>
        .block-container {
            max-width: 900px;  /* landing centrada y cómoda */
            margin-left: auto;
            margin-right: auto;
        }
        </style>
    """, unsafe_allow_html=True)
else:
    # App iniciada: contenedor más ancho para desktop
    st.markdown("""
        <style>
        .block-container {
            max-width: 1200px;  /* ajusta 1100-1400 según tu preferencia */
            margin-left: auto;
            margin-right: auto;
        }
        </style>
    """, unsafe_allow_html=True)

# ==========================
# Pantalla inicial
# ==========================
if not st.session_state.perfilado_iniciado:
    # Portada con logo, título y subtítulo (HTML correcto)
    st.markdown("""
        <div style="text-align: center; margin-top: 80px;">
            <img src="https://delivery.bunge.com/-/jssmedia/Feature/Components/Basic/Icons/NewLogo.ashx?iar=0&hash=F544E33B7C336344D37599CBB3053C28" width="180" style="margin-bottom: 20px;">
            <h1 style="color: #004C97; font-size: 48px; font-weight: bold;">DQaaS - Data Quality as a Service</h1>
            <p style="color: #003366; font-size: 22px; font-weight: bold;">
                Bunge Global SA - Viterra Data Products Squad Extension
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Estilo SOLO del botón (sin cambiar el layout)
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

    # Espaciado bajo el título
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # Botón ligeramente desplazado a la izquierda (asimetría en columnas)
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
            <img src="https://delivery.bunge.com/-/jssmedia/Feature/Components/Basic/Icons/NewLogo.ashx?iar=0&hash=F544E33B7C336344D37599CBB3053C28" width="180" style="margin-bottom: 10px;">
            <h1 style="color: #004C97; font-size: 48px; font-weight: bold; margin: 0;">DQaaS - Data Quality as a Service</h1>
            <p style="color: #003366; font-size: 22px; font-weight: bold; margin-top: 10px;">
                Bunge Global SA - Viterra Data Products Squad Extension
            </p>
        </div>
    """, unsafe_allow_html=True)

    # ==========================
    # Sidebar
    # ==========================
    st.sidebar.header("Opciones")
    st.sidebar.info("Selecciona la tabla y genera reglas de calidad en formato Bunge YAML.")
    if st.sidebar.button("Conectar a GCP", key="gcp_button"):
        st.sidebar.success("Conexión simulada con BigQuery ✅")

    # ==========================
    # Mapeo de tablas
    # ==========================
    tablas_map = {
        "Clientes": "clientes",
        "Ventas": "ventas",
        "Productos": "productos",
        "Proveedores": "proveedores",
        "Pedidos": "pedidos"
    }

    # ==========================
    # Estilos (solo títulos y footer)
    # ==========================
    st.markdown("""
        <style>
        .subtitle {
            font-size: 24px;
            font-weight: bold;
            color: #004C97;
            margin-bottom: -10px;
        }
        footer {
            text-align: center;
            color: #6b6b6b;
            margin-top: 40px;
        }
        </style>
    """, unsafe_allow_html=True)

    # ==========================
    # Select tabla (demo fija)
    # ==========================
    st.markdown('<p class="subtitle">Selecciona una tabla:</p>', unsafe_allow_html=True)
    tabla_visible = st.selectbox("", list(tablas_map.keys()))
    tabla_seleccionada = tablas_map[tabla_visible]

    # ==========================
    # Reglas por tabla (demo fija)
    # ==========================
    reglas_por_tabla = {
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
    # Pestañas
    # ==========================
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        ["📋 Reglas", "📊 Métricas", "📈 Gráficos", "⬇️ Descargar YAML", "📂 Datos de prueba", "📄 CSV adjunto (auto)"]
    )

    # --- Reglas ---
    with tab1:
        st.markdown('<p class="subtitle">Reglas para la tabla seleccionada:</p>', unsafe_allow_html=True)
        st.table(reglas_por_tabla[tabla_seleccionada])

    # --- Métricas ---
    with tab2:
        st.markdown('<p class="subtitle">Métricas de calidad:</p>', unsafe_allow_html=True)
        cols = st.columns(len(metricas))
        for i, (k, v) in enumerate(metricas.items()):
            color = "normal" if v >= umbral else "inverse"
            estado = "✅" if v >= umbral else "⚠️"
            cols[i].metric(label=k, value=f"{v}% {estado}", delta="", delta_color=color)

    # --- Gráficos ---
    with tab3:
        st.markdown('<p class="subtitle">Visualización de métricas:</p>', unsafe_allow_html=True)
        fig_bar = px.bar(
            x=list(metricas.keys()),
            y=list(metricas.values()),
            color=list(metricas.keys()),
            title="Métricas de Calidad",
            labels={"x": "Dimensión", "y": "Porcentaje"}
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=list(metricas.values()), theta=list(metricas.keys()), fill='toself', name='Calidad'))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[70, 100])), showlegend=False, title="Radar de Calidad")
        st.plotly_chart(fig_radar, use_container_width=True)

    # --- Descargar YAML (demo tabla) ---
    with tab4:
        yaml_data = {
            "metadata": {
                "company": "Bunge Global SA",
                "generated_by": "DQaaS Streamlit App",
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "source_system": "GCP BigQuery"
            },
            "table": tabla_seleccionada,
            "rules": reglas_por_tabla[tabla_seleccionada],
            "quality_metrics": metricas
        }
        yaml_str = yaml.dump(yaml_data, allow_unicode=True)
        st.download_button(
            label="Descargar reglas y métricas en YAML",
            data=yaml_str,
            file_name=f"{tabla_seleccionada}_quality.yaml",
            mime="text/yaml"
        )

    # --- Datos de prueba ---
    with tab5:
        st.markdown(f"**Datos de la tabla {tabla_visible}:**")
        if tabla_seleccionada == "clientes":
            st.table(clientes_data)
        elif tabla_seleccionada == "ventas":
            st.table(ventas_data)
        elif tabla_seleccionada == "productos":
            st.table(productos_data)
        elif tabla_seleccionada == "proveedores":
            st.table(proveedores_data)
        elif tabla_seleccionada == "pedidos":
            st.table(pedidos_data)

    # ========= 📄 CSV adjunto (auto): reglas, métricas, gráficos, YAML, datos =========
    with tab6:
        st.markdown('<p class="subtitle">CSV adjunto: perfilado automático (cualquier esquema)</p>', unsafe_allow_html=True)

        import pandas as pd
        import numpy as np
        import re

        # ---- Carga del CSV ----
        csv_file = st.file_uploader("Sube un CSV (cualquier esquema)", type=["csv"], key="csv_uploader_auto")

        def load_csv_to_df(uploaded) -> pd.DataFrame:
            if uploaded is not None:
                return pd.read_csv(uploaded)
            else:
                # Por defecto intenta leer el CSV que compartiste previamente
                return pd.read_csv("global_agribusiness_food_company_1000_2.csv")

        try:
            df = load_csv_to_df(csv_file)
            n_rows, n_cols = df.shape

            # ---- Inferencia de tipos ----
            # Convertimos objetos a datetime si >60% de parseo posible
            def try_parse_datetime(series: pd.Series) -> bool:
                try:
                    parsed = pd.to_datetime(series, errors="coerce", infer_datetime_format=True)
                    return parsed.notna().mean() >= 0.6
                except Exception:
                    return False

            # Normaliza strings (espacios)
            for col in df.select_dtypes(include=["object"]).columns:
                df[col] = df[col].astype(str).str.strip()

            # Detecta posibles fechas en columnas object
            datetime_candidates = []
            for col in df.columns:
                if df[col].dtype == "object" and try_parse_datetime(df[col]):
                    datetime_candidates.append(col)
            # Castea esas columnas a datetime
            for col in datetime_candidates:
                df[col] = pd.to_datetime(df[col], errors="coerce", infer_datetime_format=True)

            numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
            datetime_cols = df.select_dtypes(include=["datetime"]).columns.tolist()
            categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

            # Heurística para clave(s): columnas que contengan 'id' en el nombre
            id_like = [c for c in df.columns if re.search(r"\bid\b", c, flags=re.IGNORECASE)]
            default_keys = id_like if id_like else ([numeric_cols[0]] if numeric_cols else [df.columns[0]])

            # ---- Controles de configuración dinámica ----
            with st.expander("⚙️ Configurar reglas (CSV)"):
                key_cols = st.multiselect(
                    "Columnas clave para Unicidad (puede ser compuesto)",
                    options=df.columns.tolist(),
                    default=default_keys
                )
                # Percentiles para rangos numéricos (aplican a todas las numéricas)
                c1, c2, c3 = st.columns(3)
                p_low = c1.slider("Percentil inferior (rango numérico)", 0.0, 20.0, 5.0, 0.5)
                p_high = c2.slider("Percentil superior (rango numérico)", 80.0, 100.0, 95.0, 0.5)
                max_cat = c3.slider("Máx. categorías 'permitidas' por columna", 5, 50, 20, 1)
                # Fechas: no futuras
                allow_future_dates = st.checkbox("Permitir fechas futuras", value=False)

            # ---- Reglas derivadas del CSV (genéricas) ----
            reglas_csv = []

            # 1) No nulos por columna
            for col in df.columns:
                reglas_csv.append({
                    "name": f"{col}_not_null",
                    "description": f"{col} no debe ser nulo",
                    "condition": f"{col} IS NOT NULL",
                    "dimension": "Completitud"
                })

            # 2) Unicidad por columnas clave (si se configuran)
            if key_cols:
                reglas_csv.append({
                    "name": f"unique_key_{'_'.join(key_cols)}",
                    "description": f"Clave única basada en columnas: {', '.join(key_cols)}",
                    "condition": f"UNIQUE({', '.join(key_cols)})",
                    "dimension": "Unicidad"
                })

            # 3) Rangos por percentiles para cada columna numérica
            for col in numeric_cols:
                q_low = df[col].quantile(p_low / 100.0)
                q_high = df[col].quantile(p_high / 100.0)
                reglas_csv.append({
                    "name": f"{col}_range",
                    "description": f"{col} entre P{p_low:.1f}={q_low:.3f} y P{p_high:.1f}={q_high:.3f}",
                    "condition": f"{col} BETWEEN {q_low:.3f} AND {q_high:.3f}",
                    "dimension": "Validez"
                })
                reglas_csv.append({
                    "name": f"{col}_non_negative",
                    "description": f"{col} ≥ 0 (si aplica)",
                    "condition": f"{col} >= 0",
                    "dimension": "Validez"
                })

            # 4) Fechas no futuras
            for col in datetime_cols:
                reglas_csv.append({
                    "name": f"{col}_not_future",
                    "description": f"{col} no puede ser futura",
                    "condition": f"{col} <= CURRENT_DATE",
                    "dimension": "Validez"
                })

            # 5) Categóricas: lista de valores permitidos (top-N por frecuencia)
            for col in categorical_cols:
                # top-N categorías más frecuentes
                top_vals = df[col].value_counts(dropna=True).head(max_cat).index.tolist()
                reglas_csv.append({
                    "name": f"{col}_allowed_values",
                    "description": f"{col} dentro de las {len(top_vals)} categorías más frecuentes",
                    "condition": f"{col} IN {top_vals}",
                    "dimension": "Consistencia"
                })

            # ---- Métricas de calidad (genéricas) ----
            total_cells = n_rows * n_cols if n_rows and n_cols else 0

            # Completitud: % celdas no nulas
            completeness = (df.notna().sum().sum() / total_cells * 100.0) if total_cells > 0 else 0.0

            # Unicidad: si hay key_cols, % de filas con clave no nula y no duplicada
            if key_cols:
                keys_non_null = df[key_cols].notna().all(axis=1)
                # clave compuesta como tupla
                key_tuples = [tuple(x) for x in df[key_cols].values]
                unique_count = len(set(key_tuples))
                uniqueness = (unique_count / n_rows * 100.0) if n_rows > 0 else 0.0
                # integridad clave: filas con clave presente (no nula)
                integrity_key = keys_non_null.mean() * 100.0
            else:
                # sin clave definida: unicidad sobre fila completa
                uniqueness = (df.drop_duplicates().shape[0] / n_rows * 100.0) if n_rows > 0 else 0.0
                integrity_key = 0.0

            # Validez: promedio de cumplimiento de rangos numéricos + fechas no futuras
            validity_scores = []
            # numéricos
            for col in numeric_cols:
                q_low = df[col].quantile(p_low / 100.0)
                q_high = df[col].quantile(p_high / 100.0)
                mask_range = df[col].between(q_low, q_high, inclusive="both")
                mask_nonneg = df[col] >= 0
                # promedio de ambas
                validity_scores.append(mask_range.mean() * 100.0 if n_rows > 0 else 0.0)
                validity_scores.append(mask_nonneg.mean() * 100.0 if n_rows > 0 else 0.0)
            # fechas
            for col in datetime_cols:
                if allow_future_dates:
                    # todo válido
                    validity_scores.append(100.0)
                else:
                    mask_date = df[col] <= pd.Timestamp(date.today())
                    validity_scores.append(mask_date.mean() * 100.0 if n_rows > 0 else 0.0)
            validity = round(np.mean(validity_scores), 2) if validity_scores else 0.0

            # Consistencia: categóricas dentro del top-N
            consistency_scores = []
            for col in categorical_cols:
                top_vals = df[col].value_counts(dropna=True).head(max_cat).index.tolist()
                consistency_scores.append(df[col].isin(top_vals).mean() * 100.0 if n_rows > 0 else 0.0)
            consistency = round(np.mean(consistency_scores), 2) if consistency_scores else 0.0

            # Exactitud (proxy): valores numéricos dentro de IQR (por columna), promedio
            accuracy_scores = []
            for col in numeric_cols:
                q1 = df[col].quantile(0.25)
                q3 = df[col].quantile(0.75)
                iqr = q3 - q1
                low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
                accuracy_scores.append(df[col].between(low, high, inclusive="both").mean() * 100.0 if n_rows > 0 else 0.0)
            accuracy = round(np.mean(accuracy_scores), 2) if accuracy_scores else 0.0

            metricas_csv = {
                "Completitud": round(completeness, 2),
                "Unicidad": round(uniqueness, 2),
                "Consistencia": round(consistency, 2),
                "Validez": round(validity, 2),
                "Integridad Clave": round(integrity_key, 2),
                "Exactitud": round(accuracy, 2)
            }
            umbral_csv = 90

            # ---- Subpestañas para el CSV ----
            ctab1, ctab2, ctab3, ctab4, ctab5 = st.tabs(
                ["📋 Reglas CSV", "📊 Métricas CSV", "📈 Gráficos CSV", "⬇️ Descargar YAML CSV", "📂 Vista CSV"]
            )

            # --- Reglas CSV ---
            with ctab1:
                st.markdown('<p class="subtitle">Reglas generadas dinámicamente (CSV):</p>', unsafe_allow_html=True)
                st.table(reglas_csv)

            # --- Métricas CSV ---
            with ctab2:
                st.markdown('<p class="subtitle">Métricas de calidad calculadas (CSV):</p>', unsafe_allow_html=True)
                cols = st.columns(len(metricas_csv))
                for i, (k, v) in enumerate(metricas_csv.items()):
                    color = "normal" if v >= umbral_csv else "inverse"
                    estado = "✅" if v >= umbral_csv else "⚠️"
                    cols[i].metric(label=k, value=f"{v}% {estado}", delta="", delta_color=color)

            # --- Gráficos CSV ---
            with ctab3:
                st.markdown('<p class="subtitle">Visualización de métricas del CSV:</p>', unsafe_allow_html=True)
                fig_bar_csv = px.bar(
                    x=list(metricas_csv.keys()),
                    y=list(metricas_csv.values()),
                    color=list(metricas_csv.keys()),
                    title="Métricas de Calidad (CSV)",
                    labels={"x": "Dimensión", "y": "Porcentaje"}
                )
                st.plotly_chart(fig_bar_csv, use_container_width=True)

                fig_radar_csv = go.Figure()
                fig_radar_csv.add_trace(go.Scatterpolar(
                    r=list(metricas_csv.values()),
                    theta=list(metricas_csv.keys()),
                    fill='toself',
                    name='Calidad CSV'
                ))
                min_axis = max(0, min(metricas_csv.values()) - 10)
                fig_radar_csv.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[min_axis, 100])),
                    showlegend=False,
                    title="Radar de Calidad (CSV)"
                )
                st.plotly_chart(fig_radar_csv, use_container_width=True)

            # --- Descargar YAML CSV ---
            with ctab4:
                yaml_csv = {
                    "metadata": {
                        "company": "Bunge Global SA",
                        "generated_by": "DQaaS Streamlit App",
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "source_system": "CSV Upload (auto)"
                    },
                    "dataset": {
                        "rows": int(n_rows),
                        "columns": int(n_cols),
                        "numeric_columns": numeric_cols,
                        "datetime_columns": datetime_cols,
                        "categorical_columns": categorical_cols,
                        "key_columns": key_cols
                    },
                    "rules": reglas_csv,
                    "quality_metrics": metricas_csv,
                    "parameters": {
                        "percentile_low": p_low,
                        "percentile_high": p_high,
                        "max_allowed_categories": max_cat,
                        "allow_future_dates": allow_future_dates
                    }
                }
                yaml_str_csv = yaml.dump(yaml_csv, allow_unicode=True, sort_keys=False)
                st.download_button(
                    label="Descargar reglas y métricas del CSV (YAML)",
                    data=yaml_str_csv,
                    file_name="csv_quality_profile.yaml",
                    mime="text/yaml"
                )

            # --- Vista CSV (con filtros opcionales) ---
            with ctab5:
                st.markdown('<p class="subtitle">Vista de datos del CSV (filtros dinámicos):</p>', unsafe_allow_html=True)

                with st.expander("🔎 Filtros"):
                    # Filtros por cada tipo detectado
                    # Categóricos: multiselect por columna
                    filter_vals = {}
                    if categorical_cols:
                        st.markdown("**Categóricas**")
                        for col in categorical_cols:
                            options = sorted(df[col].dropna().unique().tolist())
                            filter_vals[col] = st.multiselect(f"{col}", options)

                    # Numéricas: rango por columna (hasta 5 primeras para no saturar UI)
                    if numeric_cols:
                        st.markdown("**Numéricas**")
                        for col in numeric_cols[:5]:
                            mn = float(df[col].min())
                            mx = float(df[col].max())
                            filter_vals[col] = st.slider(f"{col} (rango)", mn, mx, (mn, mx))

                    # Texto libre
                    search_text = st.text_input("Buscar texto en todas las columnas (contiene)", "")

                dff = df.copy()
                # Aplica filtros categóricos
                for col in categorical_cols:
                    vals = filter_vals.get(col)
                    if vals:
                        dff = dff[dff[col].isin(vals)]
                # Aplica filtros numéricos (solo si slider presente)
                for col in numeric_cols[:5]:
                    rng = filter_vals.get(col)
                    if isinstance(rng, tuple):
                        dff = dff[(dff[col] >= rng[0]) & (dff[col] <= rng[1])]
                # Búsqueda libre (en columnas de texto)
                if search_text:
                    mask_any = pd.Series(False, index=dff.index)
                    text_cols = dff.select_dtypes(include=["object", "category"]).columns
                    for col in text_cols:
                        mask_any = mask_any | dff[col].astype(str).str.contains(search_text, case=False, na=False)
                    dff = dff[mask_any]

                st.caption(f"Filas mostradas: {len(dff):,} de {len(df):,}")
                # Ordena por la primera datetime si existe
                sort_col = datetime_cols[0] if datetime_cols else None
                if sort_col:
                    dff = dff.sort_values(by=sort_col, ascending=False)
                st.dataframe(dff, use_container_width=True, height=520)

        except Exception as e:
            st.error(f"Error procesando el CSV: {e}")
            st.info("Prueba con un CSV válido. La app soporta esquemas arbitrarios y perfila columnas numéricas, de fecha y categóricas automáticamente.")

    # ==========================
    # Footer
    # ==========================
    st.markdown('<footer>© 2025 Bunge Global SA - Todos los derechos reservados</footer>', unsafe_allow_html=True)
