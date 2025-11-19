#!/usr/bin/env python3

import os
import sys
import requests
import openai
from dotenv import load_dotenv
import time

def test_basic_connectivity():
    """Test basic internet connectivity"""
    print("🌐 Testing Internet Connectivity...")
    
    try:
        # Test basic internet
        response = requests.get("https://httpbin.org/ip", timeout=10)
        if response.status_code == 200:
            print("✅ Internet connection: Working")
            return True
        else:
            print(f"❌ Internet test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Internet connection failed: {str(e)}")
        return False

def test_openai_api():
    """Test OpenAI API specifically"""
    print("\n🤖 Testing OpenAI API...")
    
    try:
        # Test if we can reach OpenAI API
        response = requests.get("https://api.openai.com/v1/models", timeout=10)
        print(f"✅ OpenAI API reachable: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ Cannot reach OpenAI API: {str(e)}")
        return False

def test_openai_with_retry():
    """Test OpenAI with retry logic"""
    print("\n🔄 Testing OpenAI Client with Retry...")
    
    load_dotenv()
    
    # Get and clean API key
    api_key = os.getenv('OPENAI_API_KEY', '').strip('"\'')
    if not api_key:
        print("❌ No API key found")
        return False
    
    print(f"✅ API Key: {api_key[:12]}...{api_key[-4:]}")
    
    # Try with different configurations
    configs = [
        {"timeout": 30, "max_retries": 3},
        {"timeout": 60, "max_retries": 2},
        {"timeout": 120, "max_retries": 1}
    ]
    
    for i, config in enumerate(configs, 1):
        try:
            print(f"\n🔄 Attempt {i}: timeout={config['timeout']}s, retries={config['max_retries']}")
            
            # Create client with custom settings
            client = openai.OpenAI(
                api_key=api_key,
                timeout=config['timeout'],
                max_retries=config['max_retries']
            )
            
            # Simple test
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Say 'test'"}],
                max_tokens=5
            )
            
            result = response.choices[0].message.content
            print(f"✅ Success! Response: {result}")
            return True
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Attempt {i} failed: {error_msg[:100]}...")
            
            if "invalid_api_key" in error_msg.lower():
                print("🔑 API Key issue detected!")
                return False
            elif "insufficient_quota" in error_msg.lower():
                print("💳 Quota/billing issue detected!")
                return False
                
            time.sleep(2)  # Wait between attempts
    
    return False

def main():
    """Main diagnostic function"""
    print("🔍 OpenAI Connection Diagnostics")
    print("=================================")
    
    # Test 1: Basic connectivity
    if not test_basic_connectivity():
        print("\n❌ Basic internet connectivity failed!")
        print("Please check your internet connection and try again.")
        return False
    
    # Test 2: OpenAI API reachability
    if not test_openai_api():
        print("\n❌ Cannot reach OpenAI API!")
        print("This might be a firewall, proxy, or regional restriction issue.")
        return False
    
    # Test 3: OpenAI client with retry
    if test_openai_with_retry():
        print(f"\n🎉 OpenAI connection successful!")
        print(f"Your API key and connection are working.")
        return True
    else:
        print(f"\n❌ OpenAI connection failed after all attempts!")
        
        # Provide specific guidance
        print(f"\n💡 Troubleshooting steps:")
        print(f"1. Verify API key at: https://platform.openai.com/api-keys")
        print(f"2. Check billing at: https://platform.openai.com/account/billing")
        print(f"3. Ensure you have available credits")
        print(f"4. Try again in a few minutes (rate limiting)")
        print(f"5. Check if you're behind a corporate firewall")
        
        return False

if __name__ == "__main__":
    success = main()
    input(f"\nPress Enter to continue...")
    sys.exit(0 if success else 1)