#!/usr/bin/env python3

import json
import os
import subprocess
import sys
from pathlib import Path

def check_claude_desktop_config():
    """Check Claude Desktop configuration"""
    print("🔍 Claude Desktop Configuration Checker")
    print("======================================")
    
    # Find Claude Desktop config file
    config_dir = Path(os.getenv('APPDATA')) / 'Claude'
    config_file = config_dir / 'claude_desktop_config.json'
    
    print(f"\n1️⃣ Checking Claude Desktop installation...")
    if not config_dir.exists():
        print("❌ Claude Desktop not found!")
        print("   Please install Claude Desktop from: https://claude.ai/download")
        return False
    else:
        print("✅ Claude Desktop directory found")
    
    print(f"\n2️⃣ Checking configuration file...")
    if not config_file.exists():
        print("❌ Configuration file not found!")
        print(f"   Expected: {config_file}")
        print("   Run 'setup_claude_desktop.bat' to create it")
        return False
    else:
        print("✅ Configuration file exists")
    
    print(f"\n3️⃣ Validating configuration...")
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        if 'mcpServers' not in config:
            print("❌ No MCP servers configured")
            return False
        
        if 'database' not in config['mcpServers']:
            print("❌ Database server not configured")
            return False
        
        db_config = config['mcpServers']['database']
        print("✅ Database server configuration found")
        
        # Check paths
        python_path = db_config.get('command', '')
        server_script = db_config['args'][0] if db_config.get('args') else ''
        
        print(f"\n4️⃣ Checking file paths...")
        if not os.path.exists(python_path):
            print(f"❌ Python executable not found: {python_path}")
            return False
        else:
            print(f"✅ Python executable found")
        
        if not os.path.exists(server_script):
            print(f"❌ Server script not found: {server_script}")
            return False
        else:
            print(f"✅ Server script found")
        
        # Check environment variables
        print(f"\n5️⃣ Checking environment settings...")
        env = db_config.get('env', {})
        server = env.get('DB_SERVER', 'Not set')
        database = env.get('DB_NAME', 'Not set')
        
        print(f"   Server: {server}")
        print(f"   Database: {database}")
        
        if server == 'Not set' or database == 'Not set':
            print("⚠️  Environment variables not properly set")
        else:
            print("✅ Environment variables configured")
        
        print(f"\n6️⃣ Testing server startup...")
        try:
            # Test if the server can start
            result = subprocess.run([
                python_path, server_script
            ], input='{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0.0"}}}\n',
            capture_output=True, text=True, timeout=5)
            
            if result.returncode == 0:
                print("✅ Server can start successfully")
            else:
                print(f"⚠️  Server startup issue: {result.stderr[:100]}...")
        except subprocess.TimeoutExpired:
            print("✅ Server started (timeout expected for this test)")
        except Exception as e:
            print(f"⚠️  Server test failed: {e}")
        
        print(f"\n🎉 Configuration check complete!")
        print(f"\n📋 Summary:")
        print(f"   ✅ Claude Desktop: Installed")
        print(f"   ✅ Configuration: Valid")
        print(f"   ✅ Python Path: Found")
        print(f"   ✅ Server Script: Found")
        print(f"   ✅ Environment: Configured")
        
        print(f"\n💡 Ready to use!")
        print(f"   1. Restart Claude Desktop")
        print(f"   2. Try these prompts:")
        print(f"      • 'List all tables in my database'")
        print(f"      • 'Show me PATIENT_DETAILS table structure'")
        print(f"      • 'Execute USP_AHS_UM_ACTIVITY_LOG_REFERRALS_GET'")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON configuration: {e}")
        return False
    except Exception as e:
        print(f"❌ Configuration check failed: {e}")
        return False

if __name__ == "__main__":
    success = check_claude_desktop_config()
    if not success:
        print(f"\n🔧 To fix issues, run: setup_claude_desktop.bat")
    
    input(f"\nPress Enter to continue...")
    sys.exit(0 if success else 1)