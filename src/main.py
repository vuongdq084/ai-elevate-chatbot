import os
from flask import Flask
from flask_cors import CORS
from playsound import playsound

# Import from new structure
from config.settings import HOST, PORT, DEBUG
from web.routes import init_routes
from core.user_manager.user import load_user, save_chat
from core.context_manager.chroma_context import load_context
from core.chat_engine.query import query
from core.tts_engine.tts import text_to_speech

# --- Web Server Setup ---
app = Flask(__name__, static_folder='web/static', static_url_path='/')
CORS(app)

# Initialize routes
init_routes(app)

# Function to run the Flask app
def run_server():
    print("Starting Flask server...")
    app.run(host=HOST, port=PORT, debug=DEBUG)

def main():
    """Command Line Interface for the chatbot"""
    # Step 1: Load user data, searching for previous history.
    user_id = input("Enter your user ID: ")
    user_data = load_user(user_id)
    chat_history = []
    if user_data["status"] == "FOUND":
        print("Loaded history:")
        chat_history = user_data["history"]
        print(user_data["history"])
    else:
        print("No previous history found.")
 
    # Step 2: Load context based on the user's question, checking if it exists.
    while True:
        print("Enter your question: ")
        question = input().strip()
        context_data = load_context(question)
    
        if context_data["status"] == "FOUND":
            context = context_data["context"]
        else:
            context = ""
            print("No relevant context found.")
        
        # Step 3: Query the chat engine with the user's question and context.
        answer = query(user_id, chat_history, context, question)
        print("Answer:", answer)
        save_chat(user_id, question, answer)
        user_data = load_user(user_id)
        chat_history = user_data["history"]
 
        # Step 4: Call the TTS function from the new package to generate speech
        print("Generating speech from the answer...")
        speech_file = text_to_speech(answer, output_file="answer.wav")
        playsound(speech_file)
        
if __name__ == "__main__":
    print("Choose your interface:")
    print("1. Web Interface (Flask)")
    print("2. Command Line Interface")
    
    choice = input("Enter your choice (1 or 2): ").strip()
    
    if choice == "1":
        run_server()
    elif choice == "2":
        main()
    else:
        print("Invalid choice. Running web interface by default...")
        run_server()