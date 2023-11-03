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
    st.session_state.messages = [{"role": "assistant", "content": "Ask me any questions"}]

# User-provided prompt
if prompt := st.chat_input(disabled=not openai_key):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

openai.api_key = openai_key

# Function to get the GPT3.5's response
def get_assistant_response(allmessages):
    r = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": m["role"], "content": m["content"]} for m in allmessages],
    )
    response = r.choices[0].message.content
    return response

# Display the prior chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

