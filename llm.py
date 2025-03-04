from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq

# Load environment variables from a .env file
load_dotenv()

# Validate environment variables
required_vars = ["MODEL_NAME", "GROQ_API_KEY"]
for var in required_vars:
    if var not in os.environ:
        raise ValueError(f"Environment variable '{var}' is not set. Please add it to your .env file.")

# Initialize the ChatGroq model
llm = ChatGroq(model_name=os.environ["MODEL_NAME"], temperature=0.4)

# Function to invoke the LLM and return the response content
def invoke_llm(message, chat_history=None):
    """
    Invoke the LLM with a message and optional chat history.
    
    Args:
        message (str): The user's message.
        chat_history (list): A list of dictionaries containing the chat history.
                             Each dictionary should have "user" and "bot" keys.
    
    Returns:
        str: The LLM's response.
    """
    # System prompt to provide context
    system_prompt = (
        "You are a helpful assistant providing support during a flooding disaster. "
        "Users are in urgent need of assistance. Provide direct, concise, and actionable answers. "
        "Do not include unnecessary details or explanations. Focus on helping the user immediately. "
        "If the question is unrelated to flooding, still provide a direct and concise answer."
        "The disaster managment centre contact number in Rathnapura is +94 452 222 991"
        
        
    )

    # Prepare the chat history as context
    history_context = ""
    if chat_history:
        for chat in chat_history:
            history_context += f"User: {chat['user']}\nBot: {chat['bot']}\n"

    # Combine the system prompt, chat history, and user message
    full_message = f"{system_prompt}\n\n{history_context}User: {message}"

    try:
        # Invoke the LLM with the combined message
        response = llm.invoke(full_message)
        return response.content
    except Exception as e:
        print(f"Error invoking LLM: {e}")
        return "Sorry, I encountered an error while processing your request."