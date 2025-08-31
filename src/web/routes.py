import os
from flask import request, jsonify, send_from_directory
from core.user_manager.user import load_user, save_chat, load_user_for_web
from core.context_manager.chroma_context import load_context
from core.chat_engine.query import query
from core.tts_engine.tts import text_to_speech
from config.settings import FRONTEND_DIR, AUDIO_DIR

def init_routes(app):
    """Initialize all web routes"""
    
    @app.route('/')
    def serve_index():
        """Serve the main index.html file from the frontend directory."""
        return send_from_directory(FRONTEND_DIR, 'index.html')

    @app.route('/audio/<path:filename>')
    def serve_audio(filename):
        """Serve audio files from the audio directory."""
        if not os.path.exists(AUDIO_DIR):
            os.makedirs(AUDIO_DIR)
        return send_from_directory(AUDIO_DIR, filename)

    @app.route('/history', methods=['POST'])
    def get_history():
        """Retrieves the chat history for a given user ID."""
        try:
            data = request.get_json()
            user_id = data.get("user_id")

            if not user_id:
                return jsonify({"error": "Missing user_id"}), 400

            user_data = load_user_for_web(user_id)
            chat_history = user_data.get("history", [])
            return jsonify({"history": chat_history})

        except Exception as e:
            print(f"An error occurred: {e}")
            return jsonify({"error": "An internal server error occurred"}), 500

    @app.route('/chat', methods=['POST'])
    def chat():
        """Handles the chatbot logic via a POST request."""
        try:
            data = request.get_json()
            user_id = data.get("user_id")
            user_message = data.get("message")

            if not user_id or not user_message:
                return jsonify({"error": "Missing user_id or message"}), 400

            # Load user data and chat history
            user_data = load_user(user_id)
            chat_history = user_data.get("history", [])

            # Load context
            print(f"Loading context for query: {user_message}")
            context_data = load_context(user_message)
            print(f"Context data: {context_data}")
            context = context_data.get("context", "") if context_data else ""
            
            if not context:
                print("No relevant context found. Responding with general knowledge.")
            else:
                print(f"Context found. Length: {len(context)}")
                print(f"Context preview: {context[:200]}...")
            
            # Query chat engine
            answer = query(user_id, chat_history, context, user_message)

            # Generate audio file
            audio_filename = f"answer_{user_id}_{os.urandom(8).hex()}.wav"
            if not os.path.exists(AUDIO_DIR):
                os.makedirs(AUDIO_DIR)
            audio_filepath = os.path.join(AUDIO_DIR, audio_filename)
            
            print("Generating speech from the answer...")
            text_to_speech(answer, output_file=audio_filepath)
            
            # Save chat history
            save_chat(user_id, user_message, answer)

            # Return response
            audio_url = f"/audio/{audio_filename}"
            return jsonify({"response": answer, "audio_url": audio_url})

        except Exception as e:
            print(f"An error occurred: {e}")
            return jsonify({"error": "An internal server error occurred"}), 500
