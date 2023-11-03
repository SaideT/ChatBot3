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

if "messages" not in st.session_state.keys():
    counter = 0
    with st.chat_message("assistant"):
        st.write(counter)

# User-provided prompt
if prompt := st.chat_input(disabled=not openai_key):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)






