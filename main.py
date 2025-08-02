from user_manager.user import load_user, save_chat
from context_manager.context import load_context, build_faiss_index
from chat_engine.query import query

def main():
    
    build_faiss_index("data")

    #Step 1: Load user data, searching for previous history.
    user_id = input("Enter your user ID: ")
    user_data = load_user(user_id)

    if user_data["status"] == "FOUND":
        print("Loaded history:")
        for item in user_data["history"]:
            print(item)
    else:
        print("No previous history found.")

    # Step 2: Load context based on the user's question, checking if it exists.
    question = input("Enter your question: ")
    context_data = load_context(question)

    if context_data["status"] == "FOUND":
        context = context_data["context"]
    else:
        context = ""
        print("No relevant context found.")
    
    # Step 3: Query the chat engine with the user's question and context.
    answer = query(user_id, user_data.get("history", []), context)
    print("Answer:", answer)

    # Step 4: Save the chat history with the user's question and answer.
    # save_chat(user_id, {"question": question, "answer": answer})
    save_chat(user_id, question, answer)

if __name__ == "__main__":
    main()
