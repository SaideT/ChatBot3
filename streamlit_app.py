import streamlit as st
from openai import AsyncOpenAI
import asyncio
import pinecone
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import Pinecone
import copy

st.set_page_config(page_title="TaxPro 2023", page_icon="🦙", layout="centered", initial_sidebar_state="auto", menu_items=None)
st.title("Chat with TaxPro 2023, powered by GPT-3.5 Turbo")

# Sidebar for entering OpenAI key
with st.sidebar:
    st.title('Enter OpenAI API key here:')
    if 'openai_key' in st.secrets:
        st.success('OpenAI key already provided!', icon='✅')
        openai_key = st.secrets['openai_key']
    else:
        openai_key = st.text_input('Enter OpenAI API key here:', type='password', label_visibility="collapsed")
        if not openai_key:
            st.warning('Please enter your OpenAI key!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')

# Store chat messages, and initialize the chat message history
if 'messages' not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "I am TaxPro 2022. Ask me a question for your 2022 tax filing!"}]

# Display the prior chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"].replace("$","\$"))

# Define a function to get the GPT-3.5-turbo's response
if 'get_assistant_response' not in st.session_state:
    async def async_get_assistant_response(messages):
        client = AsyncOpenAI(api_key=openai_key)
        result = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        response = result.choices[0].message.content
        return response
    def get_assistant_response(messages):
        return asyncio.run(async_get_assistant_response(messages))
    st.session_state.get_assistant_response = get_assistant_response

if 'vectorestore' not in st.session_state:
    # Connect to pinecone database
    pinecone.init(api_key=st.secrets['pinecone_key'], environment=st.secrets['pinecone_environment'])
    index = pinecone.Index(st.secrets['index_name'])
    # Set embedding model and vectors DB, need to be used for embedding users' prompts and information retrieval from the pinecone database
    if 'embedding_model' not in st.session_state:
        st.session_state.embedding_model = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    st.session_state.vectorstore = Pinecone(index, st.session_state.embedding_model.embed_query, 'text')

# User-provided prompt
if prompt := st.chat_input(disabled=not openai_key):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt.replace("$","\$"))

# If the last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Retrieve similar chuncks from the pinecone database
            retrieved_chunks = st.session_state.vectorstore.similarity_search(st.session_state.messages[-1]["content"], k=3)
            # Concatenate the retrieved chunks to the user prompt
            context = "\n".join([chunk.page_content for chunk in retrieved_chunks])
            rag_prompt = f'''You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. 
If you don't know the answer, just say that you don't know. Keep the answer concise.

Context:
{context}

Question:
{st.session_state.messages[-1]["content"]}

Answer:'''
            # Replace the original prompt with the concatenated RAG prompt
            new_messages = copy.deepcopy(st.session_state.messages)[-10:]
            new_messages[-1]["content"] = rag_prompt
            # Get the GPT-3.5's response
            response = st.session_state.get_assistant_response(new_messages)
            st.write(response.replace("$","\$"))
    # Add response to chat messages
    st.session_state.messages.append({"role": "assistant", "content": response}) # Add response to message history
