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
import time
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

async def wait_for_element(page, selector, timeout=10000):
    """Wait for an element to appear on the page"""
    try:
        await page.wait_for_selector(selector, timeout=timeout)
        return True
    except Exception as e:
        logger.warning(f"Element with selector '{selector}' not found within {timeout}ms")
        return False

async def login_to_instagram(page, username, password):
    """Log into Instagram with provided credentials"""
    logger.info(f"Logging into Instagram as {username}...")
    
    try:
        # Navigate to Instagram login page
        logger.info("Navigating to Instagram login page...")
        await page.goto("https://www.instagram.com/accounts/login/")
        
        # Wait for the page to load
        logger.info("Waiting for login page to load...")
        await page.wait_for_timeout(5000)
        
        # Try multiple selectors for username field
        username_selectors = [
            "input[name='username']",
            "input[aria-label='Phone number, username, or email']",
            "input[type='text']"
        ]
        
        username_field = None
        for selector in username_selectors:
            try:
                username_field = await page.query_selector(selector)
                if username_field:
                    logger.info(f"Found username field with selector: {selector}")
                    break
            except:
                continue
        
        if not username_field:
            raise InstagramAutomationError("Could not find username field")
        
        # Fill in username
        await username_field.fill(username)
        
        # Try multiple selectors for password field
        password_selectors = [
            "input[name='password']",
            "input[aria-label='Password']",
            "input[type='password']"
        ]
        
        password_field = None
        for selector in password_selectors:
            try:
                password_field = await page.query_selector(selector)
                if password_field:
                    logger.info(f"Found password field with selector: {selector}")
                    break
            except:
                continue
        
        if not password_field:
            raise InstagramAutomationError("Could not find password field")
        
        # Fill in password
        await password_field.fill(password)
        
        # Try multiple selectors for login button
        login_button_selectors = [
            "button[type='submit']",
            "button:has-text('Log in')",
            "button:has-text('Log In')",
            "button:has-text('Login')"
        ]
        
        login_button = None
        for selector in login_button_selectors:
            try:
                login_button = await page.query_selector(selector)
                if login_button:
                    logger.info(f"Found login button with selector: {selector}")
                    break
            except:
                continue
        
        if not login_button:
            raise InstagramAutomationError("Could not find login button")
        
        # Click login button
        logger.info("Clicking login button...")
        await login_button.click()
        
        # Wait for navigation
        logger.info("Waiting for login to complete...")
        await page.wait_for_timeout(8000)
        
        # Check if login was successful
        current_url = page.url
        logger.info(f"Current URL after login attempt: {current_url}")
        
        if "login" in current_url and "challenge" not in current_url:
            # Check for error messages
            error_selectors = [
                "div:has-text('Sorry, your password was incorrect')",
                "div:has-text('Incorrect password')",
                "div:has-text('The username you entered')",
                "span:has-text('Try Again')"
            ]
            
            for selector in error_selectors:
                error_elements = await page.query_selector_all(selector)
                if error_elements:
                    error_text = await error_elements[0].inner_text()
                    raise InstagramAutomationError(f"Login failed: {error_text}")
        
        # Check for successful login indicators
        home_indicators = [
            "a[href='/']",
            "a[aria-label='Home']",
            "a:has-text('Home')"
        ]
        
        login_successful = False
        for selector in home_indicators:
            try:
                element = await page.query_selector(selector)
                if element:
                    login_successful = True
                    break
            except:
                continue
        
        if not login_successful:
            logger.warning("Could not confirm successful login, but proceeding...")
        
        logger.info("Login process completed!")
        return True
        
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        raise InstagramAutomationError(f"Failed to login: {str(e)}")

async def navigate_to_profile(page, target_username):
    """Navigate to a target Instagram profile"""
    logger.info(f"Navigating to profile: {target_username}")
    
    try:
        # Try direct navigation first
        profile_url = f"https://www.instagram.com/{target_username}/"
        logger.info(f"Going to {profile_url}")
        await page.goto(profile_url)
        
        # Wait for page to load
        await page.wait_for_timeout(5000)
        
        # Check if we're on the right page
        current_url = page.url
        logger.info(f"Current URL: {current_url}")
        
        if target_username.lower() in current_url.lower():
            logger.info("Successfully navigated to profile")
            return True
        else:
            logger.warning("Direct navigation failed, trying search method")
            
            # Try using Instagram search
            search_url = "https://www.instagram.com/"
            await page.goto(search_url)
            await page.wait_for_timeout(3000)
            
            # Try to find search input
            search_selectors = [
                "input[aria-label='Search input']",
                "input[placeholder='Search']",
                "input[type='text']"
            ]
            
            search_input = None
            for selector in search_selectors:
                try:
                    search_input = await page.query_selector(selector)
                    if search_input:
                        logger.info(f"Found search input with selector: {selector}")
                        break
                except:
                    continue
            
            if search_input:
                await search_input.fill(target_username)
                await page.wait_for_timeout(2000)
                
                # Try to find and click search result
                result_selectors = [
                    f"a[href='/{target_username}/']",
                    f"div:has-text('{target_username}')",
                    "div[role='button']"
                ]
                
                for selector in result_selectors:
                    try:
                        result = await page.query_selector(selector)
                        if result:
                            await result.click()
                            await page.wait_for_timeout(3000)
                            break
                    except:
                        continue
            
            # Final check
            current_url = page.url
            if target_username.lower() in current_url.lower():
                logger.info("Successfully navigated to profile via search")
                return True
            else:
                logger.warning("Could not confirm navigation to profile")
                return False
                
    except Exception as e:
        logger.error(f"Error navigating to profile: {str(e)}")
        return False

