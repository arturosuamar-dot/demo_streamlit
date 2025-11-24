
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
            <h1 style="color: #004C97; font-size: 48px; font-weight: bold;">Bunge Global SA — Data Quality Service</h1>
            <p style="color: #003366; font-size: 22px; font-weight: bold;">
                For Viterra • Delivered by the Data Products Squad
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
            <h1 style="color: #004C97; font-size: 48px; font-weight: bold; margin: 0;">Bunge Global SA — Data Quality Service</h1>
            <p style="color: #003366; font-size: 22px; font-weight: bold; margin-top: 10px;">
                For Viterra • Delivered by the Data Products Squad
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
    # Select tabla
    # ==========================
    st.markdown('<p class="subtitle">Selecciona una tabla:</p>', unsafe_allow_html=True)
    tabla_visible = st.selectbox("", list(tablas_map.keys()))
    tabla_seleccionada = tablas_map[tabla_visible]

    # ==========================
    # Reglas por tabla
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
    # Datos ficticios coherentes
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
    # Función para métricas (tablas demo)
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
    # Pestañas (añadimos CSV adjunto)
    # ==========================
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        ["📋 Reglas", "📊 Métricas", "📈 Gráficos", "⬇️ Descargar YAML", "📂 Datos de prueba", "📄 CSV adjunto"]
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

    # --- Descargar YAML ---
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

    # ========= 📄 CSV adjunto: Reglas, Métricas, Gráficos, YAML, Datos =========
    with tab6:
        st.markdown('<p class="subtitle">CSV adjunto: reglas, métricas, gráficos y YAML</p>', unsafe_allow_html=True)

        import pandas as pd
        import numpy as np

        # ---- Carga del CSV ----
        csv_file = st.file_uploader("Sube un CSV con el mismo esquema (opcional)", type=["csv"], key="csv_uploader")
        def load_csv_to_df(uploaded) -> pd.DataFrame:
            if uploaded is not None:
                return pd.read_csv(uploaded)
            else:
                return pd.read_csv("global_agribusiness_food_company_1000_2.csv")

        try:
            df = load_csv_to_df(csv_file)

            # Tipado y limpieza
            expected_cols = ["ProductID","ProductName","Category","Region","Country","Supplier","UnitPrice","Currency","StockQuantity","LastUpdated"]
            missing = [c for c in expected_cols if c not in df.columns]
            if missing:
                st.error(f"El CSV no contiene columnas esperadas: {missing}")
                st.stop()

            df["LastUpdated"] = pd.to_datetime(df["LastUpdated"], errors="coerce")
            for col in ["UnitPrice", "StockQuantity", "ProductID"]:
                df[col] = pd.to_numeric(df[col], errors="coerce")
            for col in df.select_dtypes(include=["object"]).columns:
                df[col] = df[col].astype(str).str.strip()

            # ---- Definición/derivación de reglas desde el CSV ----
            allowed_currency = {"USD","EUR","INR"}
            allowed_regions  = {"North America","South America","Europe","Africa","Asia","Oceania"}

            # Rango sugerido de precio (puedes ajustar)
            min_rule_price, max_rule_price = 100, 2000

            reglas_csv = [
                {"name": "product_id_not_null", "description": "ProductID no debe ser nulo", "condition": "ProductID IS NOT NULL", "dimension": "Completitud"},
                {"name": "product_name_not_null", "description": "ProductName no debe ser nulo", "condition": "ProductName IS NOT NULL", "dimension": "Completitud"},
                {"name": "category_not_null", "description": "Category no debe ser nulo", "condition": "Category IS NOT NULL", "dimension": "Completitud"},
                {"name": "region_valid", "description": "Region válida", "condition": f"Region IN {sorted(list(allowed_regions))}", "dimension": "Consistencia"},
                {"name": "country_not_null", "description": "Country no debe ser nulo", "condition": "Country IS NOT NULL", "dimension": "Completitud"},
                {"name": "supplier_not_null", "description": "Supplier no debe ser nulo", "condition": "Supplier IS NOT NULL", "dimension": "Completitud"},
                {"name": "currency_valid", "description": "Moneda válida (USD, EUR, INR)", "condition": f"Currency IN {sorted(list(allowed_currency))}", "dimension": "Consistencia"},
                {"name": "unit_price_range", "description": f"UnitPrice entre {min_rule_price} y {max_rule_price}", "condition": f"UnitPrice BETWEEN {min_rule_price} AND {max_rule_price}", "dimension": "Validez"},
                {"name": "unit_price_positive", "description": "UnitPrice > 0", "condition": "UnitPrice > 0", "dimension": "Validez"},
                {"name": "stock_non_negative", "description": "StockQuantity ≥ 0", "condition": "StockQuantity >= 0", "dimension": "Validez"},
                {"name": "last_updated_not_future", "description": "LastUpdated no puede ser futura", "condition": "LastUpdated <= CURRENT_DATE", "dimension": "Validez"},
                {"name": "product_id_unique", "description": "ProductID único", "condition": "ProductID IS UNIQUE", "dimension": "Unicidad"},
            ]

            # ---- Cálculo de métricas de calidad sobre el CSV ----
            total_rows = len(df)

            # Completitud: % de valores no nulos sobre columnas críticas
            critical_cols = ["ProductID","ProductName","Category","Region","Country","Supplier","UnitPrice","Currency","StockQuantity","LastUpdated"]
            completeness = float(
                df[critical_cols].notna().sum().sum()
            ) / (len(df) * len(critical_cols)) * 100 if total_rows > 0 else 0.0

            # Unicidad: % de ProductID únicos
            uniqueness = df["ProductID"].nunique() / total_rows * 100 if total_rows > 0 else 0.0

            # Consistencia: Currency y Region dentro de listados permitidos
            consistency_mask = df["Currency"].isin(allowed_currency) & df["Region"].isin(allowed_regions)
            consistency = consistency_mask.mean() * 100 if total_rows > 0 else 0.0

            # Validez: reglas numéricas y de fecha
            today = pd.Timestamp(date.today())
            validity_mask = (
                (df["UnitPrice"] > 0) &
                (df["UnitPrice"].between(min_rule_price, max_rule_price, inclusive="both")) &
                (df["StockQuantity"] >= 0) &
                (df["LastUpdated"] <= today)
            )
            validity = validity_mask.mean() * 100 if total_rows > 0 else 0.0

            # Integridad referencial (simplificada): Supplier y Category presentes + ProductID no duplicado
            referential_mask = (
                df["Supplier"].notna() &
                df["Category"].notna()
            )
            referential = referential_mask.mean() * 100 if total_rows > 0 else 0.0

            # Exactitud (proxy): valores de UnitPrice dentro del IQR ampliado (Q1-1.5*IQR, Q3+1.5*IQR)
            if total_rows > 0 and df["UnitPrice"].notna().sum() > 0:
                q1 = df["UnitPrice"].quantile(0.25)
                q3 = df["UnitPrice"].quantile(0.75)
                iqr = q3 - q1
                low, high = q1 - 1.5*iqr, q3 + 1.5*iqr
                accuracy_mask = df["UnitPrice"].between(low, high, inclusive="both")
                accuracy = accuracy_mask.mean() * 100
            else:
                accuracy = 0.0

            metricas_csv = {
                "Completitud": round(completeness, 2),
                "Unicidad": round(uniqueness, 2),
                "Consistencia": round(consistency, 2),
                "Validez": round(validity, 2),
                "Integridad Referencial": round(referential, 2),
                "Exactitud": round(accuracy, 2)
            }
            umbral_csv = 90

            # ---- Subpestañas para el CSV ----
            ctab1, ctab2, ctab3, ctab4, ctab5 = st.tabs(
                ["📋 Reglas CSV", "📊 Métricas CSV", "📈 Gráficos CSV", "⬇️ Descargar YAML CSV", "📂 Vista CSV"]
            )

            # --- Reglas CSV ---
            with ctab1:
                st.markdown('<p class="subtitle">Reglas generadas para el CSV:</p>', unsafe_allow_html=True)
                st.table(reglas_csv)

            # --- Métricas CSV ---
            with ctab2:
                st.markdown('<p class="subtitle">Métricas de calidad calculadas sobre el CSV:</p>', unsafe_allow_html=True)
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
                # Ajusta el rango en función de las métricas observadas
                min_axis = max(0, min(metricas_csv.values()) - 10)
                max_axis = min(100, max(metricas_csv.values()) + 5)
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
                        "source_system": "CSV Upload"
                    },
                    "table": "agribusiness_products_csv",
                    "rules": reglas_csv,
                    "quality_metrics": metricas_csv,
                    "summary": {
                        "rows": int(total_rows),
                        "distinct_products": int(df["ProductID"].nunique())
                    }
                }
                yaml_str_csv = yaml.dump(yaml_csv, allow_unicode=True, sort_keys=False)
                st.download_button(
                    label="Descargar reglas y métricas del CSV en YAML",
                    data=yaml_str_csv,
                    file_name="agribusiness_products_csv_quality.yaml",
                    mime="text/yaml"
                )

            # --- Vista CSV (con filtros opcionales) ---
            with ctab5:
                st.markdown('<p class="subtitle">Vista de datos del CSV:</p>', unsafe_allow_html=True)

                with st.expander("🔎 Filtros"):
                    c1, c2, c3, c4, c5 = st.columns(5)
                    category = c1.multiselect("Category", sorted(df["Category"].dropna().unique().tolist()))
                    region = c2.multiselect("Region", sorted(df["Region"].dropna().unique().tolist()))
                    country = c3.multiselect("Country", sorted(df["Country"].dropna().unique().tolist()))
                    supplier = c4.multiselect("Supplier", sorted(df["Supplier"].dropna().unique().tolist()))
                    currency = c5.multiselect("Currency", sorted(df["Currency"].dropna().unique().tolist()))
                    search_text = st.text_input("Buscar (ProductName o Supplier)", "")
                    # slider de precios
                    min_price = float(df["UnitPrice"].min())
                    max_price = float(df["UnitPrice"].max())
                    price_range = st.slider("Rango UnitPrice", min_value=min_price, max_value=max_price,
                                            value=(min_price, max_price))

                dff = df.copy()
                if category: dff = dff[dff["Category"].isin(category)]
                if region: dff = dff[dff["Region"].isin(region)]
                if country: dff = dff[dff["Country"].isin(country)]
                if supplier: dff = dff[dff["Supplier"].isin(supplier)]
                if currency: dff = dff[dff["Currency"].isin(currency)]
                if search_text:
                    mask = (
                        dff["ProductName"].astype(str).str.contains(search_text, case=False, na=False) |
                        dff["Supplier"].astype(str).str.contains(search_text, case=False, na=False)
                    )
                    dff = dff[mask]
                dff = dff[(dff["UnitPrice"] >= price_range[0]) & (dff["UnitPrice"] <= price_range[1])]

                st.caption(f"Filas mostradas: {len(dff):,} de {len(df):,}")
                st.dataframe(
                    dff.sort_values(by="LastUpdated", ascending=False),
                    use_container_width=True,
                    height=520
                )

        except Exception as e:
            st.error(f"Error procesando el CSV: {e}")
            st.info("Verifica el esquema esperado: ProductID, ProductName, Category, Region, Country, Supplier, UnitPrice, Currency, StockQuantity, LastUpdated.")

    # ==========================
    # Footer
    # ==========================
    st.markdown('<footer>© 2025 Bunge Global SA - Todos los derechos reservados</footer>', unsafe_allow_html=True)
