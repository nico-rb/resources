import streamlit as st

st.title("Formularios")

st.write("Los cambios en estos campos NO provocan re-ejecución hasta pulsar 'Enviar'.")

with st.form("mi_formulario"):
    nombre = st.text_input("Nombre")
    email = st.text_input("Email")
    edad = st.slider("Edad", 18, 99, 25)
    tema = st.selectbox("Tema de interés", ["Python", "Data Science", "Web", "ML/AI"])
    acepta = st.checkbox("Acepto los términos y condiciones")

    # El botón submit es obligatorio dentro de un form
    enviado = st.form_submit_button("Enviar")

if enviado:
    if not nombre or not email:
        st.error("Por favor, rellena nombre y email.")
    elif not acepta:
        st.warning("Debes aceptar los términos y condiciones.")
    else:
        st.success(f"¡Formulario enviado!")
        st.write(f"- **Nombre:** {nombre}")
        st.write(f"- **Email:** {email}")
        st.write(f"- **Edad:** {edad}")
        st.write(f"- **Tema:** {tema}")
