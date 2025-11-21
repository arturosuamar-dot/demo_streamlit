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
if st.sidebar.button("Conectar a GCP"):
    st.sidebar.success("Conexión simulada con BigQuery ✅")

# ==========================
# Selección de tabla
# ==========================
st.markdown('<p style="color:#003366;font-size:22px;font-weight:bold;">Selecciona una tabla para generar reglas y métricas:</p>', unsafe_allow_html=True)
tablas_disponibles = ["clientes", "ventas", "productos", "proveedores", "pedidos"]
tabla_seleccionada = st.selectbox("", tablas_disponibles)

# ==========================
# Reglas más específicas
# ==========================
reglas_por_tabla = {
    "clientes": [
        {"name": "no_null_id", "description": "ID no debe ser nulo", "condition": "id IS NOT NULL", "dimension": "Completitud"},
        {"name": "email_format", "description": "Formato de email válido", "condition": "email LIKE '%@%'", "dimension": "Consistencia"},
        {"name": "age_range", "description": "Edad entre 18 y 99", "condition": "age BETWEEN 18 AND 99", "dimension": "Validez"}
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
        {"name": "id_unique", "description": "ID único", "condition": "id IS UNIQUE", "dimension": "Unicidad"}
    ],
    "pedidos": [
        {"name": "status_valid", "description": "Estado válido (PENDIENTE, COMPLETADO)", "condition": "status IN ('PENDIENTE','COMPLETADO')", "dimension": "Consistencia"},
        {"name": "delivery_date_check", "description": "Fecha entrega >= fecha pedido", "condition": "delivery_date >= order_date", "dimension": "Validez"},
        {"name": "quantity_min", "description": "Cantidad mínima 100 toneladas", "condition": "quantity >= 100", "dimension": "Validez"}
    ]
}

# ==========================
# Datos más cercanos al negocio
# ==========================
clientes_data = [
    {"id": 101, "nombre": "Agroexport SA", "email": "contacto@agroexport.com", "age": 45},
    {"id": 102, "nombre": "Granos del Sur", "email": "ventas@granosur.com", "age": 38},
    {"id": 103, "nombre": "Bunge Brasil", "email": "info@bunge.com.br", "age": 50}
]
ventas_data = [
    {"id": 201, "amount": 150000, "currency": "USD", "sale_date": "2025-11-15"},
    {"id": 202, "amount": 98000, "currency": "EUR", "sale_date": "2025-11-18"},
    {"id": 203, "amount": 250000, "currency": "USD", "sale_date": "2025-11-20"}
]
productos_data = [
    {"code": "SOY2025", "name": "Soja Premium", "price": 520, "category": "Oleaginosas"},
    {"code": "MAIZ2025", "name": "Maíz Amarillo", "price": 320, "category": "Cereales"},
    {"code": "TRIGO2025", "name": "Trigo Pan", "price": 410, "category": "Cereales"}
]

# ==========================
# Función para métricas con umbral
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
umbral = 90  # Umbral para indicadores

# ==========================
# Pestañas
# ==========================
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Reglas", "📊 Métricas", "📈 Gráficos", "⬇️ Descargar YAML", "📂 Datos de prueba"])

# --- Reglas ---
with tab1:
    st.markdown('<p class="subtitle">Reglas para la tabla seleccionada:</p>', unsafe_allow_html=True)
    st.table(reglas_por_tabla[tabla_seleccionada])

# --- Métricas con indicadores ---
with tab2:
    st.markdown('<p class="subtitle">Métricas de calidad:</p>', unsafe_allow_html=True)
    cols = st.columns(len(metricas))
    for i, (k, v) in enumerate(metricas.items()):
        if v >= umbral:
            delta = 1  # flecha hacia arriba
            color = "normal"  # verde
        else:
            delta = -1  # flecha hacia abajo
            color = "inverse"  # rojo
        cols[i].metric(label=k, value=f"{v}%", delta=delta, delta_color=color)


# --- Gráficos dinámicos ---
with tab3:
    st.markdown('<p class="subtitle">Visualización de métricas:</p>', unsafe_allow_html=True)
    # Gráfico de barras
    fig_bar = px.bar(x=list(metricas.keys()), y=list(metricas.values()), color=list(metricas.keys()),
                     title="Métricas de Calidad", labels={"x": "Dimensión", "y": "Porcentaje"})
    st.plotly_chart(fig_bar, use_container_width=True)

    # Gráfico radar
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=list(metricas.values()),
        theta=list(metricas.keys()),
        fill='toself',
        name='Calidad'
    ))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[70, 100])),
                            showlegend=False, title="Radar de Calidad")
    st.plotly_chart(fig_radar, use_container_width=True)

# --- Descargar yaml ---
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
    st.markdown(f"**Datos de la tabla {tabla_seleccionada}:**")
    if tabla_seleccionada == "clientes":
        st.table(clientes_data)
    elif tabla_seleccionada == "ventas":
        st.table(ventas_data)
    elif tabla_seleccionada == "productos":
        st.table(productos_data)

# ==========================
# Footer
# ==========================
st.markdown('<footer>© 2025 Bunge Global SA - Todos los derechos reservados</footer>', unsafe_allow_html=True)
