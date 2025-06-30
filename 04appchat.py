import streamlit as st
import openai
from PIL import Image

# Configurar página
st.set_page_config(page_title="Chatbot Colombiano", page_icon="🇨🇴")

# Mensaje de bienvenida
msg_chatbot = "¡Hola! Soy tu asistente colombiano 🇨🇴, pregúntame lo que necesites."

# 👉 Cargar clave desde secretos
try:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
except Exception as e:
    st.error("❌ No se encontró la clave OPENAI_API_KEY en Streamlit Cloud.")
    st.stop()

# Sidebar
with st.sidebar:
    st.title("🤖 Chatbot con OpenAI")
    try:
        st.image("openai.jpg", caption="OpenAI")
    except:
        pass
    st.markdown("Usando GPT-4o con dejo colombiano.")
    if st.button("🧹 Limpiar chat"):
        st.session_state.messages = [{"role": "assistant", "content": msg_chatbot}]

# Inicializar conversación
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": msg_chatbot}]

# Mostrar historial
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrada de usuario
prompt = st.chat_input("¿Qué quieres saber?")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Llamar a OpenAI
    with st.chat_message("assistant"):
        with st.spinner("Pensando un momentico..."):
            response = openai.ChatCompletion.create(
                model="gpt-4o",  # o "gpt-3.5-turbo" si no tienes acceso
                messages=[
                    {"role": "system", "content": "Eres un asistente colombiano, amable, con expresiones como 'parce', 'chévere' y 'bacano'."},
                    *st.session_state.messages
                ],
                temperature=0.7,
                max_tokens=400
            )
            full_response = response.choices[0].message.content
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
