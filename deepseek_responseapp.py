import streamlit as st
import requests

# Custom CSS for white background and dark green accents
st.markdown("""
    <style>
        body {
            background-color: white;
        }
        .stApp {
            background-color: white;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #006400; /* Dark green */
        }
        .stTextArea textarea {
            background-color: #f0fff0; /* Light green tint */
            border: 1px solid #006400;
            color: #006400;
        }
        .stButton>button {
            background-color: #006400;
            color: white;
            border: None;
        }
        .stButton>button:hover {
            background-color: #004d00;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("DeepSeek R1 Response App")

# Input prompt
user_prompt = st.text_area("Enter your prompt:", height=150)

# API endpoint
API_URL = "https://api-inference.huggingface.co/models/deepseek-ai/deepseek-llm-r1"

# Hugging Face API token (securely stored in Streamlit secrets)
headers = {
    "Authorization": f"Bearer {st.secrets['HF_API_TOKEN']}"
}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Submit button
if st.button("Generate Response"):
    if user_prompt.strip():
        with st.spinner("Generating response..."):
            output = query({"inputs": user_prompt})
            st.markdown("### Response:")
            st.write(output.get("generated_text", "No response received."))
    else:
        st.warning("Please enter a prompt.")
