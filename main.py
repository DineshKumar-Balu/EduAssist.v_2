import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel, Part
from google.api_core.exceptions import GoogleAPIError
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize Vertex AI
project_id = "chat-website-433318"
vertexai.init(project=project_id, location="us-central1")
model = GenerativeModel("gemini-1.5-flash-001")

# Function to handle document summarization
def summarize_document(pdf_file_uri, prompt):
    pdf_file = Part.from_uri(pdf_file_uri, mime_type="application/pdf")
    contents = [pdf_file, prompt]
    
    try:
        response = model.generate_content(contents)
        return response.text
    except GoogleAPIError as e:
        logging.error(f"Google API error occurred: {e}")
        return "An error occurred while processing your request."
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return "An unexpected error occurred."

# Function to handle user queries
def handle_user_query(user_query):
    prompt = f"""
    You are a friendly, professional assistant. Please answer the following question based on the provided document:
    
    {user_query}
    """
    pdf_file_uri = "gs://storage-vectordb/sodapdf-converted.pdf"
    response = summarize_document(pdf_file_uri, prompt)
    return response

# Function to generate casual conversation responses
def casual_chat_response(user_query):
    if "how are you" in user_query.lower():
        return "I'm just a bunch of code, but thanks for asking! How can I assist you today?"
    elif "hello" in user_query.lower() or "hi" in user_query.lower():
        return "Hello! I'm here to help with any questions you have about the document."
    elif "thank you" in user_query.lower():
        return "You're very welcome! If you have more questions, feel free to ask."
    else:
        return handle_user_query(user_query)

# Streamlit app
st.write("Query me!!!")

# Input box for user query
user_query = st.text_input("Enter your query:")

# Button to submit the query
if st.button("Submit"):
    if user_query.lower() == 'exit':
        st.write("Goodbye! Feel free to come back anytime.")
    elif user_query.strip() == "":
        st.write("Please enter a query to proceed.")
    else:
        answer = casual_chat_response(user_query)
        st.write(f"**Bot:** {answer}")
