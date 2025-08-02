"""
Azure OpenAI Configuration
"""
from openai import AzureOpenAI
import os
import json
from typing import List

# Azure OpenAI Configuration

os.environ["AZURE_OPENAI_ENDPOINT"] = ""
os.environ["AZURE_OPENAI_API_KEY"] = ""
os.environ["AZURE_DEPLOYMENT_NAME"] = "GPT-4o-mini"


# API Version
API_VERSION = "2024-07-01-preview"

def get_openai_client():
    """
    Initialize and return Azure OpenAI client
    """
    try:
        # Create client with minimal parameters for Azure OpenAI
        client = AzureOpenAI(
            api_version=API_VERSION,
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY")
        )
        
        # Test the connection
        # Note: Just creating the client doesn't guarantee it works
        return client
        
    except Exception as e:
        print(f"Error initializing OpenAI client: {e}")
        print("Falling back to rule-based responses with FAQ database")
        return None

def call_openai_api(question: str, context: str = "", history: str = "") -> str:
    """
    Call Azure OpenAI API with question and context, supporting function calling
    
    Args:
        question: User's question
        context: System context/prompt
        history: Chat history for reference
        
    Returns:
        AI-generated response
    """
    client = get_openai_client()
    
    if client is None:
        return "I apologize, but I cannot connect to the AI service at the moment. Please try again later."
    
    # Import function definitions
    try:
        from function_definitions import get_function_list, execute_function
        functions_available = True
        function_list = get_function_list()
    except ImportError:
        functions_available = False
        function_list = []
    
    # Build system prompt
    system_prompt = f"""
You are a helpful AI assistant specialized in answering questions based on provided context with function calling capabilities.

Context Information:
{context if context else "No specific context provided."}

Previous Conversation:
{history if history else "No previous conversation."}

Instructions:
- Answer based on the provided context when relevant
- Use available functions when they can provide more accurate or specific information
- For FAQ questions, prioritize using the search_faq_database function
- For weather questions, use get_weather_info function
- For traffic questions, use get_traffic_info function  
- For restaurant questions, use recommend_restaurants function
- For AWS cost questions, use analyze_aws_costs function
- Be helpful and informative
- Support both English and Vietnamese languages
- Detect the language of the user's input and respond in the same language
"""

    try:
        # Prepare messages
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
        
        # Call API with or without functions
        if functions_available and function_list:
            response = client.chat.completions.create(
                model=os.getenv("AZURE_DEPLOYMENT_NAME"),
                messages=messages,
                tools=function_list,
                tool_choice="auto",
                temperature=0.3,
                max_tokens=500
            )
        else:
            response = client.chat.completions.create(
                model=os.getenv("AZURE_DEPLOYMENT_NAME"),
                messages=messages,
                temperature=0.3,
                max_tokens=500
            )
        
        # Handle function calls if present
        response_message = response.choices[0].message
        
        if hasattr(response_message, 'tool_calls') and response_message.tool_calls:
            # Execute function calls
            function_results = []
            
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                # Execute the function
                function_result = execute_function(function_name, function_args)
                function_results.append(f"Function {function_name} result: {function_result}")
            
            # Combine function results with original response
            combined_result = "\n".join(function_results)
            
            # Make another call to get final response with function results
            final_messages = messages + [
                {"role": "assistant", "content": f"I executed the following functions: {combined_result}"},
                {"role": "user", "content": "Based on the function results, please provide a comprehensive answer to my question."}
            ]
            
            final_response = client.chat.completions.create(
                model=os.getenv("AZURE_DEPLOYMENT_NAME"),
                messages=final_messages,
                temperature=0.3,
                max_tokens=500
            )
            
            return final_response.choices[0].message.content.strip()
        
        else:
            # No function calls, return normal response
            return response_message.content.strip()
        
    except Exception as e:
        return f"I apologize, but I encountered an error while processing your question: {str(e)}"

def call_openai_api_batch(questions: List[str], context: str = "", history: str = "") -> List[str]:
    """
    Call Azure OpenAI API with multiple questions in batch for efficiency
    
    Args:
        questions: List of user questions
        context: System context/prompt
        history: Chat history for reference
        
    Returns:
        List of AI-generated responses
    """
    client = get_openai_client()
    
    if client is None:
        return ["I apologize, but I cannot connect to the AI service at the moment. Please try again later."] * len(questions)
    
    # Import function definitions
    try:
        from function_definitions import get_function_list
        functions_available = True
        function_list = get_function_list()
    except ImportError:
        functions_available = False
        function_list = []
    
    # Build system prompt
    system_prompt = f"""
You are a helpful AI assistant specialized in answering questions based on provided context.

Context Information:
{context if context else "No specific context provided."}

Previous Conversation:
{history if history else "No previous conversation."}

Instructions:
- Answer each question accurately and concisely
- Use available functions when they can provide better information
- Support both English and Vietnamese languages
- Keep responses under 200 tokens each for efficiency
"""

    results = []
    
    try:
        # Process questions in batches of 5 for optimal performance
        batch_size = 5
        for i in range(0, len(questions), batch_size):
            batch_questions = questions[i:i + batch_size]
            batch_results = []
            
            for question in batch_questions:
                try:
                    messages = [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": question}
                    ]
                    
                    if functions_available and function_list:
                        response = client.chat.completions.create(
                            model=os.getenv("AZURE_DEPLOYMENT_NAME"),
                            messages=messages,
                            tools=function_list,
                            tool_choice="auto",
                            temperature=0.3,
                            max_tokens=200
                        )
                    else:
                        response = client.chat.completions.create(
                            model=os.getenv("AZURE_DEPLOYMENT_NAME"),
                            messages=messages,
                            temperature=0.3,
                            max_tokens=200
                        )
                    
                    batch_results.append(response.choices[0].message.content.strip() if response.choices[0].message.content else "No response generated")
                    
                except Exception as e:
                    batch_results.append(f"Error processing question: {str(e)}")
            
            results.extend(batch_results)
            
        return results
        
    except Exception as e:
        return [f"Batch processing error: {str(e)}"] * len(questions)
