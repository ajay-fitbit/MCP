#!/usr/bin/env python3

import os
import openai
from dotenv import load_dotenv

def test_openai_connection():
    """Test OpenAI API connection"""
    print("🔍 Testing OpenAI Connection")
    print("============================")
    
    # Load environment
    load_dotenv()
    
    # Get API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment variables")
        return False
    
    # Clean the API key
    api_key = api_key.strip('"\'')
    print(f"✅ API Key found: {api_key[:12]}...{api_key[-4:]}")
    
    try:
        # Initialize client
        client = openai.OpenAI(api_key=api_key)
        print("✅ OpenAI client initialized")
        
        # Test simple API call
        print("\n🔄 Testing simple API call...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Say 'Hello, World!' and nothing else."}
            ],
            max_tokens=10
        )
        
        result = response.choices[0].message.content
        print(f"✅ API Response: {result}")
        
        # Test model availability
        print("\n🔄 Testing model availability...")
        models_to_test = ["gpt-3.5-turbo", "gpt-4", "gpt-4o"]
        
        for model in models_to_test:
            try:
                test_response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": "Hi"}],
                    max_tokens=5
                )
                print(f"✅ {model}: Available")
            except Exception as e:
                error_msg = str(e)
                if "does not exist" in error_msg:
                    print(f"❌ {model}: Not available")
                elif "insufficient_quota" in error_msg:
                    print(f"⚠️  {model}: Quota exceeded")
                elif "rate_limit" in error_msg:
                    print(f"⚠️  {model}: Rate limited")
                else:
                    print(f"❌ {model}: {error_msg[:50]}...")
        
        # Test function calling
        print("\n🔄 Testing function calling...")
        try:
            func_response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": "What's the weather like? Use the get_weather function."}
                ],
                tools=[
                    {
                        "type": "function",
                        "function": {
                            "name": "get_weather",
                            "description": "Get the weather for a location",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "location": {"type": "string", "description": "The location"}
                                },
                                "required": ["location"]
                            }
                        }
                    }
                ],
                tool_choice="auto",
                max_tokens=100
            )
            
            if func_response.choices[0].message.tool_calls:
                print("✅ Function calling: Working")
            else:
                print("⚠️  Function calling: No function called")
                
        except Exception as e:
            print(f"❌ Function calling: {str(e)[:50]}...")
        
        print(f"\n🎉 OpenAI connection test completed!")
        print(f"\n📊 Summary:")
        print(f"   ✅ API Key: Valid")
        print(f"   ✅ Connection: Working")
        print(f"   ✅ Basic chat: Working")
        
        return True
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Connection failed: {error_msg}")
        
        if "invalid_api_key" in error_msg:
            print("\n💡 Solutions:")
            print("   1. Check your API key at: https://platform.openai.com/api-keys")
            print("   2. Make sure it starts with 'sk-'")
            print("   3. Ensure no extra quotes or spaces")
        elif "insufficient_quota" in error_msg:
            print("\n💡 Solutions:")
            print("   1. Check your billing at: https://platform.openai.com/account/billing")
            print("   2. Add payment method if needed")
            print("   3. Check usage limits")
        elif "rate_limit" in error_msg:
            print("\n💡 Solutions:")
            print("   1. Wait a few minutes and try again")
            print("   2. You may be hitting rate limits")
        else:
            print("\n💡 Solutions:")
            print("   1. Check internet connection")
            print("   2. Verify API key is correct")
            print("   3. Try again in a few minutes")
        
        return False

if __name__ == "__main__":
    success = test_openai_connection()
    input(f"\nPress Enter to continue...")
    exit(0 if success else 1)