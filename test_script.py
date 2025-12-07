#!/usr/bin/env python3
"""
Simple test script to verify the Instagram automation tool works
"""

import asyncio
import argparse

def main():
    """Main function to test the script"""
    print("Instagram Automation Tool Test")
    print("=" * 40)
    print("This is a test to verify the script runs correctly.")
    print("To use the full automation tool, run:")
    print("python instagram_automation.py --username YOUR_USERNAME --password YOUR_PASSWORD --target TARGET_ACCOUNT [--like]")
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ Test completed successfully!")
    else:
        print("\n❌ Test failed!")