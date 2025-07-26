#!/usr/bin/env python3
"""
Wikipedia Scraper with Email Notifications
Main application entry point
"""

import sys
import traceback
from src.scraper import main as scrape_wikipedia
from src.email_sender import EmailSender
from src.utils import setup_logging

def main():
    """Main application function"""
    logger = setup_logging()
    logger.info("Starting Wikipedia scraping job...")
    
    try:
        # Run scraping
        scraping_result = scrape_wikipedia()
        
        # Send email notification
        email_sender = EmailSender()
        email_success = email_sender.send_scraping_report(scraping_result)
        
        if scraping_result['success']:
            logger.info(f"✅ Scraping completed successfully. {scraping_result['articles_count']} articles scraped.")
        else:
            logger.error(f"❌ Scraping failed: {scraping_result.get('error')}")
            
        if email_success:
            logger.info("📧 Email notification sent successfully.")
        else:
            logger.warning("⚠️ Failed to send email notification.")
            
        return 0 if scraping_result['success'] else 1
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        logger.error(traceback.format_exc())
        
        # Try to send error notification
        try:
            email_sender = EmailSender()
            error_result = {
                'success': False,
                'error': f"Unexpected error: {str(e)}"
            }
            email_sender.send_scraping_report(error_result)
        except:
            pass
            
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
