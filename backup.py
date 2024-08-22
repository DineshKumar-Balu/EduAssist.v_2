import vertexai
from vertexai.generative_models import GenerativeModel, Part
from google.api_core.exceptions import GoogleAPIError
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Replace with your Google Cloud project ID
project_id = "chat-website-433318"

# Initialize Vertex AI
vertexai.init(project=project_id, location="us-central1")

# Initialize the model
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
    # Define the prompt for the query
    prompt = f"""
    You are a professional assistant. Please answer the following question based on the provided document:
    
    {user_query}
    """
    
    # For the example, we use a static PDF URI. You might want to handle dynamic PDFs based on user context.
    pdf_file_uri = "gs://storage-vectordb/sodapdf-converted.pdf"
    
    # Generate a response to the user's query
    response = summarize_document(pdf_file_uri, prompt)
    return response

# Main function to interact with the user in a loop
def main():
    print("Chatbot is ready. Type 'exit' to quit.")
    while True:
        # Get user query
        user_query = input("You: ")
        
        # Check if the user wants to exit
        if user_query.lower() == 'exit':
            print("Goodbye!")
            break
        
        # Process the query and get the response
        answer = handle_user_query(user_query)
        
        # Print the answer
        print("Bot:", answer)

if __name__ == "__main__":
    main()
