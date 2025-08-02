#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo Vietnamese FAQ functionality
"""

from context_manager.context import load_context
from chat_engine.query import query

def demo_vietnamese_questions():
    """Test specific Vietnamese questions"""
    
    print("=== Vietnamese FAQ Demo ===")
    
    vietnamese_questions = [
        "Dịch vụ Amazon EC2 Auto Scaling là gì",
        "Amazon EC2 Auto Scaling là gì?",
        "Auto Scaling là gì?",
        "EC2 Auto Scaling là gì?"
    ]
    
    for question in vietnamese_questions:
        print(f"\n--- Testing: {question} ---")
        
        try:
            # Load context
            context_result = load_context(question)
            print(f"Context Status: {context_result.status}")
            
            if context_result.status == "FOUND":
                # Generate answer
                answer = query("test_user", "", context_result.context, question)
                print(f"Answer: {answer}")
                
                # Check if it's a proper FAQ answer
                if "Amazon EC2 Auto Scaling is a fully managed service" in answer:
                    print("✅ SUCCESS: Vietnamese question matched English FAQ!")
                else:
                    print("⚠ Partial match or fallback answer")
            else:
                print("❌ No context found")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    demo_vietnamese_questions()
