#!/usr/bin/env python3
"""
Quick test script for AI Elevate Chatbot
"""

def test_imports():
    """Test all module imports"""
    try:
        print("Testing imports...")
        
        # Test basic modules
        from user_manager.user import load_user, save_chat
        print("✓ User manager imported")
        
        from context_manager.context import load_context, init_context
        print("✓ Context manager imported")
        
        from chat_engine.query import query
        print("✓ Chat engine imported")
        
        # Test OpenAI config
        try:
            from config.openai_config import get_openai_client, call_openai_api
            print("✓ OpenAI config imported")
            openai_available = True
        except ImportError as e:
            print(f"⚠ OpenAI config import failed: {e}")
            openai_available = False
        
        # Test main module
        import main
        print("✓ Main module imported")
        
        return openai_available
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_basic_functionality():
    """Test basic system functionality"""
    try:
        print("\nTesting basic functionality...")
        
        # Test context initialization
        from context_manager.context import init_context
        init_context()
        print("✓ Context system initialized")
        
        # Test user loading (new user)
        from user_manager.user import load_user
        test_user_data = load_user("test_user")
        print(f"✓ User loading: {test_user_data.status}")
        
        # Test context loading
        from context_manager.context import load_context
        test_context = load_context("What is Amazon EC2 Auto Scaling?")
        print(f"✓ Context loading: {test_context.status}")
        
        # Test query processing
        from chat_engine.query import query
        test_answer = query("test_user", "", test_context.context, "What is AWS Auto Scaling?")
        print(f"✓ Query processing: {len(test_answer)} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Functionality error: {e}")
        return False

if __name__ == "__main__":
    print("=== AI Elevate Chatbot Test ===")
    
    # Test imports
    openai_ready = test_imports()
    
    # Test functionality
    func_ready = test_basic_functionality()
    
    print(f"\n=== Test Results ===")
    print(f"OpenAI Integration: {'✓ Ready' if openai_ready else '⚠ Fallback mode'}")
    print(f"Core Functionality: {'✓ Ready' if func_ready else '❌ Issues detected'}")
    
    if func_ready:
        print("\n🎉 System is ready! You can run:")
        print("   python main.py")
    else:
        print("\n❌ Please check the errors above before running the main application.")
