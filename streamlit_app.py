import streamlit as st
import pandas as pd
import yaml

# ==========================
# Configuración de la página
# ==========================
st.set_page_config(
    page_title="DQaaS - Bunge Global SA",
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
            color: #002244; /* Azul más oscuro */
            font-size: 36px;
            font-weight: bold;
        }}
        .subtitle {{
            color: #333333; /* Gris oscuro */
            font-size: 20px;
            font-weight: bold;
        }}
        .stButton>button {{
            background-color: {bunge_primary};
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
        }}
        .stButton>button:hover {{
            background-color: #003366;
        }}
        body, .stMarkdown, .stText {{
            color: #000000; /* Texto negro para contenido */
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
# Selección de fuente de datos
# ==========================
st.write("### Selecciona la fuente de datos para generar el perfil:")
opciones_fuente = ["Subir archivo CSV", "Subir archivo Excel"]
fuente = st.selectbox("Fuente de datos:", opciones_fuente)

df = None
if fuente == "Subir archivo CSV":
    archivo = st.file_uploader("Carga tu archivo CSV", type=["csv"])
    if archivo:
        df = pd.read_csv(archivo)
elif fuente == "Subir archivo Excel":
    archivo = st.file_uploader("Carga tu archivo Excel", type=["xlsx"])
    if archivo:
        df = pd.read_excel(archivo)

# ==========================
# Data Profiling
# ==========================
if df is not None:
    st.subheader("Vista previa de los datos")
    st.dataframe(df.head())

    # Generar perfil básico
    perfil = {
        "filas": df.shape[0],
        "columnas": df.shape[1],
        "columnas_info": {}
    }

    for col in df.columns:
        perfil["columnas_info"][col] = {
            "tipo": str(df[col].dtype),
            "nulos": int(df[col].isnull().sum()),
            "únicos": int(df[col].nunique())
        }

    st.subheader("Perfil de datos")
    st.json(perfil)

    # Convertir a YAML
    yaml_content = yaml.dump(perfil, allow_unicode=True)

    # Botón para descargar
    st.download_button(
        label="Descargar perfil en YAML",
        data=yaml_content,
        file_name="data_profiling.yaml",
        mime="text/yaml"
    )

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
