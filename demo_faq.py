#!/usr/bin/env python3
"""
Demo script showing FAQ functionality working
"""

from user_manager.user import load_user, save_chat
from context_manager.context import load_context, init_context
from chat_engine.query import query

def demo_faq_functionality():
    """Demonstrate FAQ search working properly"""
    
    print("=== AI Elevate Chatbot - FAQ Demo ===")
    print("Demonstrating FAQ database integration\n")
    
    # Initialize system
    init_context()
    
    # Demo user
    user_id = "demo_faq_user"
    
    # Test the exact question from your scenario
    test_question = "What is Amazon EC2 Auto Scaling?"
    
    print(f"User Question: {test_question}")
    print("-" * 50)
    
    # Step 1: Load context
    print("🔍 Searching for relevant context...")
    context_result = load_context(test_question)
    print(f"Context Status: {context_result.status}")
    
    if context_result.status == "FOUND":
        print("✓ FAQ database loaded successfully!")
        
        # Step 2: Generate answer
        print("\n🤖 Generating response from FAQ database...")
        answer = query(user_id, "", context_result.context, test_question)
        
        # Step 3: Display result
        print("\n--- AI Response ---")
        print(f"🤖 Answer: {answer}")
        
        # Step 4: Save conversation
        print(f"\n💾 Saving conversation for user '{user_id}'...")
        save_chat(user_id, test_question, answer)
        print("✓ Conversation saved!")
        
        # Verify FAQ match
        if "Amazon EC2 Auto Scaling is a fully managed service" in answer:
            print("\n🎉 SUCCESS: Question found exact match in FAQ database!")
            print("✓ System correctly retrieved answer from questions_and_answers.txt")
        else:
            print("\n⚠ Warning: Answer may not be from FAQ database")
    
    else:
        print("❌ Failed to load context")
    
    print("\n" + "="*60)
    print("FAQ Demo completed successfully!")

if __name__ == "__main__":
    demo_faq_functionality()
