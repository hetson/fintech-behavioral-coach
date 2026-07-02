import streamlit as st
from agent import procesar_mensaje_coach

# Configuración de la página web
st.set_page_config(page_title="Nudge AI", page_icon="🦉", layout="centered")

# Encabezado
st.title("🦉 Nudge AI")
st.subheader("Tu Coach Financiero Conductual")
st.markdown("---")

# Inicializar el historial de chat en la memoria de la sesión
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []
    # Mensaje de bienvenida inicial
    st.session_state.mensajes.append({
        "rol": "assistant", 
        "contenido": "¡Hola! Soy Nudge AI. Estoy aquí para escucharte y ayudarte a tomar decisiones financieras más tranquilas y conscientes. ¿Cómo te sientes hoy respecto a tus finanzas?"
    })

# Mostrar el historial de mensajes en la pantalla
for msg in st.session_state.mensajes:
    with st.chat_message(msg["rol"]):
        st.markdown(msg["contenido"])

# Caja de texto para que el usuario escriba
if prompt := st.chat_input("Escribe tu mensaje aquí (ej. 'Tuve un mal día, quiero comprar ropa')..."):
    
    # 1. Mostrar lo que el usuario escribió
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 2. Guardarlo en el historial
    st.session_state.mensajes.append({"rol": "user", "contenido": prompt})
    
    # 3. Mostrar el indicador de "Pensando..." mientras RAG y Gemini trabajan
    with st.chat_message("assistant"):
        with st.spinner("Analizando tu situación y consultando la literatura conductual..."):
            # ¡Llamamos a nuestro potente backend!
            respuesta_ia = procesar_mensaje_coach(prompt)
            st.markdown(respuesta_ia)
            
    # 4. Guardar la respuesta de la IA en el historial
    st.session_state.mensajes.append({"rol": "assistant", "contenido": respuesta_ia})