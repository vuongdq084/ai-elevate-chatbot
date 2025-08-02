from user_manager.user import load_user, save_chat
from context_manager.context import load_context, init_context
from chat_engine.query import query, query_batch, analyze_question_intent

def main():
    """
    Main program flow for AI Elevate Chatbot with Azure OpenAI integration,
    Function Calling, and Batching support
    """
    print("=== AI Elevate Chatbot ===")
    print("Welcome to the AI Chatbot System with Azure OpenAI, Function Calling & Batching!")
    
    # Check if OpenAI package is available
    try:
        import openai
        print("✅ Azure OpenAI integration enabled")
        print("✅ Function Calling support enabled")
        print("✅ Batching support enabled")
    except ImportError:
        print("⚠ OpenAI package not installed. Install with: pip install openai")
        print("  Falling back to rule-based responses.")
    
    # Initialize context system with FAQ data
    print("\n--- Initializing System ---")
    init_context()
    
    # Step 1: Request user to enter username
    print("\n--- User Authentication ---")
    user_id = input("Enter your user name: ").strip()
    
    if not user_id:
        print("User name cannot be empty. Exiting...")
        return
    
    # Step 2: Call Module 2 LoadUser to get history
    print(f"\n--- Loading User History for '{user_id}' ---")
    user_data = load_user(user_id)
    
    if user_data.status == "FOUND":
        print("✓ User found! Previous chat history:")
        print("-" * 50)
        print(user_data.history if user_data.history else "No previous conversations.")
        print("-" * 50)
    else:
        print("✓ New user detected. Starting fresh conversation.")
    
    # Ask for mode selection
    print("\n--- Mode Selection ---")
    print("Choose interaction mode:")
    print("1. Single Question Mode (default)")
    print("2. Batch Question Mode")
    print("3. Function Calling Demo")
    
    mode = input("Enter mode (1/2/3) or press Enter for default: ").strip()
    
    if mode == "2":
        batch_mode(user_id, user_data)
    elif mode == "3":
        function_calling_demo()
    else:
        single_question_mode(user_id, user_data)

def single_question_mode(user_id: str, user_data):
    """Single question mode with Function Calling support"""
    
    # Main chat loop
    while True:
        print("\n--- Chat Session ---")
        
        # Step 3: Request user to enter question
        question = input("Enter your question (or 'quit' to exit): ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("Thank you for using AI Elevate Chatbot. Goodbye!")
            break
        
        if not question:
            print("Question cannot be empty. Please try again.")
            continue
        
        # Optional: Show intent analysis
        show_analysis = input("Show question analysis? (y/n): ").strip().lower() == 'y'
        if show_analysis:
            print("\n🧠 Analyzing question intent...")
            analysis = analyze_question_intent(question)
            print(f"   Language: {analysis['language']}")
            print(f"   Intent: {analysis['intent']}")
            print(f"   Confidence: {analysis['confidence']:.1f}")
            print(f"   Recommended Function: {analysis['recommended_function']}")
            print(f"   Reasoning: {analysis['reasoning']}")
        
        # Step 4: Call Module 3 LoadContext to get context
        print("🔍 Searching for relevant context...")
        context_data = load_context(question)
        
        if context_data.status == "FOUND":
            print("✓ Relevant context found!")
            context = context_data.context
        else:
            print("⚠ No specific context found. Using general knowledge.")
            context = ""
        
        # Step 5: Call Module 4 Query with Function Calling to get answer
        print("🤖 Generating response with Function Calling...")
        answer = query(user_id, user_data.history, context, question)
        
        # Step 6: Display answer on screen
        print("\n--- AI Response ---")
        print("🤖 Answer:", answer)
        
        # Step 7: Call Module 2 SaveChat to save the conversation
        print("\n💾 Saving conversation...")
        save_chat(user_id, question, answer)
        
        # Update user history for next iteration
        user_data.history += f"Q: {question}\nA: {answer}\n---\n"
        
        print("\n" + "="*60)

def batch_mode(user_id: str, user_data):
    """Batch processing mode"""
    
    print("\n=== Batch Question Mode ===")
    print("Enter multiple questions separated by new lines.")
    print("Type 'END' on a new line when finished.")
    
    questions = []
    print("\nEnter your questions:")
    
    while True:
        line = input(f"Question {len(questions) + 1}: ").strip()
        if line.upper() == 'END':
            break
        if line:
            questions.append(line)
    
    if not questions:
        print("No questions entered. Returning to main mode.")
        return
    
    print(f"\n📋 Processing {len(questions)} questions in batch...")
    
    # Load context once for all questions
    context_data = load_context("batch processing multiple questions")
    context = context_data.context if context_data.status == "FOUND" else ""
    
    # Process questions in batch
    print("🚀 Starting batch processing...")
    answers = query_batch(user_id, user_data.history, context, questions)
    
    # Display results
    print(f"\n📊 Batch Processing Results:")
    print("=" * 60)
    
    for i, (question, answer) in enumerate(zip(questions, answers), 1):
        print(f"\n--- Question {i} ---")
        print(f"Q: {question}")
        print(f"A: {answer}")
        
        # Save each conversation
        save_chat(user_id, question, answer)
        user_data.history += f"Q: {question}\nA: {answer}\n---\n"
    
    print(f"\n✅ Batch processing completed!")
    print(f"   Questions processed: {len(questions)}")
    print(f"   All conversations saved for user: {user_id}")

def function_calling_demo():
    """Demonstrate Function Calling capabilities"""
    
    print("\n=== Function Calling Demo ===")
    print("Demonstrating AI's ability to call specific functions")
    
    # Sample questions that trigger different functions
    demo_questions = [
        ("What is Amazon EC2 Auto Scaling?", "FAQ Database Function"),
        ("Thời tiết hôm nay ở Hà Nội?", "Weather Function"),
        ("Traffic in Ho Chi Minh City?", "Traffic Function"),
        ("Best restaurants in Da Nang?", "Restaurant Function"),
        ("Cost analysis for Auto Scaling?", "Cost Analysis Function")
    ]
    
    init_context()
    
    for i, (question, expected_function) in enumerate(demo_questions, 1):
        print(f"\n--- Demo {i}: {expected_function} ---")
        print(f"Question: {question}")
        
        # Analyze intent
        analysis = analyze_question_intent(question)
        print(f"🎯 Detected Intent: {analysis['intent']}")
        print(f"🔧 Recommended Function: {analysis['recommended_function']}")
        
        # Get answer
        context_data = load_context(question)
        answer = query("demo_user", "", context_data.context, question)
        print(f"🤖 Answer: {answer[:100]}...")
        
        print("-" * 50)
    
    print("\n✅ Function Calling demo completed!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please restart the program.")
