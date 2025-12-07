#!/usr/bin/env python3
"""
Debug Script for Instagram Automation

This script helps debug issues with finding elements on Instagram pages.
It opens Instagram and tries various selectors to see what works.
"""

import asyncio
import logging
import sys
from stagehand import Stagehand, StagehandConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug_instagram.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

async def debug_instagram_elements():
    """Debug Instagram element selectors"""
    logger.info("Starting Instagram element debugging...")
    
    # Configuration
    config = StagehandConfig(
        env="LOCAL",
        headless=False,  # Show browser window for debugging
        verbose=1,
    )
    
    stagehand = None
    try:
        # Initialize Stagehand
        logger.info("Initializing Stagehand...")
        stagehand = Stagehand(config)
        await stagehand.init()
        page = stagehand.page
        
        # Set viewport size
        await page.set_viewport_size({"width": 1920, "height": 1080})
        
        # Test 1: Go to Instagram homepage
        logger.info("=== TEST 1: Instagram Homepage ===")
        await page.goto("https://www.instagram.com/")
        await page.wait_for_timeout(5000)
        
        # Try to find various elements on the homepage
        elements_to_find = [
            ("Search input", "input[aria-label='Search input']"),
            ("Search placeholder", "input[placeholder='Search']"),
            ("Generic search", "input[type='text']"),
            ("Home link", "a[href='/']"),
            ("Home aria", "a[aria-label='Home']"),
            ("Home text", "a:has-text('Home')"),
            ("Login link", "a[href='/accounts/login/']"),
            ("Signup link", "a[href='/accounts/emailsignup/']"),
        ]
        
        for name, selector in elements_to_find:
            try:
                element = await page.query_selector(selector)
                if element:
                    logger.info(f"✅ FOUND: {name} with selector '{selector}'")
                else:
                    logger.info(f"❌ NOT FOUND: {name} with selector '{selector}'")
            except Exception as e:
                logger.info(f"❌ ERROR: {name} with selector '{selector}': {str(e)}")
        
        # Test 2: Go to login page
        logger.info("\n=== TEST 2: Instagram Login Page ===")
        await page.goto("https://www.instagram.com/accounts/login/")
        await page.wait_for_timeout(5000)
        
        login_elements = [
            ("Username input", "input[name='username']"),
            ("Username aria", "input[aria-label='Phone number, username, or email']"),
            ("Username generic", "input[type='text']"),
            ("Password input", "input[name='password']"),
            ("Password aria", "input[aria-label='Password']"),
            ("Password generic", "input[type='password']"),
            ("Login button", "button[type='submit']"),
            ("Login text", "button:has-text('Log in')"),
            ("Login text2", "button:has-text('Log In')"),
            ("Login text3", "button:has-text('Login')"),
        ]
        
        for name, selector in login_elements:
            try:
                element = await page.query_selector(selector)
                if element:
                    logger.info(f"✅ FOUND: {name} with selector '{selector}'")
                else:
                    logger.info(f"❌ NOT FOUND: {name} with selector '{selector}'")
            except Exception as e:
                logger.info(f"❌ ERROR: {name} with selector '{selector}': {str(e)}")
        
        # Test 3: Profile page example (you can change this to a real username)
        logger.info("\n=== TEST 3: Profile Page (Example) ===")
        test_username = "instagram"  # Change this to test with a real account
        await page.goto(f"https://www.instagram.com/{test_username}/")
        await page.wait_for_timeout(5000)
        
        profile_elements = [
            ("Profile header", "header"),
            ("Profile picture", "img[alt*='profile picture']"),
            ("Follow button", "button:has-text('Follow')"),
            ("Following button", "button:has-text('Following')"),
            ("Message button", "button:has-text('Message')"),
            ("Post links", "a[href^='/p/']"),
            ("Post images", "img[alt]"),
        ]
        
        for name, selector in profile_elements:
            try:
                elements = await page.query_selector_all(selector)
                if elements:
                    logger.info(f"✅ FOUND: {name} with selector '{selector}' ({len(elements)} elements)")
                else:
                    logger.info(f"❌ NOT FOUND: {name} with selector '{selector}'")
            except Exception as e:
                logger.info(f"❌ ERROR: {name} with selector '{selector}': {str(e)}")
        
        # Test 4: Post modal (click on a post first)
        logger.info("\n=== TEST 4: Post Modal Elements ===")
        logger.info("Manual step: Please click on a post to open the modal, then press Enter to continue...")
        input("Press Enter after clicking on a post...")
        
        post_modal_elements = [
            ("Like button", "section button:has(svg[aria-label='Like'])"),
            ("Like SVG", "svg[aria-label='Like']"),
            ("Liked SVG", "svg[aria-label='Unlike']"),
            ("Comment button", "section button:has(svg[aria-label='Comment'])"),
            ("Share button", "section button:has(svg[aria-label='Share'])"),
            ("Save button", "section button:has(svg[aria-label='Save'])"),
        ]
        
        for name, selector in post_modal_elements:
            try:
                element = await page.query_selector(selector)
                if element:
                    logger.info(f"✅ FOUND: {name} with selector '{selector}'")
                else:
                    logger.info(f"❌ NOT FOUND: {name} with selector '{selector}'")
            except Exception as e:
                logger.info(f"❌ ERROR: {name} with selector '{selector}': {str(e)}")
        
        logger.info("\n=== DEBUGGING COMPLETE ===")
        logger.info("Check debug_instagram.log for detailed results")
        
        return True
        
    except Exception as e:
        logger.error(f"Error during debugging: {str(e)}")
        return False
    finally:
        if stagehand:
            logger.info("Closing browser...")
            await stagehand.close()

def main():
    logger.info("Instagram Element Debugging Tool")
    logger.info("=" * 40)
    logger.info("This tool will help identify which selectors work on Instagram pages")
    logger.info("")
    
    # Run the async debug function
    success = asyncio.run(debug_instagram_elements())
    
    if success:
        logger.info("\n🎉 Debugging completed successfully!")
        logger.info("Review the log output to see which selectors work")
    else:
        logger.error("\n❌ Debugging failed!")

if __name__ == "__main__":
    main()