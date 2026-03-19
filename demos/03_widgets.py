import streamlit as st

st.title("Widgets de entrada")

# Text input
nombre = st.text_input("¿Cómo te llamas?", value="Mundo")
st.write(f"¡Hola, **{nombre}**!")

# Slider
edad = st.slider("Selecciona tu edad", min_value=0, max_value=120, value=25)
st.write(f"Tienes **{edad}** años.")

# Selectbox
color = st.selectbox("¿Cuál es tu color favorito?", ["Rojo", "Azul", "Verde", "Amarillo"])
st.write(f"Tu color favorito es **{color}**.")

# Multiselect
frutas = st.multiselect(
    "¿Qué frutas te gustan?",
    ["Manzana", "Plátano", "Naranja", "Fresa", "Mango"],
    default=["Manzana"],
)
st.write(f"Seleccionaste: {', '.join(frutas) if frutas else 'ninguna'}")

# Checkbox
if st.checkbox("Mostrar mensaje secreto"):
    st.success("¡Has descubierto el mensaje secreto! 🎉")

# Number input
numero = st.number_input("Introduce un número", min_value=0, max_value=1000, value=42)
st.write(f"El doble de {numero} es **{numero * 2}**.")

# Radio
opcion = st.radio("¿Café o té?", ["Café ☕", "Té 🍵"])
st.write(f"Elegiste: {opcion}")

# Button
if st.button("Haz clic aquí"):
    st.balloons()
    st.write("¡Clic registrado!")
