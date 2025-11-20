import streamlit as st
import yaml

# ==========================

st.set_page_config(
    page_title="Mi App",
    page_icon="🌐",  # Configuración de la página
    layout="wide"
)

# ==========================
# Estilos personalizados (colores Bunge)
# ==========================
bunge_primary = "#004C97"   # Azul corporativo
bunge_secondary = "#F4B41A" # Amarillo corporativo
bunge_bg = "#F9F9F9"

st.markdown(f"""
    <style>
        .stApp {{
            background-color: {bunge_bg};
        }}
        .title {{
            color: {bunge_primary};
            font-size: 36px;
            font-weight: bold;
        }}
        .subtitle {{
            color: {bunge_secondary};
            font-size: 20px;
            font-weight: bold;
        }}
        .stButton>button {{
            background-color: {bunge_primary};
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
        }}
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
# Reglas de Calidad del Dato
# ==========================
st.write("### Selecciona el tipo de reglas de calidad:")

reglas = {
    "Completitud": [
        "Todos los campos obligatorios deben estar presentes",
        "No se permiten valores nulos en campos clave"
    ],
    "Consistencia": [
        "Formato de fecha debe ser YYYY-MM-DD",
        "Valores numéricos deben coincidir con el rango definido"
    ],
    "Unicidad": [
        "No debe haber duplicados en el identificador principal"
    ]
}

opcion = st.radio("Tipo de regla:", list(reglas.keys()))

if st.button("Mostrar reglas"):
    st.write(f"**Reglas para {opcion}:**")
    for regla in reglas[opcion]:
        st.write(f"- {regla}")

    # Convertir a YAML
    yaml_content = yaml.dump({opcion: reglas[opcion]}, allow_unicode=True)

    # Botón de descarga
    st.download_button(
        label="Descargar reglas en YAML",
        data=yaml_content,
        file_name=f"reglas_{opcion.lower()}.yaml",
        mime="text/yaml"
    )
# ==========================
st.set_page_config(
    page_title="DQaaS - Bunge Global SA",




# Ejemplo yaml

# data puede ser cualquier estructura Python (diccionario, lista, etc.).
# yaml.dump() convierte el objeto en texto YAML.
# mime="text/yaml" indica el tipo de archivo.
# file_name define el nombre del archivo descargado.

# Datos de ejemplo
#data = {
#    "nombre": "Arturo",
#    "rol": "Data Architecture Associate",
#    "ubicación": "La Coruña"
#}

# Convertir a YAML
#yaml_content = yaml.dump(data, allow_unicode=True)

# Crear botón de descarga
#st.download_button(
#    label="Descargar YAML",
#    data=yaml_content,
#    file_name="configuracion.yaml",
#    mime="text/yaml"
#)
