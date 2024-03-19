import os
import vertexai
import streamlit as st
from vertexai.preview import generative_models
from vertexai.preview.generative_models import (
    GenerativeModel,
    Part,
    Content,
    ChatSession,
)

from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()
key_path = os.environ["GCLOUD_SERVICE_ACCOUNT_KEY_PATH"]
credentials = Credentials.from_service_account_file(
    key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

PROJECT_ID = os.environ["PROJECT_ID"]  # Replace with your project ID

# Initialize Vertex AI SDK
vertexai.init(project=PROJECT_ID, credentials=credentials)
config = generative_models.GenerationConfig(temperature=0.4)

# Load model with config
model = GenerativeModel("gemini-pro", generation_config=config)
chat = model.start_chat()


# Helper function
def llm_function(chat: ChatSession, query):
    response = chat.send_message(query)
    output = response.candidates[0].content.parts[0].text

    with st.chat_message("model"):
        st.markdown(output)

    st.session_state.messages.append({"role": "user", "content": query})
    st.session_state.messages.append({"role": "model", "content": output})


st.title("Gemini Explorer")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display and load to chat history
for index, message in enumerate(st.session_state.messages):
    content = Content(role=message["role"], parts=[Part.from_text(message["content"])])

    if index != 0:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    chat.history.append(content)

# For initial message startup
if len(st.session_state.messages) == 0:
    llm_function(
        chat,
        "Introduce yourself as ReX, an assistant powered by Google Gemini. You use emojis to be interactive.",
    )

# Prompt the user to enter their name if it's not provided yet
if "user_name" not in st.session_state:
    user_name = st.text_input("Please enter your name")
    if user_name:
        st.session_state.user_name = user_name
        # Modify ReX's initial prompt to include the user's name
        initial_prompt = f"Hey, my name is {user_name}!"
        if len(st.session_state.messages) == 2:
            llm_function(chat, initial_prompt)

# For capture user input
query = st.chat_input("Gemini Explorer")

if query:
    with st.chat_message("user"):
        st.markdown(query)
    llm_function(chat, query)
