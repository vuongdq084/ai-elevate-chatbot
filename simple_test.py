"""
Simple test for Azure OpenAI without any other imports
"""

def test_simple():
    print("Testing simple Azure OpenAI import...")
    
    try:
        from openai import AzureOpenAI
        print("✅ Import successful")
        
        # Try to initialize with minimal parameters
        client = AzureOpenAI(
            api_version="2024-07-01-preview",
            azure_endpoint="https://aiportalapi.stu-platform.live/jpe",
            api_key="sk-SuGZEQ_HeMNrxDB0Myp4eQ"
        )
        print("✅ Client created successfully")
        
        # Just check if the client has expected attributes
        print(f"✅ Client type: {type(client)}")
        print("✅ All tests passed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simple()
