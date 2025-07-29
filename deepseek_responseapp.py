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

# IMPORTANT: Update this to the correct DeepSeek R1 model endpoint on Hugging Face
# You will need to find the specific DeepSeek R1 model you want to use
# For example, if you're using deepseek-llm-7b-chat:
API_URL = "https://api-inference.huggingface.co/models/deepseek-ai/deepseek-llm-7b-chat"
# Or deepseek-ai/deepseek-llm-7b-base, etc. CHECK THE MODEL PAGE ON HUGGING FACE.

# Hugging Face API token (securely stored in Streamlit secrets)
headers = {
    "Authorization": f"Bearer {st.secrets['HF_API_TOKEN']}"
}

def query(payload):
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Request to Hugging Face API failed: {e}")
        return None  # Return None or an empty dict to indicate failure
    except ValueError:
        st.error("Failed to decode JSON from API response. The API might have returned an empty or invalid response.")
        return None

# Submit button
if st.button("Generate Response"):
    if user_prompt.strip():
        with st.spinner("Generating response..."):
            output = query({"inputs": user_prompt})

            if output is not None:
                st.markdown("### Response:")
                # This part might need adjustment based on the actual DeepSeek model's response format
                if isinstance(output, list) and len(output) > 0 and "generated_text" in output[0]:
                    st.write(output[0]["generated_text"])
                elif isinstance(output, dict) and "generated_text" in output: # Fallback for direct dict response
                     st.write(output["generated_text"])
                else:
                    st.warning("Could not parse the response from the LLM. Here's the raw output:")
                    st.json(output) # Display raw JSON for debugging
            else:
                st.error("Failed to get a response from the LLM.")
    else:
        st.warning("Please enter a prompt.")
