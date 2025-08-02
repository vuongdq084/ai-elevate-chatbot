"""
Function calling definitions for AI chatbot
"""

import json
from typing import Dict, List, Any

# Define available functions for the AI to call
AVAILABLE_FUNCTIONS = {
    "search_faq_database": {
        "type": "function",
        "function": {
            "name": "search_faq_database",
            "description": "Search the internal FAQ database for AWS Auto Scaling questions and answers",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to find relevant FAQ entries"
                    },
                    "language": {
                        "type": "string",
                        "enum": ["english", "vietnamese"],
                        "description": "The language of the query (english or vietnamese)"
                    }
                },
                "required": ["query"]
            }
        }
    },
    "get_weather_info": {
        "type": "function",
        "function": {
            "name": "get_weather_info",
            "description": "Get current weather information for Vietnamese cities",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "enum": ["hanoi", "ho_chi_minh", "da_nang"],
                        "description": "The city to get weather information for"
                    }
                },
                "required": ["city"]
            }
        }
    },
    "get_traffic_info": {
        "type": "function",
        "function": {
            "name": "get_traffic_info",
            "description": "Get current traffic information for Vietnamese cities",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "enum": ["hanoi", "ho_chi_minh", "da_nang"],
                        "description": "The city to get traffic information for"
                    }
                },
                "required": ["city"]
            }
        }
    },
    "recommend_restaurants": {
        "type": "function",
        "function": {
            "name": "recommend_restaurants",
            "description": "Get restaurant recommendations for Vietnamese cities",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "enum": ["hanoi", "ho_chi_minh", "da_nang"],
                        "description": "The city to get restaurant recommendations for"
                    },
                    "cuisine_type": {
                        "type": "string",
                        "enum": ["vietnamese", "seafood", "pho", "any"],
                        "description": "Type of cuisine preferred"
                    }
                },
                "required": ["city"]
            }
        }
    },
    "analyze_aws_costs": {
        "type": "function",
        "function": {
            "name": "analyze_aws_costs",
            "description": "Analyze AWS Auto Scaling cost implications and recommendations",
            "parameters": {
                "type": "object",
                "properties": {
                    "instance_type": {
                        "type": "string",
                        "description": "EC2 instance type (e.g., t3.micro, m5.large)"
                    },
                    "expected_load": {
                        "type": "string",
                        "enum": ["low", "medium", "high", "variable"],
                        "description": "Expected application load pattern"
                    }
                },
                "required": ["expected_load"]
            }
        }
    }
}

def execute_function(function_name: str, arguments: Dict[str, Any]) -> str:
    """
    Execute the specified function with given arguments
    
    Args:
        function_name: Name of the function to execute
        arguments: Arguments to pass to the function
        
    Returns:
        Function execution result as string
    """
    
    if function_name == "search_faq_database":
        return _search_faq_function(arguments.get("query", ""), arguments.get("language", "english"))
    
    elif function_name == "get_weather_info":
        return _get_weather_function(arguments.get("city", "hanoi"))
    
    elif function_name == "get_traffic_info":
        return _get_traffic_function(arguments.get("city", "hanoi"))
    
    elif function_name == "recommend_restaurants":
        return _recommend_restaurants_function(
            arguments.get("city", "hanoi"), 
            arguments.get("cuisine_type", "any")
        )
    
    elif function_name == "analyze_aws_costs":
        return _analyze_aws_costs_function(
            arguments.get("instance_type", "t3.micro"),
            arguments.get("expected_load", "medium")
        )
    
    else:
        return f"Unknown function: {function_name}"

def _search_faq_function(query: str, language: str) -> str:
    """Search FAQ database function implementation"""
    # This would integrate with the existing FAQ search logic
    try:
        from context_manager.context import load_context
        context_result = load_context(query)
        if context_result.status == "FOUND":
            return f"FAQ search successful. Found relevant information for query: {query}"
        else:
            return "No relevant FAQ entries found for this query."
    except Exception as e:
        return f"Error searching FAQ: {str(e)}"

def _get_weather_function(city: str) -> str:
    """Get weather information function implementation"""
    weather_data = {
        "hanoi": "Current temperature in Hanoi is 38°C with 65% humidity. It's sunny with light wind.",
        "ho_chi_minh": "Current temperature in Ho Chi Minh City is 39°C with 70% humidity. Hot and humid.",
        "da_nang": "Current temperature in Da Nang is 30°C with pleasant coastal breeze."
    }
    return weather_data.get(city, "Weather information not available for this city.")

def _get_traffic_function(city: str) -> str:
    """Get traffic information function implementation"""
    traffic_data = {
        "hanoi": "Traffic in Hanoi is moderate with some congestion in the city center.",
        "ho_chi_minh": "Traffic in Ho Chi Minh City is heavy during rush hours. Alternative routes recommended.",
        "da_nang": "Traffic in Da Nang is generally light with good flow on main roads."
    }
    return traffic_data.get(city, "Traffic information not available for this city.")

def _recommend_restaurants_function(city: str, cuisine_type: str) -> str:
    """Get restaurant recommendations function implementation"""
    recommendations = {
        "hanoi": {
            "vietnamese": "Top Vietnamese restaurants in Hanoi: Pho Gia Truyen, Bun Cha Huong Lien",
            "pho": "Best pho in Hanoi: Pho Bat Dan, Pho Thin, Pho Gia Truyen",
            "any": "Popular restaurants in Hanoi include traditional pho shops and French-influenced cuisine"
        },
        "ho_chi_minh": {
            "vietnamese": "Top Vietnamese restaurants in Ho Chi Minh City: Nha Hang Ngon, Com Nieu Saigon",
            "seafood": "Best seafood in Ho Chi Minh City: Oc Thanh Da, Quan 94",
            "any": "Ho Chi Minh City offers diverse dining from street food to upscale restaurants"
        },
        "da_nang": {
            "seafood": "Top seafood restaurants in Da Nang specialize in fresh coastal dishes",
            "vietnamese": "Da Nang offers excellent local specialties like Mi Quang and Cao Lau",
            "any": "Da Nang is famous for fresh seafood and unique local dishes"
        }
    }
    return recommendations.get(city, {}).get(cuisine_type, f"Restaurant recommendations not available for {city}")

def _analyze_aws_costs_function(instance_type: str, expected_load: str) -> str:
    """Analyze AWS costs function implementation"""
    cost_analysis = {
        "low": f"For {instance_type} with low load: Auto Scaling can reduce costs by 20-40% by scaling down during low usage periods.",
        "medium": f"For {instance_type} with medium load: Auto Scaling provides balanced cost optimization with 15-30% savings.",
        "high": f"For {instance_type} with high load: Auto Scaling ensures performance while optimizing costs during peak/off-peak cycles.",
        "variable": f"For {instance_type} with variable load: Auto Scaling is highly beneficial, potentially saving 30-50% in costs."
    }
    return cost_analysis.get(expected_load, "Cost analysis not available for this load pattern.")

def get_function_list() -> List[Dict]:
    """Get list of available functions for OpenAI function calling"""
    return list(AVAILABLE_FUNCTIONS.values())
