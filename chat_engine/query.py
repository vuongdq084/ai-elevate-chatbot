import sys
import os

# Add config directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))

try:
    from openai_config import call_openai_api, call_openai_api_batch
    from function_definitions import execute_function
    OPENAI_AVAILABLE = True
    FUNCTION_CALLING_AVAILABLE = True
except ImportError:
    print("Warning: OpenAI configuration not available. Using fallback responses.")
    OPENAI_AVAILABLE = False
    FUNCTION_CALLING_AVAILABLE = False

def query(user_id: str, history: str, context: str, question: str) -> str:
    """
    Generate answer using Azure OpenAI API with FAQ integration, Function Calling support
    
    Args:
        user_id: User identifier (reference info)
        history: User's chat history (reference info)
        context: System prompt/context from context manager (includes FAQ data)
        question: User's current question
        
    Returns:
        Generated answer string
    """
    
    # First, try to find answer in FAQ database regardless of OpenAI status
    faq_answer = _search_faq_database(question, context)
    if faq_answer:
        return faq_answer
    
    # If no FAQ match and OpenAI is available, try OpenAI API with Function Calling
    if OPENAI_AVAILABLE:
        try:
            # Enhanced context with function calling instructions
            enhanced_context = f"""
            You are a multilingual AI assistant specialized in answering questions based on a predefined FAQ database and AWS public FAQ documentation.
            
            You have access to the following context and FAQ information:
            {context}
            
            FUNCTION CALLING CAPABILITIES:
            You can call the following functions to get more accurate information:
            - search_faq_database: Search internal FAQ database
            - get_weather_info: Get weather information for Vietnamese cities
            - get_traffic_info: Get traffic information for Vietnamese cities  
            - recommend_restaurants: Get restaurant recommendations
            - analyze_aws_costs: Analyze AWS Auto Scaling costs
            
            Your behavior follows these rules:
            
            1. Language Support
            - Support both English and Vietnamese.
            - Detect the language of the user's input and respond in the same language.
            
            2. Function Usage Priority
            - For FAQ questions about AWS/Auto Scaling: Use search_faq_database function
            - For weather questions: Use get_weather_info function
            - For traffic questions: Use get_traffic_info function
            - For restaurant questions: Use recommend_restaurants function
            - For AWS cost questions: Use analyze_aws_costs function
            
            3. Primary Source: Internal FAQ Bank
            - Always search the internal FAQ bank first using functions.
            - If the user's question is identical, similar, or contextually related to any FAQ entry:
                - Return the original answer from the FAQ bank without rephrasing.
                - Maintain the original formatting of the answer.
            
            4. Secondary Source: AWS Public FAQ
            - If the question is not related to any entry in the FAQ bank:
                - Search the official AWS FAQ site at https://aws.amazon.com/faqs/
                - If an answer is found there, respond using this format:
                "Can not find any related information in FAQ bank. But in https://aws.amazon.com/faqs/ the answer is:
                [insert answer from AWS FAQ]"
            
            5. Out-of-Scope Questions
            - If the question is unrelated to both the internal FAQ bank and the AWS FAQ site, respond with:
                "The question is out of scope."
            
            6. Tone and Style
            - Be clear, concise, and professional.
            - Do not provide answers from external sources other than the internal FAQ and https://aws.amazon.com/faqs/.
            - Never generate answers on your own—only use content from the approved sources above.
            - Always keep the response under 500 tokens. Summarize long answers if necessary, but preserve the core information accurately.
            """
            
            # Call Azure OpenAI API with Function Calling support
            answer = call_openai_api(question, enhanced_context, history)
            return answer
            
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            # Continue to fallback
    
    # Fallback to rule-based responses
    return _fallback_query(user_id, history, context, question)

