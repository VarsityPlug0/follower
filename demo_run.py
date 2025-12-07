#!/usr/bin/env python3
"""
Demo Run Script for Instagram Automation Tool

This script demonstrates how to run the Instagram automation tool
with sample parameters and shows the expected output.
"""

import subprocess
import sys
import os

def main():
    print("Instagram Automation Tool - Demo Run")
    print("=" * 40)
    print()
    
    # Show the help information first
    print("1. Displaying help information:")
    print("-" * 30)
    
    try:
        result = subprocess.run([
            sys.executable, "instagram_automation.py", "--help"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print(result.stdout)
        else:
            print("Help command failed:")
            print(result.stderr)
            
    except subprocess.TimeoutExpired:
        print("Help command timed out")
    except Exception as e:
        print(f"Error running help command: {e}")
    
    print("\n" + "=" * 40)
    print("Demo run completed!")
    print()
    print("To run the actual Instagram automation tool:")
    print("python instagram_automation.py --username YOUR_USERNAME --password YOUR_PASSWORD --target TARGET_ACCOUNT")
    print()
    print("For production use with headless mode:")
    print("python instagram_automation.py --username YOUR_USERNAME --password YOUR_PASSWORD --target TARGET_ACCOUNT --headless")

if __name__ == "__main__":
    # Change to the follower directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()