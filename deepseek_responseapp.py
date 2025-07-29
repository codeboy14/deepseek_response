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

# Input prompt - This must be defined BEFORE its first use
user_prompt = st.text_area("Enter your prompt:", height=150)

# IMPORTANT: Update this to the correct DeepSeek R1 model endpoint on Hugging Face
API_URL = "https://api-inference.huggingface.co/models/deepseek-ai/deepseek-llm-7b-chat" 

# Hugging Face API token (securely stored in Streamlit secrets)
headers = {
    "Authorization": f"Bearer {st.secrets['HF_API_TOKEN']}"
}

def query(payload):
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()

        try:
            return response.json()
        except requests.exceptions.JSONDecodeError as e:
            st.error(f"JSON Decode Error: Could not parse response as JSON. Original error: {e}")
            st.error(f"Raw API Response Status Code: {response.status_code}")
            st.error(f"Raw API Response Headers: {response.headers}")
            st.error(f"Raw API Response Content (first 500 chars): {response.text[:500]}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Request to Hugging Face API failed: {e}")
        if 'response' in locals() and response is not None:
             st.error(f"Request status code (if available): {response.status_code}")
             st.error(f"Request text (if available, first 500 chars): {response.text[:500]}")
        return None

# Submit button
# This is where user_prompt is first accessed for its content
if st.button("Generate Response"):
    if user_prompt.strip(): # This line should be safe if user_prompt is defined above
        with st.spinner("Generating response..."):
            output = query({"inputs": user_prompt})

            if output is not None:
                st.markdown("### Response:")
                if isinstance(output, list) and len(output) > 0 and "generated_text" in output[0]:
                    st.write(output[0]["generated_text"])
                elif isinstance(output, dict) and "generated_text" in output:
                     st.write(output["generated_text"])
                else:
                    st.warning("Could not parse the response from the LLM. Here's the raw output for debugging:")
                    st.json(output)
            else:
                st.error("Failed to get a valid response from the LLM. Check the error messages above for details.")
    else:
        st.warning("Please enter a prompt.")
