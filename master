import streamlit as st
import pandas as pd
import numpy as np

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
