import streamlit as st
import ollama
import uuid


st.set_page_config(page_title="Chatbot con Ollama", page_icon="🤖")

if "chats" not in st.session_state:
    st.session_state.chats = {}

if "chat_id" not in st.session_state:
    st.session_state.chat_id = None

if "histories" not in st.session_state:
    st.session_state.histories = {}

if not st.session_state.chat_id and st.session_state.histories:
    st.session_state.chat_id = str(uuid.uuid4())

user_input = st.text_input("Tú:", placeholder="Escribe aquí...")
send_button = st.button("Enviar")

if send_button and user_input:
    if not st.session_state.chat_id and not st.query_params.get("chat", None):
        chat_id = str(uuid.uuid4())
        st.session_state.chat_id = chat_id
        st.session_state.chats[chat_id] = [{"role": "system", "content": "Eres un chatbot amigable y útil."}]

    chat_id = st.query_params.get("chat") if st.query_params.get("chat", None) else st.session_state.chat_id
    st.session_state.histories[chat_id] = []
    st.session_state.chats[chat_id].append({"role": "user", "content": user_input})

    response = ollama.chat(model="llama3.2:1b", messages=st.session_state.chats[chat_id])
    response_text = response["message"]["content"]

    st.session_state.chats[chat_id].append({"role": "assistant", "content": response_text})

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
    st.session_state.histories = {}
    st.query_params.clear()

st.sidebar.button("Nuevo Chat", on_click=new_chat)



# import streamlit as st
# import ollama
# import uuid  # Para generar IDs únicos

# st.set_page_config(page_title="Chatbot con Ollama", page_icon="🤖")

# # Obtener o generar un ID de chat
# query_params = st.query_params
# chat_id = query_params.get("chat", str(uuid.uuid4()))  # Si no hay chat_id, se genera uno nuevo

# # Guardar historial por ID de chat
# if "chats" not in st.session_state:
#     st.session_state.chats = {}

# if chat_id not in st.session_state.chats:
#     st.session_state.chats[chat_id] = [{"role": "system", "content": "Eres un chatbot experto."}]

# # Input del usuario
# user_input = st.text_input("Tú:", placeholder="Escribe aquí...")

# if st.button("Enviar") and user_input:
#     st.session_state.chats[chat_id].append({"role": "user", "content": user_input})
    
#     response = ollama.chat(model="llama3.2:1b", messages=st.session_state.chats[chat_id])
#     st.session_state.chats[chat_id].append({"role": "assistant", "content": response["message"]["content"]})

#     st.rerun()

# # Mostrar historial
# for message in st.session_state.chats[chat_id]:
#     if message["role"] == "user":
#         st.markdown(f"**Tú:** {message['content']}")
#     elif message["role"] == "assistant":
#         st.markdown(f"**🤖 Chatbot:** {message['content']}")

# # Mostrar chats activos en la sidebar
# st.sidebar.header("Chats Activos")
# for chat in st.session_state.chats.keys():
#     if chat:
#         st.sidebar.button(f"Chat {chat[:8]}", on_click=lambda c=chat: st.query_params.update({"chat": c}))

# st.sidebar.button("Nuevo Chat", on_click=lambda: st.query_params.update({"chat": str(uuid.uuid4())}))
