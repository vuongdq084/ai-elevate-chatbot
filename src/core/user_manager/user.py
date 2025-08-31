import json
import os
import chromadb
import uuid
import os
from chromadb.config import Settings
from datetime import datetime

# ===== Cấu hình ChromaDB Local =====
client = chromadb.PersistentClient(path="../../data/chroma_db", settings=Settings(allow_reset=True))
 
# Tạo hoặc lấy collection
collection = client.get_or_create_collection(name="user_qa")
 
# START - public function
def load_user(user_id, top_k = 5):
    results = collection.get(where={"userId": user_id})
    if not results["ids"]:
        return {"status": "NOT_FOUND", "history": []}
    else :
        items = []
        for meta, doc in zip(results["metadatas"], results["documents"]):
            items.append({
                "question": meta["question"],
                "answer": doc,
                "createdAt": meta.get("createdAt")
            })
        items.sort(key=lambda x: x["createdAt"], reverse=False)  # Oldest first
        
        if top_k > 0 :
            recent = items[:top_k]

        history_list = [
            f"Question: {item['question']} - Answer: {item['answer']}" for item in recent
        ]
        data_user_history = " | ".join(history_list)

        return {"status": "FOUND", "history": data_user_history}
 
def save_chat(user_id, question, answer):
    qa_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat()

    collection.add(
        ids=[qa_id],
        documents=[answer],
        metadatas=[{"userId": user_id, "question": question, "createdAt": timestamp}]
    )

def get_user_questions_answers(user_id, top_k=5):
    results = collection.get(where={"userId": user_id})
    if not results["ids"]:
        return {"status": "NOT_FOUND", "questions": [], "answers": []}
    else:
        items = []
        for meta, doc in zip(results["metadatas"], results["documents"]):
            items.append({
                "question": meta["question"],
                "answer": doc,
                "createdAt": meta.get("createdAt")
            })
        items.sort(key=lambda x: x["createdAt"], reverse=False)  # Oldest first

        if top_k > 0:
            items = items[:top_k]

        questions = [item["question"] for item in items]
        answers = [item["answer"] for item in items]

        return {
            "status": "FOUND",
            "questions": questions,
            "answers": answers
        }
# END - public function

# Additional functions from user_ui.py for web interface
def load_user_for_web(user_id):
    """
    Loads a user's chat history from ChromaDB for web interface.
    Returns a list of messages for the frontend to display.
    """
    # Get all documents for the given user ID, ordered by their creation
    results = collection.get(where={"userId": user_id})

    # If no results are found, return an empty history
    if not results["ids"]:
        return {"status": "NOT_FOUND", "history": []}
    else:
        # Reconstruct the chat history as a list of alternating user and bot messages
        history_list = []
        # Sort results based on metadatas to maintain chat order
        items = []
        for meta, doc in zip(results["metadatas"], results["documents"]):
            items.append({
                "question": meta["question"],
                "answer": doc,
                "createdAt": meta.get("createdAt")
            })
        items.sort(key=lambda x: x["createdAt"], reverse=False)  # Oldest first
        
        # Create flat list: question, answer, question, answer...
        for item in items:
            history_list.append(item["question"])
            history_list.append(item["answer"])
        
        return {"status": "FOUND", "history": history_list}