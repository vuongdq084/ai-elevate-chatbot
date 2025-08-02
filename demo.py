#!/usr/bin/env python3
"""
Demo script for AI Elevate Chatbot
This script demonstrates the functionality of all modules
"""

from user_manager.user import load_user, save_chat
from context_manager.context import load_context, init_context
from chat_engine.query import query

def demo_system():
    """
    Demonstrate the AI chatbot system functionality
    """
    print("=== AI Elevate Chatbot Demo ===")
    
    # Initialize context system
    print("\n1. Initializing context system...")
    init_context()
    
    # Demo user
    demo_user_id = "demo_user"
    
    # Test Module 2: Load User
    print(f"\n2. Testing Module 2 - Load User (ID: {demo_user_id})")
    user_data = load_user(demo_user_id)
    print(f"   Status: {user_data.status}")
    print(f"   History: {user_data.history[:100]}..." if len(user_data.history) > 100 else f"   History: {user_data.history}")
    
    # Test questions
    test_questions = [
        "What's the weather like in Hanoi?",
        "How's the traffic in Ho Chi Minh City?",
        "Can you recommend restaurants in Da Nang?",
        "Hello, how are you?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n3.{i} Testing question: '{question}'")
        
        # Test Module 3: Load Context
        print("   - Loading context...")
        context_data = load_context(question)
        print(f"   - Context status: {context_data.status}")
        if context_data.status == "FOUND":
            print(f"   - Context preview: {context_data.context[:100]}...")
        
        # Test Module 4: Query
        print("   - Generating response...")
        answer = query(demo_user_id, user_data.history, context_data.context, question)
        print(f"   - Answer: {answer}")
        
        # Test Module 2: Save Chat
        print("   - Saving chat...")
        save_chat(demo_user_id, question, answer)
        
        # Update history for next iteration
        user_data.history += f"Q: {question}\nA: {answer}\n---\n"
    
    print("\n=== Demo completed successfully! ===")
    print("\nThe system has demonstrated:")
    print("✓ Module 1: Main program flow")
    print("✓ Module 2: User management (load/save)")
    print("✓ Module 3: Context management")
    print("✓ Module 4: Query processing")
    
    # Show final user data
    print(f"\n=== Final user data for '{demo_user_id}' ===")
    final_user_data = load_user(demo_user_id)
    print(f"Status: {final_user_data.status}")
    print("Chat History:")
    print(final_user_data.history)

if __name__ == "__main__":
    demo_system()
