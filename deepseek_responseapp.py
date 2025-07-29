import streamlit as st
import requests

# ... (your existing CSS and Streamlit setup) ...

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

        # --- IMPORTANT DEBUGGING STEPS ---
        try:
            # Attempt to parse as JSON
            return response.json()
        except requests.exceptions.JSONDecodeError as e:
            st.error(f"JSON Decode Error: Could not parse response as JSON. Original error: {e}")
            st.error(f"Raw API Response Status Code: {response.status_code}")
            st.error(f"Raw API Response Headers: {response.headers}")
            st.error(f"Raw API Response Content (first 500 chars): {response.text[:500]}") # Print raw text for inspection
            return None # Indicate failure
        # --- END DEBUGGING STEPS ---

    except requests.exceptions.RequestException as e:
        st.error(f"Request to Hugging Face API failed: {e}")
        # If response object exists even after an exception (e.g. timeout), you can still inspect it
        if 'response' in locals() and response is not None:
             st.error(f"Request status code (if available): {response.status_code}")
             st.error(f"Request text (if available, first 500 chars): {response.text[:500]}")
        return None  # Return None or an empty dict to indicate failure

# Submit button
if st.button("Generate Response"):
    if user_prompt.strip():
        with st.spinner("Generating response..."):
            output = query({"inputs": user_prompt})

            if output is not None:
                st.markdown("### Response:")
                # This part might need adjustment based on the actual DeepSeek model's response format
                # As observed from Hugging Face inference API, it's typically a list of dicts
                if isinstance(output, list) and len(output) > 0 and "generated_text" in output[0]:
                    st.write(output[0]["generated_text"])
                elif isinstance(output, dict) and "generated_text" in output: # Fallback for direct dict response
                     st.write(output["generated_text"])
                else:
                    st.warning("Could not parse the response from the LLM. Here's the raw output for debugging:")
                    st.json(output) # Display raw JSON for debugging
            else:
                st.error("Failed to get a valid response from the LLM. Check the error messages above for details.")
    else:
        st.warning("Please enter a prompt.")
