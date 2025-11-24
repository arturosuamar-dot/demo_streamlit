
import streamlit as st
import yaml
import random
from datetime import datetime
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
# Estilos globales
# ==========================
st.markdown("""
    <style>
    /* Centra TODOS los st.button de la página */
    div.stButton {
        display: flex;
        justify-content: center;
    }
    /* Estilo del botón */
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

    /* Subtítulo reutilizable */
    .subtitle {
        font-size: 24px;
        font-weight: bold;
        color: #004C97;
        margin-bottom: -10px;
    }

    /* Footer */
    footer {
        text-align: center;
        color: #6b6b6b;
        margin-top: 40px;
    }

    /* Opcional: reduce padding superior del contenedor principal para un look más centrado */
    .block-container {
        padding-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================
# Pantalla inicial
# ==========================
if not st.session_state.perfilado_iniciado:
    # Portada con logo, título y subtítulo
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

    # Espaciado bajo el título
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # Botón (queda centrado por el CSS anterior)
    if st.button("🚀 Iniciar Perfilado de Datos", key="start_button"):
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
    # Función para métricas
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
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Reglas", "📊 Métricas", "📈 Gráficos", "⬇️ Descargar YAML", "📂 Datos de prueba"])

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

    # ==========================
    # Footer
    # ==========================
    st.markdown('<footer>© 2025 Bunge Global SA - Todos los derechos reservados</footer>', unsafe_allow_html=True)
