import json
import os
import chromadb
import uuid
import os
from chromadb.config import Settings
from datetime import datetime

# ===== Cấu hình ChromaDB Local =====
client = chromadb.PersistentClient(path="./chroma_db", settings=Settings(allow_reset=True))
 
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
        items.sort(key=lambda x: x["createdAt"], reverse=True)
        
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
        items.sort(key=lambda x: x["createdAt"], reverse=True)

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