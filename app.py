import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from a .env file for security
load_dotenv()

# Configure the Gemini API client
# The API key is loaded from the environment variable named "GOOGLE_API_KEY".
# This is a best practice to avoid hardcoding sensitive information.
try:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
except Exception as e:
    st.error(f"Error configuring Google Generative AI: {e}")
    st.info("Please make sure you have a valid API key set up in a .env file or as an environment variable.")
    st.stop()

# Set up the model name as requested
# The user's request for "gemini-2.0-flash-lite" is noted. The `google-generativeai` library
# internally handles the correct API endpoint based on the model name.
MODEL_NAME = "gemini-2.0-flash-lite" 

# Set the Streamlit page configuration and title
st.set_page_config(page_title="GenAI Network Scripting Assistant", layout="wide")
st.title("MANISH  - Network Scripting Assistant 🤖")
st.markdown(
    """
    Hello! I'm an AI-powered assistant designed to help network engineers.
    Just tell me the task you want to automate, and I will generate a
    network automation script for you.
    """
)

# Initialize Streamlit session state to store conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "user":
            st.markdown(message["content"])
        else:
            st.code(message["content"], language="python")

# Get user input and display it
if prompt := st.chat_input("Describe the network task you want to automate..."):
    # Add user's message to chat history and display
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare the prompt for the model
    # Providing a detailed system instruction helps the model generate accurate code.
    system_instruction = (
        "You are an expert network engineer and Python programmer. "
        "Your task is to generate a complete and well-commented Python "
        "script for network automation based on the user's request. "
        "The script should use standard libraries like `netmiko` or `paramiko` "
        "and should be ready to run. Provide only the code, no extra text or explanation."
    )
    
    # Create the model instance with the specified model name
    try:
        model = genai.GenerativeModel(
            model_name=MODEL_NAME,
            system_instruction=system_instruction
        )
    except Exception as e:
        st.error(f"Error initializing model '{MODEL_NAME}': {e}")
        st.stop()

    # Generate the script from the model
    with st.spinner("Thinking... Generating script..."):
        try:
            response = model.generate_content(
                f"Generate a network automation script for the following task: {prompt}",
            )
            generated_script = response.text
        except Exception as e:
            generated_script = f"An error occurred while generating the script: {e}"
            st.error(generated_script)

    # Display the generated script in a code block
    with st.chat_message("assistant"):
        st.code(generated_script, language="python")

    # Add assistant's response to chat history
    st.session_state.messages.append({"role": "assistant", "content": generated_script})

