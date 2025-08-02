"""
Test OpenAI Azure client connection
"""
import os
from openai import AzureOpenAI

# Set environment
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://aiportalapi.stu-platform.live/jpe"
os.environ["AZURE_OPENAI_API_KEY"] = "sk-SuGZEQ_HeMNrxDB0Myp4eQ"
os.environ["AZURE_DEPLOYMENT_NAME"] = "GPT-4o-mini"

def test_azure_client():
    """Test Azure OpenAI client initialization"""
    try:
        print("Testing Azure OpenAI client...")
        
        # Initialize client
        client = AzureOpenAI(
            api_version="2024-07-01-preview",
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY")
        )
        
        print("✅ Client initialized successfully")
        
        # Test a simple call
        response = client.chat.completions.create(
            model=os.getenv("AZURE_DEPLOYMENT_NAME"),
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say hello!"}
            ],
            max_tokens=50
        )
        
        print("✅ API call successful")
        print(f"Response: {response.choices[0].message.content}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"Error type: {type(e)}")

if __name__ == "__main__":
    test_azure_client()