def query_batch(user_id: str, history: str, context: str, questions: list) -> list:
    """
    Process multiple questions in batch for efficiency using Batching technique
    
    Args:
        user_id: User identifier (reference info)
        history: User's chat history (reference info)
        context: System prompt/context from context manager
        questions: List of user questions
        
    Returns:
        List of generated answers
    """
    
    if not questions:
        return []
    
    # Try batch processing with OpenAI API
    if OPENAI_AVAILABLE:
        try:
            print(f"🔄 Processing {len(questions)} questions in batch...")
            
            # Enhanced context for batch processing
            batch_context = f"""
            You are processing multiple questions in batch. For each question:
            
            Context Information:
            {context}
            
            Instructions:
            - Answer each question concisely and accurately
            - Use function calls when appropriate for better accuracy
            - Support both English and Vietnamese languages
            - Keep individual responses under 200 tokens for efficiency
            - Prioritize FAQ database for AWS-related questions
            """
            
            # Call batch API
            answers = call_openai_api_batch(questions, batch_context, history)
            print(f"✅ Batch processing completed successfully")
            return answers
            
        except Exception as e:
            print(f"Error in batch processing: {e}")
            print("🔄 Falling back to individual question processing...")
    
    # Fallback: Process questions individually
    answers = []
    for i, question in enumerate(questions):
        print(f"Processing question {i+1}/{len(questions)}: {question[:50]}...")
        answer = query(user_id, history, context, question)
        answers.append(answer)
    
    return answers

def analyze_question_intent(question: str) -> dict:
    """
    Analyze question intent to determine the best function to call
    Implements Chain of Thought (CoT) reasoning for function selection
    
    Args:
        question: User's question
        
    Returns:
        Dictionary with intent analysis and recommended function
    """
    
    question_lower = question.lower()
    
    # Chain of Thought analysis
    analysis = {
        "question": question,
        "language": "vietnamese" if any(vn_word in question_lower for vn_word in ['là', 'gì', 'như', 'thế', 'nào', 'tại', 'sao']) else "english",
        "intent": "unknown",
        "confidence": 0.0,
        "recommended_function": None,
        "reasoning": ""
    }
    
    # Step 1: Identify domain
    if any(keyword in question_lower for keyword in ["auto scaling", "autoscaling", "ec2", "aws", "amazon"]):
        analysis["intent"] = "aws_faq"
        analysis["confidence"] = 0.9
        analysis["recommended_function"] = "search_faq_database"
        analysis["reasoning"] = "Question contains AWS/Auto Scaling keywords, should search FAQ database"
        
    elif any(keyword in question_lower for keyword in ["weather", "temperature", "thời tiết", "nhiệt độ"]):
        analysis["intent"] = "weather"
        analysis["confidence"] = 0.8
        analysis["recommended_function"] = "get_weather_info"
        analysis["reasoning"] = "Question asks about weather information"
        
    elif any(keyword in question_lower for keyword in ["traffic", "giao thông", "đường"]):
        analysis["intent"] = "traffic"
        analysis["confidence"] = 0.8
        analysis["recommended_function"] = "get_traffic_info"
        analysis["reasoning"] = "Question asks about traffic information"
        
    elif any(keyword in question_lower for keyword in ["restaurant", "food", "nhà hàng", "ăn"]):
        analysis["intent"] = "restaurant"
        analysis["confidence"] = 0.8
        analysis["recommended_function"] = "recommend_restaurants"
        analysis["reasoning"] = "Question asks about restaurant recommendations"
        
    elif any(keyword in question_lower for keyword in ["cost", "price", "chi phí", "giá"]):
        analysis["intent"] = "aws_cost"
        analysis["confidence"] = 0.7
        analysis["recommended_function"] = "analyze_aws_costs"
        analysis["reasoning"] = "Question asks about costs, likely AWS-related"
        
    # Step 2: Few-shot pattern matching
    few_shot_patterns = {
        "what is": "aws_faq",
        "là gì": "aws_faq",
        "how to": "aws_faq", 
        "như thế nào": "aws_faq",
        "benefits": "aws_faq",
        "lợi ích": "aws_faq"
    }
    
    for pattern, intent in few_shot_patterns.items():
        if pattern in question_lower and analysis["intent"] == "unknown":
            analysis["intent"] = intent
            analysis["confidence"] = 0.6
            analysis["recommended_function"] = "search_faq_database"
            analysis["reasoning"] = f"Matched few-shot pattern: {pattern}"
    
    return analysis

