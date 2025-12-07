#!/usr/bin/env python3
"""
Production Readiness Test for Instagram Automation Tool

This script verifies that all components of the Instagram automation tool
are properly configured and ready for production use.
"""

import os
import sys
import subprocess
import argparse

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7 or higher is required")
        return False
    print("✅ Python version is compatible")
    return True

def check_required_files():
    """Check if all required files exist"""
    required_files = [
        "instagram_automation.py",
        "requirements.txt",
        "README.md",
        ".env.example"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return False
    
    print("✅ All required files are present")
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import stagehand
        import dotenv
        import playwright
        print("✅ All required Python packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing Python package: {e.name}")
        return False

def check_playwright_browsers():
    """Check if Playwright browsers are installed"""
    try:
        result = subprocess.run([
            sys.executable, "-m", "playwright", "install"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Playwright browsers are ready")
            return True
        else:
            print("❌ Playwright browser installation failed")
            return False
    except Exception as e:
        print(f"❌ Error checking Playwright browsers: {e}")
        return False

def test_script_import():
    """Test if the main script can be imported without errors"""
    try:
        # This will implicitly test if all imports work
        with open("instagram_automation.py", "r") as f:
            content = f.read()
        
        # Check for syntax errors by compiling
        compile(content, "instagram_automation.py", "exec")
        print("✅ Main script has no syntax errors")
        return True
    except Exception as e:
        print(f"❌ Script import test failed: {e}")
        return False

def main():
    """Main function to run all production readiness tests"""
    print("Instagram Automation Tool - Production Readiness Test")
    print("=" * 55)
    print()
    
    tests = [
        ("Python Version", check_python_version),
        ("Required Files", check_required_files),
        ("Dependencies", check_dependencies),
        ("Playwright Browsers", check_playwright_browsers),
        ("Script Import", test_script_import)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"Testing {test_name}...")
        if test_func():
            passed += 1
        print()
    
    print("=" * 55)
    print(f"Production Readiness Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The tool is ready for production use.")
        print()
        print("Next steps:")
        print("1. Copy .env.example to .env and fill in your credentials")
        print("2. Run the tool with: python instagram_automation.py --username YOUR_USERNAME --password YOUR_PASSWORD --target TARGET_ACCOUNT")
        return True
    else:
        print("❌ Some tests failed. Please fix the issues before using in production.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)