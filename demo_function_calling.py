#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo Function Calling và Batching trong AI Elevate Chatbot
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from context_manager.context import load_context, init_context
from chat_engine.query import query, query_batch, analyze_question_intent

def demo_function_calling():
    """Demonstrate Function Calling capabilities"""
    
    print("=== Demo Function Calling ===")
    print("Testing AI's ability to call specific functions based on question type\n")
    
    # Initialize system
    init_context()
    
    # Test cases for different function types
    test_cases = [
        {
            "question": "What is Amazon EC2 Auto Scaling?",
            "expected_function": "search_faq_database",
            "description": "FAQ question - should call search_faq_database"
        },
        {
            "question": "Thời tiết hôm nay ở Hà Nội như thế nào?",
            "expected_function": "get_weather_info", 
            "description": "Weather question in Vietnamese - should call get_weather_info"
        },
        {
            "question": "Traffic in Ho Chi Minh City?",
            "expected_function": "get_traffic_info",
            "description": "Traffic question - should call get_traffic_info"
        },
        {
            "question": "Recommend good restaurants in Da Nang",
            "expected_function": "recommend_restaurants",
            "description": "Restaurant question - should call recommend_restaurants"
        },
        {
            "question": "What are the cost benefits of Auto Scaling?",
            "expected_function": "analyze_aws_costs",
            "description": "Cost analysis question - should call analyze_aws_costs"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test {i}: {test_case['description']} ---")
        print(f"Question: {test_case['question']}")
        
        # Analyze intent first
        intent_analysis = analyze_question_intent(test_case['question'])
        print(f"🧠 Intent Analysis:")
        print(f"   - Language: {intent_analysis['language']}")
        print(f"   - Intent: {intent_analysis['intent']}")
        print(f"   - Confidence: {intent_analysis['confidence']:.1f}")
        print(f"   - Recommended Function: {intent_analysis['recommended_function']}")
        print(f"   - Reasoning: {intent_analysis['reasoning']}")
        
        # Check if matches expected
        if intent_analysis['recommended_function'] == test_case['expected_function']:
            print("✅ Correct function recommendation!")
        else:
            print(f"⚠ Expected {test_case['expected_function']}, got {intent_analysis['recommended_function']}")
        
        # Get context and generate answer
        context_result = load_context(test_case['question'])
        if context_result.status == "FOUND":
            answer = query("demo_user", "", context_result.context, test_case['question'])
            print(f"🤖 Answer: {answer[:150]}...")
        
        print("-" * 60)

def demo_batching():
    """Demonstrate Batching capabilities"""
    
    print("\n=== Demo Batching ===")
    print("Testing AI's ability to process multiple questions efficiently\n")
    
    # Initialize system
    init_context()
    
    # Batch of questions for testing
    batch_questions = [
        "What is Amazon EC2 Auto Scaling?",
        "Lợi ích của Auto Scaling là gì?",
        "How does target tracking work?",
        "Weather in Hanoi today?",
        "Traffic situation in Ho Chi Minh City?",
        "Best restaurants in Da Nang?",
        "Cost analysis for t3.micro instances?",
        "When should I use AWS Auto Scaling vs EC2 Auto Scaling?"
    ]
    
    print(f"Processing {len(batch_questions)} questions:")
    for i, q in enumerate(batch_questions, 1):
        print(f"  {i}. {q}")
    
    print(f"\n🚀 Starting batch processing...")
    
    # Load context once for all questions
    context_result = load_context("AWS Auto Scaling FAQ batch processing")
    
    # Process in batch
    batch_answers = query_batch(
        user_id="demo_batch_user", 
        history="", 
        context=context_result.context if context_result.status == "FOUND" else "",
        questions=batch_questions
    )
    
    print(f"\n📊 Batch Results:")
    print(f"Questions processed: {len(batch_questions)}")
    print(f"Answers received: {len(batch_answers)}")
    
    # Display results
    for i, (question, answer) in enumerate(zip(batch_questions, batch_answers), 1):
        print(f"\n--- Batch Result {i} ---")
        print(f"Q: {question}")
        print(f"A: {answer[:100]}...")
        
        # Check if answer looks good
        if any(keyword in answer.lower() for keyword in ['amazon', 'auto scaling', 'temperature', 'traffic', 'restaurant']):
            print("✅ Relevant answer")
        else:
            print("⚠ Generic answer")

def demo_chain_of_thought():
    """Demonstrate Chain of Thought reasoning in question analysis"""
    
    print("\n=== Demo Chain of Thought (CoT) ===")
    print("Testing step-by-step reasoning for question analysis\n")
    
    # Complex questions that require reasoning
    complex_questions = [
        "Tôi đang xây dựng một ứng dụng web có lưu lượng truy cập thay đổi theo mùa. AWS Auto Scaling có thể giúp tôi tiết kiệm chi phí như thế nào?",
        "My application has unpredictable traffic spikes. Should I use EC2 Auto Scaling or AWS Auto Scaling, and what are the cost implications?",
        "Difference between fleet management and dynamic scaling in the context of cost optimization?",
        "Target tracking policy vs predictive scaling - which is better for variable workloads?"
    ]
    
    for i, question in enumerate(complex_questions, 1):
        print(f"\n--- CoT Analysis {i} ---")
        print(f"Question: {question}")
        
        # Step-by-step analysis
        analysis = analyze_question_intent(question)
        
        print(f"\n🧠 Chain of Thought Reasoning:")
        print(f"Step 1 - Language Detection: {analysis['language']}")
        print(f"Step 2 - Domain Classification: {analysis['intent']}")
        print(f"Step 3 - Confidence Assessment: {analysis['confidence']:.1f}")
        print(f"Step 4 - Function Selection: {analysis['recommended_function']}")
        print(f"Step 5 - Reasoning: {analysis['reasoning']}")
        
        # Generate answer using the reasoning
        context_result = load_context(question)
        if context_result.status == "FOUND":
            answer = query("demo_cot_user", "", context_result.context, question)
            print(f"\n🎯 Final Answer: {answer[:200]}...")
        
        print("-" * 80)

def demo_few_shot_learning():
    """Demonstrate Few-shot learning patterns"""
    
    print("\n=== Demo Few-shot Learning ===")
    print("Testing pattern recognition from examples\n")
    
    # Few-shot examples with patterns
    few_shot_examples = [
        # Pattern: "What is X?" questions
        ("What is Amazon EC2?", "AWS service definition"),
        ("What is Auto Scaling?", "AWS service definition"),
        ("EC2 là gì?", "Vietnamese service question"),
        
        # Pattern: "How to X?" questions  
        ("How to configure Auto Scaling?", "AWS configuration guide"),
        ("Làm sao để thiết lập Auto Scaling?", "Vietnamese how-to question"),
        
        # Pattern: "Benefits of X?" questions
        ("Benefits of using Auto Scaling?", "AWS benefits explanation"),
        ("Lợi ích của Auto Scaling?", "Vietnamese benefits question"),
        
        # New questions to test pattern recognition
        ("What is target tracking?", "Should recognize 'What is' pattern"),
        ("Lợi ích của target tracking là gì?", "Should recognize Vietnamese benefits pattern"),
        ("How to set up predictive scaling?", "Should recognize 'How to' pattern")
    ]
    
    print("📚 Few-shot Examples:")
    examples_by_pattern = {}
    
    for question, expected in few_shot_examples:
        analysis = analyze_question_intent(question)
        pattern = "unknown"
        
        if "what is" in question.lower() or "là gì" in question.lower():
            pattern = "definition_pattern"
        elif "how to" in question.lower() or "làm sao" in question.lower():
            pattern = "instruction_pattern"  
        elif "benefits" in question.lower() or "lợi ích" in question.lower():
            pattern = "benefits_pattern"
        
        if pattern not in examples_by_pattern:
            examples_by_pattern[pattern] = []
        examples_by_pattern[pattern].append((question, analysis, expected))
    
    # Display pattern recognition results
    for pattern, examples in examples_by_pattern.items():
        print(f"\n🎯 {pattern.replace('_', ' ').title()}:")
        for question, analysis, expected in examples:
            print(f"  Question: {question}")
            print(f"  Intent: {analysis['intent']} (confidence: {analysis['confidence']:.1f})")
            print(f"  Function: {analysis['recommended_function']}")
            print(f"  Expected: {expected}")
            print()

def main():
    """Run all demos"""
    
    print("🚀 AI Elevate Chatbot - Function Calling & Batching Demo")
    print("=" * 70)
    
    try:
        # Run all demo functions
        demo_function_calling()
        demo_batching()
        demo_chain_of_thought()
        demo_few_shot_learning()
        
        print("\n🎉 All demos completed successfully!")
        print("\n📊 Summary of implemented techniques:")
        print("✅ Function Calling - AI can call specific functions based on question type")
        print("✅ Batching - Process multiple questions efficiently")
        print("✅ Chain of Thought (CoT) - Step-by-step reasoning for question analysis")
        print("✅ Few-shot Learning - Pattern recognition from examples")
        print("✅ Multilingual Support - English and Vietnamese")
        
    except Exception as e:
        print(f"❌ Demo error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
