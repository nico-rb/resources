import streamlit as st

st.title("Session State: contador")

# Inicializar el estado si no existe
if "contador" not in st.session_state:
    st.session_state.contador = 0

st.write(f"Valor del contador: **{st.session_state.contador}**")

# Botones para modificar el estado
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("➕ Incrementar"):
        st.session_state.contador += 1
        st.rerun()  # Re-ejecuta para mostrar el nuevo valor

with col2:
    if st.button("➖ Decrementar"):
        st.session_state.contador -= 1
        st.rerun()

with col3:
    if st.button("🔄 Reiniciar"):
        st.session_state.contador = 0
        st.rerun()

# Mostrar todo el session_state
with st.expander("Ver st.session_state completo"):
    st.write(st.session_state)
