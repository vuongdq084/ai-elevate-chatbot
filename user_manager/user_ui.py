import json
import os
import chromadb
import uuid
from chromadb.config import Settings 

# ===== ChromaDB Local Configuration =====
# Client for persistent storage
client = chromadb.PersistentClient(path="./chroma_db", settings=Settings(allow_reset=True))
 
# Create or get the collection for user Q&A
collection = client.get_or_create_collection(name="user_qa")
 
# START - public function
def load_user(user_id):
    """
    Loads a user's chat history from ChromaDB.
    Returns a list of messages for the frontend to display.
    """
    # Get all documents for the given user ID, ordered by their creation
    # For simplicity, we assume the IDs are added sequentially.
    results = collection.get(where={"userId": user_id})

    # If no results are found, return an empty history
    if not results["ids"]:
        return {"status": "NOT_FOUND", "history": []}
    else:
        # Reconstruct the chat history as a list of alternating user and bot messages
        history_list = []
        # Sort results based on metadatas to maintain chat order, if possible
        # This part might need to be refined depending on how IDs are generated
        # Here we just iterate as they are retrieved.
        for meta, doc in zip(results["metadatas"], results["documents"]):
            history_list.append(meta["question"])
            history_list.append(doc)
        
        return {"status": "FOUND", "history": history_list}

def save_chat(user_id, question, answer):
    """
    Saves a new chat message pair (question and answer) to ChromaDB.
    """
    # Generate a unique ID for the question-answer pair
    qa_id = str(uuid.uuid4())

    collection.add(
        ids=[qa_id],
        documents=[answer],
        metadatas=[{"userId": user_id, "question": question}]
    )
    print(f"Chat history saved for user: {user_id}")
# END - public function
