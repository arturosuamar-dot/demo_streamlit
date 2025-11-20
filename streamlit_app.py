import streamlit as st
import pandas as pd
import numpy as np
import yaml # Provisional

st.title("Mi primera app con Streamlit")
st.write("¡Hola, Streamlit está funcionando!")

# Entrada de texto
nombre = st.text_input("Escribe tu nombre:")
if nombre:
    st.success(f"Hola, {nombre} 👋")

# Gráfico simple
st.subheader("Gráfico aleatorio")
data = pd.DataFrame(np.random.randn(20, 3), columns=["A", "B", "C"])
st.line_chart(data)




# Ejemplo yaml

# data puede ser cualquier estructura Python (diccionario, lista, etc.).
# yaml.dump() convierte el objeto en texto YAML.
# mime="text/yaml" indica el tipo de archivo.
# file_name define el nombre del archivo descargado.

# Datos de ejemplo
data = {
    "nombre": "Arturo",
    "rol": "Data Architecture Associate",
    "ubicación": "La Coruña"
}

# Convertir a YAML
yaml_content = yaml.dump(data, allow_unicode=True)

# Crear botón de descarga
st.download_button(
    label="Descargar YAML",
    data=yaml_content,
    file_name="configuracion.yaml",
    mime="text/yaml"
)
