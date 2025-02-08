import streamlit as st
import argparse
import json
from argparse import RawTextHelpFormatter
import requests
from typing import Optional
import warnings
from dotenv import load_dotenv
import os
load_dotenv()
try:
    from langflow.load import upload_file
except ImportError:
    warnings.warn("Langflow provides a function to help you upload files to the flow. Please install langflow to use it.")
    upload_file = None

BASE_API_URL = os.getenv("BASE_API_URL")
LANGFLOW_ID = os.getenv("LANGFLOW_ID")
FLOW_ID = os.getenv("FLOW_ID")
APPLICATION_TOKEN = os.getenv("APPLICATION_TOKEN")
ENDPOINT = "BasicPromptFlow"

PROJECT_NAME = "AI Academic Assistant"
YOUR_NAME = "Keshav"
YOUR_QUALIFICATION = "Master of Applied Computing with a specialization in AI at the University of Windsor"

def run_flow(message: str, endpoint: str, application_token: str) -> str:
    """Modified version of your existing function"""
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{endpoint}"

    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat"
    }

    headers = {
        "Authorization": f"Bearer {application_token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        response_data = response.json()

        # Extract message text from response
        return response_data["outputs"][0]["outputs"][0]["results"]["message"]["text"]

    except Exception as e:
        return f"Error: {str(e)}"


st.set_page_config(
    page_title=PROJECT_NAME,
    page_icon="🤖",
    layout="centered"
)

# Custom CSS for styling
st.markdown(
    """
    <style>
    .stApp {
        max-width: 800px;
        margin: auto;
    }
    .stChatMessage {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .stChatMessage.user {
        background-color: #f0f2f6;
    }
    .stChatMessage.assistant {
        background-color: #e3f2fd;
    }
    .title {
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
    }
    .subtitle {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Project title and subtitle
st.markdown(f'<div class="title">{PROJECT_NAME}</div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="subtitle">Hi! I\'m {YOUR_NAME}, an AI-powered assistant. '
    f'I can help answer questions about {YOUR_QUALIFICATION} and related topics.</div>',
    unsafe_allow_html=True
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": f"Hi! I'm {YOUR_NAME}, an AI-powered assistant. "
                       f"I'm currently pursuing {YOUR_QUALIFICATION}. "
                       "How can I assist you today?"
        }
    ]

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to ask?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI response
    with st.spinner("Thinking..."):
        try:
            full_response = run_flow(
                message=prompt,
                endpoint=ENDPOINT,
                application_token=APPLICATION_TOKEN
            )
        except Exception as e:
            full_response = f"An error occurred: {str(e)}"

    # Display AI response
    with st.chat_message("assistant"):
        st.markdown(full_response)

    # Add AI response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