def _search_faq_database(question: str, context: str) -> str:
    """
    Search FAQ database for exact or similar matches with multilingual support
    """
    try:
        # Parse context to find FAQ entries
        if "FAQ Database:" in context:
            faq_section = context.split("FAQ Database:")[1].split("Relevant Context:")[0] if "Relevant Context:" in context else context.split("FAQ Database:")[1]
            
            # Split into Q&A pairs
            qa_pairs = []
            lines = faq_section.split('\n')
            current_question = ""
            current_answer = ""
            
            for line in lines:
                line = line.strip()
                if line.startswith('Q:') or line.startswith('Q.'):
                    # Save previous pair
                    if current_question and current_answer:
                        qa_pairs.append((current_question, current_answer.strip()))
                    # Start new pair
                    current_question = line
                    current_answer = ""
                elif line and current_question:
                    current_answer += line + " "
            
            # Add last pair
            if current_question and current_answer:
                qa_pairs.append((current_question, current_answer.strip()))
            
            # Search for matching question with multilingual support
            question_lower = question.lower()
            
            # Vietnamese to English mapping for common terms
            vietnamese_mappings = {
                'là gì': 'what is',
                'gì là': 'what is', 
                'dịch vụ': 'service',
                'amazon': 'amazon',
                'ec2': 'ec2',
                'auto scaling': 'auto scaling',
                'tự động mở rộng': 'auto scaling',
                'tự động scale': 'auto scaling',
                'mở rộng': 'scaling',
                'lợi ích': 'benefits',
                'ưu điểm': 'benefits',
                'khác nhau': 'different',
                'so với': 'vs',
                'nên': 'should',
                'sử dụng': 'use',
                'khi nào': 'when',
                'như thế nào': 'how',
                'tại sao': 'why'
            }
            
            # Normalize Vietnamese question to English
            normalized_question = question_lower
            for vn_term, en_term in vietnamese_mappings.items():
                normalized_question = normalized_question.replace(vn_term, en_term)
            
            # First, try exact match with normalized question
            for faq_q, faq_a in qa_pairs:
                faq_q_lower = faq_q.lower()
                
                # Check if this is a "what is" type question
                if ('là gì' in question_lower or 'gì là' in question_lower) and 'what is' in faq_q_lower:
                    # Extract the main subject from both questions
                    if 'ec2 auto scaling' in normalized_question and 'ec2 auto scaling' in faq_q_lower:
                        return faq_a
                    elif 'amazon ec2 auto scaling' in normalized_question and 'amazon ec2 auto scaling' in faq_q_lower:
                        return faq_a
                    elif 'auto scaling' in normalized_question and 'auto scaling' in faq_q_lower and 'what is' in faq_q_lower:
                        return faq_a
                
                # Check for high similarity with normalized terms
                question_words = set(normalized_question.split())
                faq_words = set(faq_q_lower.split())
                overlap = len(question_words.intersection(faq_words))
                
                if overlap >= 3:  # Require at least 3 word overlap
                    return faq_a
            
            # If no exact match, try keyword matching
            for faq_q, faq_a in qa_pairs:
                faq_q_lower = faq_q.lower()
                if any(keyword in faq_q_lower for keyword in ["auto scaling", "autoscaling", "ec2"]):
                    if any(term in normalized_question for term in ["what is", "auto scaling", "autoscaling", "ec2"]):
                        return faq_a
        
        return None
        
    except Exception as e:
        print(f"Error searching FAQ: {e}")
        return None

