import streamlit as st
import yaml
import random

# ==========================
# Configuración de la página
# ==========================
st.set_page_config(
    page_title="DQaaS - Bunge Global SA",
    page_icon="🌐",
    layout="wide"
)

# ==========================
# Estilos personalizados (modo oscuro)
# ==========================
st.markdown("""
    <style>
        .stApp {
            background-color: #000000; /* Fondo negro */
        }
        .title {
            color: #FFFFFF; /* Blanco */
            font-size: 48px; /* Más grande */
            font-weight: bold;
            text-align: center;
            margin-bottom: 20px;
        }
        .subtitle {
            color: #FFFFFF;
            font-size: 28px; /* Más grande que selectbox */
            font-weight: bold;
            margin-top: 10px;
        }
        .stSelectbox label {
            color: #FFFFFF !important; /* Texto blanco en selectbox */
            font-size: 20px;
        }
        .stMarkdown, .stText, .stJson, .stTable {
            color: #FFFFFF !important; /* Texto blanco en contenido */
        }
        .stButton>button {
            background-color: #004C97; /* Azul corporativo */
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 18px;
        }
        .stButton>button:hover {
            background-color: #003366;
        }
    </style>
""", unsafe_allow_html=True)

# ==========================
# Título
# ==========================
st.markdown('<p class="title">DQaaS - Data Quality as a Service</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Bunge Global SA - Viterra Data Products Squad Extension</p>', unsafe_allow_html=True)

# ==========================
# API Key simulada
# ==========================
st.sidebar.header("Configuración")
api_key = "BUNGE-AUTO-KEY-2025"
st.sidebar.success(f"API Key generada automáticamente: {api_key}")

# ==========================
# Selección de tabla simulada
# ==========================
st.markdown('<p class="subtitle">Selecciona una tabla para generar reglas y métricas:</p>', unsafe_allow_html=True)
tablas_disponibles = ["clientes", "ventas", "productos", "proveedores", "pedidos"]
tabla_seleccionada = st.selectbox("", tablas_disponibles)

# ==========================
# Reglas simuladas por tabla
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
# Métricas dinámicas variadas
# ==========================
def generar_metricas():
    return {
        "completitud": f"{random.randint(85, 99)}%",
        "unicidad": f"{random.randint(80, 98)}%",
        "consistencia": f"{random.randint(82, 97)}%",
        "validez": f"{random.randint(83, 96)}%",
        "integridad_referencial": f"{random.randint(75, 95)}%",
        "exactitud": f"{random.randint(78, 94)}%"
    }

metricas = generar_metricas()

# ==========================
# Mostrar reglas y métricas
# ==========================
st.markdown('<p class="subtitle">Reglas para la tabla seleccionada:</p>', unsafe_allow_html=True)
st.table(reglas_por_tabla[tabla_seleccionada])

st.markdown('<p class="subtitle">Métricas de calidad:</p>', unsafe_allow_html=True)
st.json(metricas)

# ==========================
# Generar YAML
# ==========================
yaml_data = {
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
