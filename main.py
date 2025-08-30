import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from user_manager.user import load_user, save_chat, load_user_for_web
from context_manager.chroma_context import load_context
from chat_engine.query import query
from tts_engine.tts import text_to_speech
from playsound import playsound

# --- Web Server Setup ---
app = Flask(__name__, static_folder='frontend', static_url_path='/')
CORS(app)

@app.route('/')
def serve_index():
    """
    Serve the main index.html file from the frontend directory.
    """
    return send_from_directory('frontend', 'index.html')

@app.route('/audio/<path:filename>')
def serve_audio(filename):
    """Serve audio files from the 'audio' directory."""
    audio_dir = 'audio'
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)
    return send_from_directory(audio_dir, filename)

@app.route('/history', methods=['POST'])
def get_history():
    """
    Retrieves the chat history for a given user ID.
    The frontend sends a JSON payload with user_id.
    """
    try:
        # Step 1: Get user ID from the request
        data = request.get_json()
        user_id = data.get("user_id")

        if not user_id:
            return jsonify({"error": "Missing user_id"}), 400

        # Step 2: Load chat history from the user manager
        user_data = load_user_for_web(user_id)
        chat_history = user_data.get("history", [])

        # Step 3: Return the history as a JSON response
        return jsonify({"history": chat_history})

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "An internal server error occurred"}), 500

@app.route('/chat', methods=['POST'])
def chat():
    """
    Handles the chatbot logic via a POST request.
    The frontend sends a JSON payload with user_id and message.
    """
    try:
        # Step 1: Get user data from the request
        data = request.get_json()
        user_id = data.get("user_id")
        user_message = data.get("message")

        if not user_id or not user_message:
            return jsonify({"error": "Missing user_id or message"}), 400

        # Step 2: Load user data and previous chat history
        user_data = load_user(user_id)
        chat_history = user_data.get("history", [])

        # Step 3: Load context based on the user's question
        print(f"Loading context for query: {user_message}")
        context_data = load_context(user_message)
        context = context_data.get("context", "") if context_data else ""
        if not context:
            print("No relevant context found. Responding with general knowledge.")
        else:
            print("Context found.")
        
        # Step 4: Query the chat engine with the user's question and context
        answer = query(user_id, chat_history, context, user_message)

        # Step 5: Generate a unique audio file for the answer and return its URL
        # We save the file with a unique name to avoid conflicts
        audio_filename = f"answer_{user_id}_{os.urandom(8).hex()}.wav"
        audio_dir = "audio"
        if not os.path.exists(audio_dir):
            os.makedirs(audio_dir)
        audio_filepath = os.path.join(audio_dir, audio_filename)
        
        print("Generating speech from the answer...")
        text_to_speech(answer, output_file=audio_filepath)
        
        # Step 6: Save the chat history with the user's question and answer
        save_chat(user_id, user_message, answer)

        # Step 7: Return the answer text and the audio URL to the frontend
        audio_url = f"/audio/{audio_filename}"
        return jsonify({"response": answer, "audio_url": audio_url})

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "An internal server error occurred"}), 500

# Function to run the Flask app
def run_server():
    print("Starting Flask server...")
    app.run(host='127.0.0.1', port=5000)

def main():
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
    #if speech_file:
        #print(f"You can now open the '{speech_file}' file to listen to the answer.")
 
    
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