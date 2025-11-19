#!/usr/bin/env python3

"""
MCP Package Verification Script
Verifies that the MCP package is correctly installed and can be imported
"""

import sys
import importlib.util

def check_package(package_name):
    """Check if a package is installed and can be imported"""
    print(f"Checking if {package_name} is installed...")
    spec = importlib.util.find_spec(package_name)
    if spec is None:
        print(f"❌ {package_name} is NOT installed!")
        return False
    else:
        print(f"✅ {package_name} is installed!")
        
        # Try to import it
        try:
            module = importlib.import_module(package_name)
            if hasattr(module, '__version__'):
                print(f"   Version: {module.__version__}")
            print(f"✅ {package_name} imported successfully!")
            return True
        except Exception as e:
            print(f"❌ Error importing {package_name}: {str(e)}")
            return False

def main():
    """Main verification function"""
    print("=== MCP Package Verification ===\n")
    
    # Check Python version
    print(f"Python version: {sys.version}")
    
    # List of packages to check
    packages = ["mcp", "mcp.server", "mcp.types", "pyodbc", "dotenv"]
    
    # Check each package
    all_ok = True
    for package in packages:
        if not check_package(package):
            all_ok = False
        print("")
    
    # Summary
    if all_ok:
        print("✅ All required packages are installed and can be imported!")
        return 0
    else:
        print("❌ Some packages are missing or cannot be imported!")
        print("\nTry installing the required packages:")
        print("pip install mcp[client] pyodbc python-dotenv")
        return 1

if __name__ == "__main__":
    sys.exit(main())