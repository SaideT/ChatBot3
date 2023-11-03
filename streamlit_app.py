import streamlit as st
import openai

# App title
st.set_page_config(page_title="Tax Assistant", page_icon="🦙", layout="centered", initial_sidebar_state="auto", menu_items=None)
st.title("Tax Assistant")

# Sidebar for entering OpenAI key
with st.sidebar:
    st.title('OpenAI key')
    openai_key = st.text_input('Enter OpenAI key:', type='password')
    if not openai_key:
        st.warning('Please enter your OpenAI key!', icon='⚠️')
    else:
        st.success('Proceed to entering your prompt message!', icon='👉')

 # Store chat messages, and initialize the chat message history
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Ask me a question about the 2022 tax return filing!"}]

openai.api_key = openai_key

# User-provided prompt
if prompt := st.chat_input(disabled=not openai_key):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# User-provided prompt
if prompt := st.chat_input(disabled=not openai_key):
    st.session_state.messages.append({"role": "user", "content": prompt})

# Display the prior chat messages
  
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        






