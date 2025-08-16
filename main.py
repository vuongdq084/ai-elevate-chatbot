import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from user_manager.user import load_user, save_chat
from context_manager.chroma_context import load_context
from chat_engine.query import query
from tts_engine.tts import text_to_speech

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

@app.route('/chat', methods=['POST'])
def chat():
    """
    Handles the chatbot logic via a POST request.
    The frontend sends a JSON payload with user_id and message.
    """
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        user_message = data.get("message")

        if not user_id or not user_message:
            return jsonify({"error": "Missing user_id or message"}), 400

        user_data = load_user(user_id)
        chat_history = user_data.get("history", [])

        print(f"Loading context for query: {user_message}")
        context_data = load_context(user_message)
        context = context_data.get("context", "")
        if context == "":
            print("No relevant context found. Responding with general knowledge.")
        else:
            print("Context found.")
        
        answer = query(user_id, chat_history, context, user_message)

        # Step 4: Generate a unique audio file for the answer and return its URL
        audio_filename = f"answer_{user_id}_{os.urandom(8).hex()}.wav"
        audio_dir = "audio"
        if not os.path.exists(audio_dir):
            os.makedirs(audio_dir)
        audio_filepath = os.path.join(audio_dir, audio_filename)
        
        print("Generating speech from the answer...")
        text_to_speech(answer, output_file=audio_filepath)
        
        # Save chat history
        save_chat(user_id, user_message, answer)

        # Return the answer text and the audio URL to the frontend
        audio_url = f"/audio/{audio_filename}"
        return jsonify({"response": answer, "audio_url": audio_url})

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "An internal server error occurred"}), 500

# Function to run the Flask app
def run_server():
    print("Starting Flask server...")
    # Set FLASK_ENV to production to suppress the warning
    os.environ['FLASK_ENV'] = 'production'
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    run_server()
