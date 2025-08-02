import json
import os
 
FILE_PATH = "user_data.json"
 
# START - public function
def load_user(user_id):
    data = load_data()
    user_data = find_user(data, user_id)
 
    if not user_data:
        return {"status": "NOT_FOUND", "history": []}
    else:
        history_list = []
        for i, qa in enumerate(user_data["qas"], 1):
            history_list.append(f"Q: {qa['question']} - A: {qa['answer']}")
        data_user_history = " | ".join(history_list)
        return {"status": "FOUND", "history": data_user_history}
 
def save_chat(user_id, question, answer):
    data = load_data()
    user = find_user(data, user_id)
 
    if not user:
        user = {"userId": user_id, "qas": []}
        data.append(user)
 
    user["qas"].append({"question": question, "answer": answer})
    save_data(data)
# END - public function
 
# START - private
def load_data():
    if not os.path.exists(FILE_PATH):
        return []
    with open(FILE_PATH, "r", encoding="utf-8") as file:
        return json.load(file)
 
def find_user(data, user_id):
    for user in data:
        if user["userId"] == user_id:
            return user
    return None
 
def save_data(data):
    with open(FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
# END - private