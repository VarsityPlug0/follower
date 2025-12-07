#!/usr/bin/env python3
"""
Instagram Automation Tool using Stagehand

This script automates Instagram actions like following accounts and liking posts
using the Stagehand browser automation framework.
"""

import asyncio
import os
import argparse
import logging
import sys
from datetime import datetime
from dotenv import load_dotenv
from stagehand import Stagehand, StagehandConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('instagram_automation.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class InstagramAutomationError(Exception):
    """Custom exception for Instagram automation errors"""
    pass

async def login_to_instagram(page, username, password):
    """Log into Instagram with provided credentials"""
    logger.info(f"Logging into Instagram as {username}...")
    
    try:
        # Navigate to Instagram login page
        await page.goto("https://www.instagram.com/accounts/login/")
        
        # Wait for the page to load
        await page.wait_for_timeout(3000)
        
        # Fill in credentials using Playwright directly (no LLM needed)
        await page.fill("input[name='username']", username)
        await page.fill("input[name='password']", password)
        
        # Click login button
        await page.click("button[type='submit']")
        
        # Wait for navigation
        await page.wait_for_timeout(5000)
        
        # Check if login was successful
        current_url = page.url
        if "login" in current_url and "challenge" not in current_url:
            # Check for error message
            error_elements = await page.query_selector_all("div:has-text('Sorry, your password was incorrect')")
            if error_elements:
                raise InstagramAutomationError("Login failed: Incorrect credentials")
        
        logger.info("Login successful!")
        return True
        
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        raise InstagramAutomationError(f"Failed to login: {str(e)}")

async def follow_account(page, target_username):
    """Follow a target account"""
    logger.info(f"Following {target_username}...")
    
    try:
        # Navigate to target account
        await page.goto(f"https://www.instagram.com/{target_username}/")
        
        # Wait for page to load
        await page.wait_for_timeout(3000)
        
        # Look for Follow button
        follow_button_selectors = [
            "button:has-text('Follow')",
            "button:has-text('Follow Back')",
            "_acan _acao _acas",
        ]
        
        follow_button = None
        for selector in follow_button_selectors:
            try:
                follow_button = await page.query_selector(selector)
                if follow_button:
                    break
            except:
                continue
        
        if not follow_button:
            raise InstagramAutomationError(f"Could not find Follow button for {target_username}")
        
        # Click Follow button
        await follow_button.click()
        
        # Wait a bit for the action to complete
        await page.wait_for_timeout(2000)
        
        logger.info(f"Successfully followed {target_username}")
        return True
        
    except Exception as e:
        logger.error(f"Error following {target_username}: {str(e)}")
        return False

async def like_recent_post(page, target_username):
    """Like the most recent post from a target account"""
    logger.info(f"Liking recent post from {target_username}...")
    
    try:
        # Navigate to target account
        await page.goto(f"https://www.instagram.com/{target_username}/")
        
        # Wait for posts to load
        await page.wait_for_timeout(3000)
        
        # Find and click on the first post (most recent)
        first_post = await page.query_selector("article div:first-child div:first-child a")
        if not first_post:
            raise InstagramAutomationError(f"Could not find posts for {target_username}")
        
        # Click on the first post
        await first_post.click()
        
        # Wait for post modal to load
        await page.wait_for_timeout(3000)
        
        # Find and click Like button (heart icon)
        like_button = await page.query_selector("section button:has(svg[aria-label='Like'])")
        if not like_button:
            # Try alternative selector
            like_button = await page.query_selector("section button:has(svg):nth-of-type(1)")
        
        if like_button:
            # Check if already liked
            svg_element = await like_button.query_selector("svg")
            if svg_element:
                like_svg_label = await svg_element.get_attribute("aria-label")
                if like_svg_label == "Like":
                    # Post is not liked yet, click to like
                    await like_button.click()
                    logger.info(f"Successfully liked a post from {target_username}")
                else:
                    logger.info(f"Post from {target_username} was already liked")
            else:
                # If we can't determine the state, just click it
                await like_button.click()
                logger.info(f"Clicked like button for a post from {target_username}")
        else:
            logger.warning(f"Could not find like button for {target_username}'s post")
            return False
            
        return True
        
    except Exception as e:
        logger.error(f"Error liking post from {target_username}: {str(e)}")
        return False

async def main():
    """Main function to run the Instagram automation"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Instagram Automation Tool')
    parser.add_argument('--username', required=True, help='Your Instagram username')
    parser.add_argument('--password', required=True, help='Your Instagram password')
    parser.add_argument('--target', required=True, help='Target account to follow')
    parser.add_argument('--like', action='store_true', help='Also like a post from the target account')
    parser.add_argument('--headless', action='store_true', help='Run browser in headless mode')
    
    args = parser.parse_args()
    
    # Configuration
    config = StagehandConfig(
        env="LOCAL",  # Use local browser
        headless=args.headless,  # Show/hide browser window
        verbose=1,  # Minimal logging
    )
    
    # Initialize Stagehand
    logger.info("Initializing Stagehand...")
    stagehand = None
    try:
        stagehand = Stagehand(config)
        await stagehand.init()
        page = stagehand.page
        
        # Login to Instagram
        await login_to_instagram(page, args.username, args.password)
        
        # Follow the target account
        follow_success = await follow_account(page, args.target)
        if not follow_success:
            logger.error("Failed to follow the target account")
            return False
        
        # Like a post if requested
        if args.like:
            like_success = await like_recent_post(page, args.target)
            if not like_success:
                logger.warning("Failed to like a post from the target account")
                # Don't return False here as following was successful
        
        logger.info("All actions completed successfully!")
        return True
        
    except InstagramAutomationError as e:
        logger.error(f"Instagram automation error: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during automation: {str(e)}")
        return False
    finally:
        # Close the browser
        if stagehand:
            logger.info("Closing browser...")
            await stagehand.close()

if __name__ == "__main__":
    logger.info("Instagram Automation Tool using Stagehand")
    logger.info("=" * 50)
    
    # Run the main function
    try:
        success = asyncio.run(main())
        
        if success:
            logger.info("\n✅ Automation completed successfully!")
            sys.exit(0)
        else:
            logger.error("\n❌ Automation failed!")
            sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Automation interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)