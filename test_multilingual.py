#!/usr/bin/env python3
"""
Test multilingual FAQ search functionality
"""

from context_manager.context import load_context
from chat_engine.query import query

def test_multilingual_faq():
    """Test FAQ search with Vietnamese questions"""
    
    print("=== Testing Multilingual FAQ Search ===")
    
    # Test Vietnamese questions that should match English FAQ entries
    test_questions = [
        ("What is Amazon EC2 Auto Scaling?", "English"),
        ("Dịch vụ Amazon EC2 Auto Scaling là gì?", "Vietnamese"),
        ("Amazon EC2 Auto Scaling là gì?", "Vietnamese"), 
        ("Auto Scaling của Amazon EC2 là gì?", "Vietnamese"),
        ("EC2 Auto Scaling là dịch vụ gì?", "Vietnamese"),
        ("Lợi ích của Amazon EC2 Auto Scaling là gì?", "Vietnamese - Benefits"),
        ("Target tracking là gì?", "Vietnamese - Target tracking"),
        ("ASG là gì?", "Vietnamese - ASG")
    ]
    
    for question, language in test_questions:
        print(f"\n--- Testing ({language}): {question} ---")
        
        # Load context (should include FAQ)
        context_result = load_context(question)
        print(f"Context Status: {context_result.status}")
        
        if context_result.status == "FOUND":
            # Generate answer
            answer = query("test_user", "", context_result.context, question)
            print(f"Answer: {answer[:150]}...")
            
            # Check if answer comes from FAQ
            if any(term in answer for term in ["Amazon EC2 Auto Scaling", "Auto Scaling", "EC2"]):
                print("✓ FAQ match found!")
            else:
                print("⚠ No FAQ match - using fallback")
        else:
            print("❌ No context found")

if __name__ == "__main__":
    test_multilingual_faq()
