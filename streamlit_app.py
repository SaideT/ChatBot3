import streamlit as st
import openai

st.set_page_config(page_title="Chat with the Tax Assistant 2022, powered by GPT3.5", page_icon="🦙", layout="centered", initial_sidebar_state="auto", menu_items=None)
st.title("Chat with the Tax Assistant 2022, powered by GPT3.5")

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

# User-provided prompt
if prompt := st.chat_input(disabled=not openai_key):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)






