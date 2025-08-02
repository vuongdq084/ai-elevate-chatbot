#!/usr/bin/env python3
"""
Test FAQ search functionality
"""

from context_manager.context import load_context
from chat_engine.query import query

def test_faq_search():
    """Test FAQ search with specific questions"""
    
    print("=== Testing FAQ Search ===")
    
    # Test questions that should match FAQ entries
    test_questions = [
        "What is Amazon EC2 Auto Scaling?",
        "When should I use Amazon EC2 Auto Scaling vs. AWS Auto Scaling?",
        "What are the benefits of using Amazon EC2 Auto Scaling?",
        "What is target tracking?",
        "What is an EC2 Auto Scaling group (ASG)?",
        "What is fleet management and how is it different from dynamic scaling?"
    ]
    
    for question in test_questions:
        print(f"\n--- Testing: {question} ---")
        
        # Load context (should include FAQ)
        context_result = load_context(question)
        print(f"Context Status: {context_result.status}")
        
        if context_result.status == "FOUND":
            # Generate answer
            answer = query("test_user", "", context_result.context, question)
            print(f"Answer: {answer[:100]}...")
            
            # Check if answer comes from FAQ
            if "Amazon EC2 Auto Scaling" in answer:
                print("✓ FAQ match found!")
            else:
                print("⚠ No FAQ match - using fallback")
        else:
            print("❌ No context found")

if __name__ == "__main__":
    test_faq_search()
