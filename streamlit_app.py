import streamlit as st
import yaml
import random
from datetime import datetime
import base64



# ==========================
# Configuración de la página
# ==========================
st.set_page_config(
    page_title="DQaaS - Bunge Global SA",
    page_icon="🌐",
    layout="wide"
)



def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

logo_base64 = get_base64_image("image.png")

st.markdown(f"""
    <div style="display: flex; align-items: center; justify-content: center; gap: 20px; margin-bottom: 20px;">
        <img src="data:image/png;base64,{logo_base64}" width="180">
        <h1 style="color: #004C97; font-size: 48px; font-weight: bold; margin: 0;">DQaaS - Data Quality as a Service</h1>
    </div>
""", unsafe_allow_html=True)

# ==========================
# Encabezado con logo y título
# ==========================
st.markdown("""
    <div style="display: flex; align-items: center; justify-content: center; gap: 20px; margin-bottom: 20px;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Bunge_logo.svg/512px-Bunge_logo.svg.png" width="180">
        <h1 style="color: #004C97; font-size: 48px; font-weight: bold; margin: 0;">DQaaS - Data Quality as a Service</h1>
    </div>
    <p style="text-align: center; color: #003366; font-size: 22px; font-weight: bold;">
        Bunge Global SA - Viterra Data Products Squad Extension
    </p>
""", unsafe_allow_html=True)

# ==========================
# Estilos personalizados (estilo Bunge)
# ==========================
st.markdown("""
    <style>
        .stApp {
            background-color: #FFFFFF !important;
            color: #003366 !important;
            font-family: 'Open Sans', sans-serif;
        }
        .title {
            color: #004C97;
            font-size: 48px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 10px;
        }
        .subtitle {
            color: #003366;
            font-size: 22px;
            font-weight: bold;
            margin-top: 20px;
        }
        .stButton>button {
            background-color: #004C97;
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 18px;
            border: none;
        }
        .stButton>button:hover {
            background-color: #003366;
        }
        footer {
            text-align: center;
            color: #666666;
            font-size: 14px;
            margin-top: 40px;
        }
    </style>
""", unsafe_allow_html=True)

# ==========================
# Encabezado con logo y título
# ==========================
st.image("https://www.bunge.com/themes/custom/bunge/logo.svg", width=180)
st.markdown('<p class="title">DQaaS - Data Quality as a Service</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Bunge Global SA - Viterra Data Products Squad Extension</p>', unsafe_allow_html=True)

# ==========================
# Sidebar para navegación
# ==========================
st.sidebar.header("Opciones")
st.sidebar.info("Selecciona la tabla y genera reglas de calidad en formato Bunge YAML.")

# ==========================
# Simulación de conexión GCP
# ==========================
if st.sidebar.button("Conectar a GCP"):
    st.sidebar.success("Conexión simulada con BigQuery ✅")

# ==========================
# Selección de tabla
# ==========================
st.markdown('<p class="subtitle">Selecciona una tabla para generar reglas y métricas:</p>', unsafe_allow_html=True)
tablas_disponibles = ["clientes", "ventas", "productos", "proveedores", "pedidos"]
tabla_seleccionada = st.selectbox("", tablas_disponibles)

# ==========================
# Reglas por tabla
# ==========================
reglas_por_tabla = {
    "clientes": [
        {"name": "no_null_id", "description": "ID no debe ser nulo", "condition": "id IS NOT NULL", "dimension": "Completitud"},
        {"name": "email_format", "description": "Formato de email válido", "condition": "email LIKE '%@%'", "dimension": "Consistencia"},
        {"name": "age_range", "description": "Edad entre 18 y 99", "condition": "age BETWEEN 18 AND 99", "dimension": "Validez"}
    ],
    "ventas": [
        {"name": "positive_amount", "description": "Monto positivo", "condition": "amount > 0", "dimension": "Validez"},
        {"name": "valid_currency", "description": "Moneda válida (USD/EUR)", "condition": "currency IN ('USD','EUR')", "dimension": "Consistencia"},
        {"name": "date_not_future", "description": "Fecha no puede ser futura", "condition": "sale_date <= CURRENT_DATE", "dimension": "Validez"}
    ],
    "productos": [
        {"name": "unique_code", "description": "Código único", "condition": "code IS UNIQUE", "dimension": "Unicidad"},
        {"name": "price_positive", "description": "Precio mayor que cero", "condition": "price > 0", "dimension": "Validez"},
        {"name": "category_not_null", "description": "Categoría no nula", "condition": "category IS NOT NULL", "dimension": "Completitud"}
    ],
    "proveedores": [
        {"name": "country_valid", "description": "País válido (ISO)", "condition": "country IN ('ES','US','BR')", "dimension": "Consistencia"},
        {"name": "contact_email", "description": "Email de contacto válido", "condition": "contact_email LIKE '%@%'", "dimension": "Consistencia"},
        {"name": "id_unique", "description": "ID único", "condition": "id IS UNIQUE", "dimension": "Unicidad"}
    ],
    "pedidos": [
        {"name": "status_valid", "description": "Estado válido (PENDIENTE, COMPLETADO)", "condition": "status IN ('PENDIENTE','COMPLETADO')", "dimension": "Consistencia"},
        {"name": "delivery_date_check", "description": "Fecha de entrega >= fecha pedido", "condition": "delivery_date >= order_date", "dimension": "Validez"},
        {"name": "quantity_positive", "description": "Cantidad mayor que cero", "condition": "quantity > 0", "dimension": "Validez"}
    ]
}

# ==========================
# Datos de prueba alineados con Bunge
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
proveedores_data = [
    {"id": 301, "name": "Logística Global", "country": "BR", "contact_email": "logistica@global.com"},
    {"id": 302, "name": "TransAgro", "country": "US", "contact_email": "info@transagro.com"},
    {"id": 303, "name": "Puertos del Sur", "country": "ES", "contact_email": "puertos@sur.com"}
]
pedidos_data = [
    {"id": 401, "status": "PENDIENTE", "order_date": "2025-11-10", "delivery_date": "2025-11-25", "quantity": 500},
    {"id": 402, "status": "COMPLETADO", "order_date": "2025-11-05", "delivery_date": "2025-11-15", "quantity": 1200},
    {"id": 403, "status": "PENDIENTE", "order_date": "2025-11-12", "delivery_date": "2025-11-28", "quantity": 800}
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

# ==========================
# Pestañas para organización
# ==========================
tab1, tab2, tab3, tab4 = st.tabs(["📋 Reglas", "📊 Métricas", "⬇️ Descargar YAML", "📂 Datos de prueba"])

with tab1:
    st.markdown('<p class="subtitle">Reglas para la tabla seleccionada:</p>', unsafe_allow_html=True)
    st.table(reglas_por_tabla[tabla_seleccionada])

with tab2:
    st.markdown('<p class="subtitle">Métricas de calidad:</p>', unsafe_allow_html=True)
    cols = st.columns(len(metricas))
    for i, (k, v) in enumerate(metricas.items()):
        cols[i].metric(label=k, value=f"{v}%")

with tab3:
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

with tab4:
    st.markdown(f"**Datos de la tabla {tabla_seleccionada}:**")
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
