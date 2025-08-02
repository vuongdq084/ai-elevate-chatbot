import os
import json
from datetime import datetime
from shared.types import UserLoadResult, ChatEntry

def load_user(user_id: str) -> UserLoadResult:
    """
    Load user history from file
    
    Args:
        user_id: User identifier string
        
    Returns:
        UserLoadResult with status and history
    """
    try:
        # Create users directory if it doesn't exist
        users_dir = "users"
        if not os.path.exists(users_dir):
            os.makedirs(users_dir)
        
        # User file path
        user_file = os.path.join(users_dir, f"{user_id}.json")
        
        if os.path.exists(user_file):
            with open(user_file, 'r', encoding='utf-8') as f:
                user_data = json.load(f)
                # Convert chat history to string format
                history_str = ""
                for chat in user_data.get('chat_history', []):
                    history_str += f"Q: {chat['question']}\nA: {chat['answer']}\n---\n"
                
                return UserLoadResult(status="FOUND", history=history_str)
        else:
            return UserLoadResult(status="NOT_FOUND", history="")
            
    except Exception as e:
        print(f"Error loading user {user_id}: {e}")
        return UserLoadResult(status="NOT_FOUND", history="")

def save_chat(user_id: str, question: str, answer: str):
    """
    Save chat conversation to user file
    
    Args:
        user_id: User identifier string
        question: User's question
        answer: Bot's answer
    """
    try:
        # Create users directory if it doesn't exist
        users_dir = "users"
        if not os.path.exists(users_dir):
            os.makedirs(users_dir)
        
        # User file path
        user_file = os.path.join(users_dir, f"{user_id}.json")
        
        # Load existing data or create new
        if os.path.exists(user_file):
            with open(user_file, 'r', encoding='utf-8') as f:
                user_data = json.load(f)
        else:
            user_data = {
                "user_id": user_id,
                "chat_history": []
            }
        
        # Add new chat entry
        chat_entry = {
            "question": question,
            "answer": answer,
            "timestamp": datetime.now().isoformat()
        }
        
        user_data['chat_history'].append(chat_entry)
        
        # Save back to file
        with open(user_file, 'w', encoding='utf-8') as f:
            json.dump(user_data, f, ensure_ascii=False, indent=2)
            
        print(f"Chat saved for user {user_id}")
        
    except Exception as e:
        print(f"Error saving chat for user {user_id}: {e}")
