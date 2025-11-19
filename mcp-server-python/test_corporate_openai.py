#!/usr/bin/env python3

import os
import sys
import ssl
import urllib3
import openai
from dotenv import load_dotenv

# Disable SSL warnings for corporate environments
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_openai_corporate_environment():
    """Test OpenAI in corporate environment with SSL workarounds"""
    print("🏢 Testing OpenAI in Corporate Environment")
    print("==========================================")
    
    load_dotenv()
    
    # Get API key
    api_key = os.getenv('OPENAI_API_KEY', '').strip('"\'')
    if not api_key:
        print("❌ No API key found")
        return False
    
    print(f"✅ API Key: {api_key[:12]}...{api_key[-4:]}")
    
    try:
        import openai
        
        # Create client with SSL workarounds for corporate environments
        print("\n🔄 Testing with corporate-friendly settings...")
        
        # Method 1: Try with default settings first
        try:
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Say 'Hello'"}],
                max_tokens=5,
                timeout=30
            )
            result = response.choices[0].message.content
            print(f"✅ Method 1 (default): Success! Response: {result}")
            return True
        except Exception as e1:
            print(f"⚠️  Method 1 failed: {str(e1)[:100]}...")
        
        # Method 2: Try with custom HTTP client for proxy/SSL issues
        try:
            import httpx
            
            # Create custom HTTP client that handles corporate environments
            http_client = httpx.Client(
                verify=False,  # Disable SSL verification
                timeout=60.0
            )
            
            client = openai.OpenAI(
                api_key=api_key,
                http_client=http_client
            )
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Say 'Hello'"}],
                max_tokens=5
            )
            result = response.choices[0].message.content
            print(f"✅ Method 2 (SSL disabled): Success! Response: {result}")
            return True
            
        except ImportError:
            print("⚠️  httpx not available, installing...")
            os.system(f'"{sys.executable}" -m pip install httpx')
            
        except Exception as e2:
            print(f"⚠️  Method 2 failed: {str(e2)[:100]}...")
        
        # Method 3: Environment variable approach
        try:
            # Set environment variables to bypass SSL
            os.environ['CURL_CA_BUNDLE'] = ''
            os.environ['REQUESTS_CA_BUNDLE'] = ''
            
            # Try again with environment variables set
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Say 'Hello'"}],
                max_tokens=5,
                timeout=60
            )
            result = response.choices[0].message.content
            print(f"✅ Method 3 (env vars): Success! Response: {result}")
            return True
            
        except Exception as e3:
            print(f"⚠️  Method 3 failed: {str(e3)[:100]}...")
        
        print(f"\n❌ All methods failed!")
        print(f"\n💡 Corporate Environment Solutions:")
        print(f"1. Ask IT to whitelist: api.openai.com")
        print(f"2. Configure proxy settings if needed")
        print(f"3. Try from a different network (home/mobile)")
        print(f"4. Use VPN if allowed by your organization")
        
        return False
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        return False

def create_corporate_openai_client():
    """Create an OpenAI client that works in corporate environments"""
    load_dotenv()
    
    api_key = os.getenv('OPENAI_API_KEY', '').strip('"\'')
    if not api_key:
        raise ValueError("No API key found")
    
    try:
        import httpx
        
        # Create HTTP client that bypasses SSL verification
        http_client = httpx.Client(
            verify=False,
            timeout=60.0
        )
        
        return openai.OpenAI(
            api_key=api_key,
            http_client=http_client
        )
    except ImportError:
        # Fallback to regular client
        return openai.OpenAI(api_key=api_key)

if __name__ == "__main__":
    success = test_openai_corporate_environment()
    
    if success:
        print(f"\n🎉 OpenAI is working in your environment!")
        print(f"You can now use the OpenAI database chat.")
    else:
        print(f"\n❌ OpenAI connection issues detected.")
        print(f"This is likely due to corporate firewall/proxy settings.")
    
    input(f"\nPress Enter to continue...")
    sys.exit(0 if success else 1)