async def follow_account(page, target_username):
    """Follow a target account"""
    logger.info(f"Attempting to follow {target_username}...")
    
    try:
        # Navigate to target account
        nav_success = await navigate_to_profile(page, target_username)
        if not nav_success:
            logger.error(f"Failed to navigate to {target_username}'s profile")
            return False
        
        # Wait for page to load completely
        await page.wait_for_timeout(3000)
        
        # Try multiple selectors for the Follow button
        follow_button_selectors = [
            "button:has-text('Follow')",
            "button:has-text('Follow Back')",
            "button:has-text('Requested')",
            "_acan._acao._acas",
            "button[type='button']",
            "[aria-label='Follow']",
            "[aria-label='Follow Back']"
        ]
        
        follow_button = None
        button_text = ""
        for selector in follow_button_selectors:
            try:
                buttons = await page.query_selector_all(selector)
                for button in buttons:
                    button_text = await button.inner_text()
                    # Check if it's actually a follow button and not already following
                    if "follow" in button_text.lower() or "request" in button_text.lower():
                        follow_button = button
                        logger.info(f"Found follow button with selector: {selector}, text: '{button_text}'")
                        break
                if follow_button:
                    break
            except Exception as e:
                logger.debug(f"Selector {selector} failed: {str(e)}")
                continue
        
        if not follow_button:
            # Try a more general approach
            logger.info("Trying general approach to find follow button...")
            all_buttons = await page.query_selector_all("button")
            for button in all_buttons:
                try:
                    text = await button.inner_text()
                    if "follow" in text.lower() or "request" in text.lower():
                        follow_button = button
                        button_text = text
                        logger.info(f"Found follow button by general search, text: '{button_text}'")
                        break
                except:
                    continue
        
        if not follow_button:
            logger.warning("Could not find Follow button, checking if already following...")
            
            # Check if already following
            following_selectors = [
                "button:has-text('Following')",
                "button:has-text('Requested')",
                "[aria-label='Following']"
            ]
            
            for selector in following_selectors:
                try:
                    following_button = await page.query_selector(selector)
                    if following_button:
                        logger.info(f"Already following {target_username} (found button: {selector})")
                        return True
                except:
                    continue
            
            logger.error(f"Could not find Follow button for {target_username}")
            return False
        
        # Check button state
        button_text = await follow_button.inner_text()
        logger.info(f"Follow button text: '{button_text}'")
        
        if "following" in button_text.lower() or "requested" in button_text.lower():
            logger.info(f"Already following {target_username}")
            return True
        
        # Click Follow button
        logger.info("Clicking Follow button...")
        await follow_button.click()
        
        # Wait a bit for the action to complete
        await page.wait_for_timeout(3000)
        
        # Verify follow action
        try:
            new_button = await page.query_selector("button:has-text('Following')")
            if new_button:
                logger.info(f"Successfully followed {target_username}")
                return True
            else:
                logger.info(f"Clicked follow button for {target_username} (verification pending)")
                return True
        except:
            logger.info(f"Clicked follow button for {target_username}")
            return True
        
    except Exception as e:
        logger.error(f"Error following {target_username}: {str(e)}")
        return False

async def like_recent_post(page, target_username):
    """Like the most recent post from a target account"""
    logger.info(f"Attempting to like recent post from {target_username}...")
    
    try:
        # Navigate to target account
        nav_success = await navigate_to_profile(page, target_username)
        if not nav_success:
            logger.error(f"Failed to navigate to {target_username}'s profile")
            return False
        
        # Wait for posts to load
        await page.wait_for_timeout(5000)
        
        # Try to find and click on the first post (most recent)
        post_selectors = [
            "article div:first-child div:first-child a",
            "a[href^='/p/']",
            "div[role='button'] img[alt]",
            "article a"
        ]
        
        first_post = None
        for selector in post_selectors:
            try:
                first_post = await page.query_selector(selector)
                if first_post:
                    logger.info(f"Found first post with selector: {selector}")
                    break
            except:
                continue
        
        if not first_post:
            logger.error(f"Could not find posts for {target_username}")
            return False
        
        # Click on the first post
        logger.info("Clicking on first post...")
        await first_post.click()
        
        # Wait for post modal to load
        await page.wait_for_timeout(5000)
        
        # Try multiple selectors for Like button
        like_button_selectors = [
            "section button:has(svg[aria-label='Like'])",
            "section button:has(svg):nth-of-type(1)",
            "button:has-text('Like')",
            "button svg[aria-label='Like']",
            "svg[aria-label='Like']"
        ]
        
        like_button = None
        for selector in like_button_selectors:
            try:
                like_button = await page.query_selector(selector)
                if like_button:
                    logger.info(f"Found like button with selector: {selector}")
                    break
            except:
                continue
        
        if not like_button:
            logger.error(f"Could not find like button for {target_username}'s post")
            return False
        
        # Check if already liked
        try:
            svg_element = await like_button.query_selector("svg")
            if svg_element:
                like_svg_label = await svg_element.get_attribute("aria-label")
                if like_svg_label and "liked" in like_svg_label.lower():
                    logger.info(f"Post from {target_username} was already liked")
                    return True
        except:
            pass
        
        # Click Like button
        logger.info("Clicking like button...")
        await like_button.click()
        
        # Wait a bit for the action to complete
        await page.wait_for_timeout(2000)
        
        logger.info(f"Successfully liked a post from {target_username}")
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
        
        # Set viewport size for better Instagram compatibility
        await page.set_viewport_size({"width": 1920, "height": 1080})
        
        # Login to Instagram
        login_success = await login_to_instagram(page, args.username, args.password)
        if not login_success:
            logger.error("Failed to login to Instagram")
            return False
        
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