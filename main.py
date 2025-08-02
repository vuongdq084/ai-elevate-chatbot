from user_manager.user import load_user, save_chat
from context_manager.context import load_context
from chat_engine.query import query

def main():
    user_id = input("Enter your user ID: ")
    user_data = load_user(user_id)

    if user_data["status"] == "FOUND":
        print("Loaded history:")
        for item in user_data["history"]:
            print(item)
    else:
        print("No previous history found.")

    question = input("Enter your question: ")
    context_data = load_context(question)

    if context_data["status"] == "FOUND":
        context = context_data["context"]
    else:
        context = ""
        print("No relevant context found.")

    answer = query(user_id, user_data.get("history", []), context)
    print("Answer:", answer)

    save_chat(user_id, {"question": question, "answer": answer})

if __name__ == "__main__":
    main()
