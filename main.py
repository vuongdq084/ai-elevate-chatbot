from user_manager.user import load_user, save_chat
from context_manager.chroma_context import load_context
from chat_engine.query import query
from tts_engine.tts import text_to_speech
from playsound import playsound
 
def main():
    # Step 1: Load user data, searching for previous history.
    # user_id = input("Enter your user ID: ")
    # user_data = load_user(user_id)
 
    # if user_data["status"] == "FOUND":
    #     print("Loaded history:")
    #     # The history from load_user is a single string, so we can't iterate.
    #     # Let's just print it directly.
    #     print(user_data["history"])
    # else:
    #     print("No previous history found.")
 
    # Step 2: Load context based on the user's question, checking if it exists.
    # question = input("Enter your question: ")
    while True:
        print("Enter your question: ")
        lines = []
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)

        question = "\n".join(lines)

        context_data = load_context(question)
    
        if context_data["status"] == "FOUND":
            context = context_data["context"]
        else:
            context = ""
            print("No relevant context found.")
        
        # Step 3: Query the chat engine with the user's question and context.
        # FIX: The `query` function was missing the 'question' argument.
        
        answer = query("test", "test", context, question)
        print("Answer:", answer)
 
     # Step 4: Call the TTS function from the new package to generate speech
    print("Generating speech from the answer...")
    speech_file = text_to_speech(answer, output_file="answer.wav")
    playsound(speech_file)
    #if speech_file:
        #print(f"You can now open the '{speech_file}' file to listen to the answer.")
 
    # Step 5: Save the chat history with the user's question and answer.
    save_chat(user_id, question, answer)
 
    
if __name__ == "__main__":
    main()