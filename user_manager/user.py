import json
import os
import chromadb
import uuid
import os

# ===== Cấu hình ChromaDB Cloud =====
CHROMA_CLOUD_HOST = os.getenv("CHROMA_CLOUD_HOST", "api.trychroma.com")
CHROMA_CLOUD_TENANT = os.getenv("CHROMA_CLOUD_TENANT", "a77c6b71-5d7c-4e9e-b2f3-36c4041e33a2")
CHROMA_CLOUD_DATABASE = os.getenv("CHROMA_CLOUD_DATABASE", "chatbot-ai")
CHROMA_CLOUD_API_KEY = os.getenv("CHROMA_CLOUD_API_KEY", "ck-695vecLiLTuRGkTpwQmELG9SbDiLBsU65ncT1CNpDACU")

client = chromadb.HttpClient(
  ssl=True,
  host={CHROMA_CLOUD_HOST},
  tenant={CHROMA_CLOUD_TENANT},
  database={CHROMA_CLOUD_DATABASE},
  headers={
    'x-chroma-token': {CHROMA_CLOUD_API_KEY}
  }
)

# Tạo hoặc lấy collection
collection = client.get_or_create_collection(name="user_qa")
 
# START - public function
def load_user(user_id):
    results = collection.get(where={"userId": user_id})
    if not results["ids"]:
        return {"status": "NOT_FOUND", "history": []}
    else :
        history_list = []
        user_data = {}
        for meta, doc in zip(results["metadatas"], results["documents"]):
            uid = meta["userId"]
            user_data.setdefault(uid, []).append((meta["question"], doc))

        for user_id, qas in user_data.items():
            for i, (q, a) in enumerate(qas, 1):
                history_list.append(f"Q: {q} - A: {a}")
        data_user_history = " | ".join(history_list)
        return {"status": "FOUND", "history": data_user_history}
 
def save_chat(user_id, question, answer):
    qa_id = str(uuid.uuid4())

    collection.add(
        ids=[qa_id],
        documents=[answer],
        metadatas=[{"userId": user_id, "question": question}]
    )
# END - public function