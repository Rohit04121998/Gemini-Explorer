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

# # Sending a Prompt and Receiving a Response
# prompt = "Once upon a time"
# response = chat.send_message(prompt)
# st.write("Generated Response:", response)

# # Sending Another Prompt
# prompt2 = "In a galaxy far, far away"
# response2 = chat.send_message(prompt2)
# st.write("Generated Response:", response2)
