#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interactive test for Vietnamese questions
"""

import sys
from context_manager.context import load_context, init_context
from chat_engine.query import query

def test_vietnamese_interactive():
    """Test Vietnamese questions interactively"""
    
    print("=== Test Vietnamese FAQ Interactive ===")
    
    # Initialize system
    init_context()
    
    # Test the exact questions from user's problem
    test_cases = [
        "Dịch vụ Amazon EC2 Auto Scaling là gì",
        "Amazon EC2 Auto Scaling là gì?",
        "What is Amazon EC2 Auto Scaling?"  # For comparison
    ]
    
    for question in test_cases:
        print(f"\n{'='*60}")
        print(f"Question: {question}")
        print(f"{'='*60}")
        
        # Step 1: Load context
        print("🔍 Searching for relevant context...")
        context_result = load_context(question)
        print(f"✓ Context Status: {context_result.status}")
        
        if context_result.status == "FOUND":
            print("✓ Relevant context found!")
            
            # Step 2: Generate answer
            print("🤖 Generating response...")
            answer = query("test_user", "", context_result.context, question)
            
            # Step 3: Display result
            print("\n--- AI Response ---")
            print(f"🤖 Answer: {answer}")
            
            # Check quality
            if "Amazon EC2 Auto Scaling is a fully managed service" in answer:
                print("\n🎉 ✅ SUCCESS: Perfect FAQ match!")
            elif "Amazon EC2 Auto Scaling" in answer:
                print("\n✅ Good: Contains relevant content")
            else:
                print("\n⚠ Warning: May not be from FAQ")
        
        else:
            print("❌ No context found")

if __name__ == "__main__":
    test_vietnamese_interactive()