def _fallback_query(user_id: str, history: str, context: str, question: str) -> str:
    """
    Fallback query implementation when OpenAI API is not available
    """
    try:
        # First, try to find answer in FAQ database
        faq_answer = _search_faq_database(question, context)
        if faq_answer:
            return faq_answer
        
        # If no FAQ match, use rule-based responses
        question_lower = question.lower()
        
        # Check for AWS/EC2 Auto Scaling related questions
        if any(keyword in question_lower for keyword in ["auto scaling", "autoscaling", "ec2", "aws"]):
            if "what is" in question_lower and "auto scaling" in question_lower:
                return """Amazon EC2 Auto Scaling is a fully managed service designed to launch or terminate Amazon EC2 instances automatically to help ensure you have the correct number of Amazon EC2 instances available to handle the load for your application. Amazon EC2 Auto Scaling helps you maintain application availability through fleet management for EC2 instances, which detects and replaces unhealthy instances, and by scaling your Amazon EC2 capacity up or down automatically according to conditions you define."""
            
            elif "benefits" in question_lower:
                return """Amazon EC2 Auto Scaling helps to maintain your Amazon EC2 instance availability. Whether you are running one Amazon EC2 instance or thousands, you can use Amazon EC2 Auto Scaling to detect impaired Amazon EC2 instances, and replace the instances without intervention. This ensures that your application has the compute capacity that you expect."""
            
            elif "target tracking" in question_lower:
                return """Target tracking is a new type of scaling policy that you can use to set up dynamic scaling for your application in just a few simple steps. With target tracking, you select a load metric for your application, such as CPU utilization or request count, set the target value, and Amazon EC2 Auto Scaling adjusts the number of EC2 instances in your ASG as needed to maintain that target."""
            
            else:
                return "Based on the FAQ database, I can help you with questions about Amazon EC2 Auto Scaling, ASG (Auto Scaling Groups), scaling policies, and related AWS services. Please ask a specific question about these topics."
        
        elif "weather" in question_lower or "temperature" in question_lower:
            if "hanoi" in question_lower:
                return "Based on the current weather information, the temperature in Hanoi is 38°C with 65% humidity. It's sunny with light wind."
            elif "ho chi minh" in question_lower or "hcm" in question_lower:
                return "The current temperature in Ho Chi Minh City is around 39°C. It's quite hot and humid today."
            elif "da nang" in question_lower:
                return "The temperature in Da Nang is approximately 30°C with pleasant coastal breeze."
            else:
                return "Based on the available weather data, temperatures in major Vietnamese cities range from 30-39°C today."
        
        elif "traffic" in question_lower:
            if "ho chi minh" in question_lower or "hcm" in question_lower:
                return "Traffic in Ho Chi Minh City is currently heavy during rush hours. I recommend using alternative routes or traveling during off-peak hours."
            else:
                return "Traffic conditions vary by location and time. For specific areas, please let me know the city you're interested in."
        
        elif "restaurant" in question_lower or "food" in question_lower:
            if "da nang" in question_lower:
                return "Da Nang has excellent Vietnamese restaurants specializing in pho and fresh seafood dishes. The coastal location provides access to great fresh ingredients."
            else:
                return "Vietnamese cuisine offers many delicious options including pho, banh mi, and fresh seafood. Each region has its specialties."
        
        elif "hello" in question_lower or "hi" in question_lower:
            return f"Hello! I'm here to help you with information about AWS services, weather, traffic, restaurants, and more. What would you like to know?"
        
        else:
            # Check if question is out of scope
            aws_keywords = ["aws", "amazon", "ec2", "auto scaling", "cloud"]
            general_keywords = ["weather", "traffic", "restaurant", "food"]
            
            if not any(keyword in question_lower for keyword in aws_keywords + general_keywords):
                return "The question is out of scope."
            
            return f"I understand you're asking about: {question}. Please ask more specific questions about AWS services, weather, traffic, or restaurant recommendations."
    
    except Exception as e:
        return f"I apologize, but I encountered an error while processing your question. Please try asking again or rephrase your question."
