import streamlit as st
import ollama
import uuid


st.set_page_config(page_title="Chatbot con Ollama", page_icon="🤖")

if "chats" not in st.session_state:
    st.session_state.chats = {}

if "chat_id" not in st.session_state:
    st.session_state.chat_id = None

user_input = st.text_input("Tú:", placeholder="Escribe aquí...")
send_button = st.button("Enviar")

if send_button and user_input:
    if not st.session_state.chat_id and not st.query_params.get("chat", None):
        chat_id = str(uuid.uuid4())
        st.session_state.chat_id = chat_id
        st.session_state.chats[chat_id] = [{"role": "system", "content": "Eres un chatbot amigable y útil."}]

    chat_id = st.query_params.get("chat") if st.query_params.get("chat", None) else st.session_state.chat_id
    st.session_state.chats[chat_id].append({"role": "user", "content": user_input})

    response = ollama.chat(model="llama3.2:1b", messages=st.session_state.chats[chat_id])
    response_text = response["message"]["content"]

    st.session_state.chats[chat_id].append({"role": "assistant", "content": response_text})

    st.query_params.update({"chat": chat_id})
    st.rerun()

if st.session_state.chats:
    chat_id = st.query_params.get("chat", None)  
    if chat_id:
        for message in st.session_state.chats[chat_id]:
            if message["role"] == "user":
                st.markdown(f"**Tú:** {message['content']}")
            elif message["role"] == "assistant":
                st.markdown(f"**🤖 Chatbot:** {message['content']}")

st.sidebar.header("Chats Activos")
for chat in st.session_state.chats.keys():
    if chat:
        st.sidebar.button(f"Chat {chat[:8]}", on_click=lambda c=chat: st.query_params.update({"chat": c}))

def new_chat():
    st.session_state.chat_id = None
    st.query_params.clear()

st.sidebar.button("Nuevo Chat", on_click=new_chat)
