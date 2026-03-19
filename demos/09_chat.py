import streamlit as st

st.title("Chat simple (eco)")

# Inicializar historial de mensajes
if "mensajes" not in st.session_state:
    st.session_state.mensajes = [
        {"role": "assistant", "content": "¡Hola! Soy un bot eco. Repito todo lo que me dices."}
    ]

# Mostrar historial
for msg in st.session_state.mensajes:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input del usuario
if prompt := st.chat_input("Escribe un mensaje..."):
    # Añadir mensaje del usuario
    st.session_state.mensajes.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Respuesta del bot (eco)
    respuesta = f"Has dicho: *{prompt}*"
    st.session_state.mensajes.append({"role": "assistant", "content": respuesta})
    with st.chat_message("assistant"):
        st.write(respuesta)
