import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from datetime import datetime
import config
from src.utils import setup_logging

class EmailSender:
    def __init__(self):
        self.logger = setup_logging()
        self.smtp_server = config.EMAIL_HOST
        self.smtp_port = config.EMAIL_PORT
        self.email_user = config.EMAIL_USER
        self.email_password = config.EMAIL_PASSWORD
    
    def create_scraping_report(self, scraping_result):
        """Create HTML email report from scraping results"""
        if scraping_result['success']:
            articles = scraping_result['articles']
            
            html_content = f"""
            <html>
            <body>
                <h2>📰 Wikipedia Scraping Report</h2>
                <p><strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p><strong>Articles Scraped:</strong> {scraping_result['articles_count']}</p>
                <p><strong>Status:</strong> ✅ Success</p>
                
                <h3>Articles Summary:</h3>
                <ul>
            """
            
            for article in articles:
                html_content += f"""
                <li>
                    <strong><a href="{article['url']}">{article['title']}</a></strong><br>
                    <em>Word Count: {article['word_count']} | Categories: {', '.join(article['categories'][:3])}</em><br>
                    {article['first_paragraph'][:200]}...
                </li><br>
                """
            
            html_content += """
                </ul>
                <p><i>Full data available in attached CSV file.</i></p>
            </body>
            </html>
            """
            
            return html_content
        else:
            return f"""
            <html>
            <body>
                <h2>❌ Wikipedia Scraping Report - Failed</h2>
                <p><strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p><strong>Error:</strong> {scraping_result.get('error', 'Unknown error')}</p>
            </body>
            </html>
            """
    
    def send_email(self, subject, html_content, csv_file_path=None):
        """Send email with optional CSV attachment"""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.email_user
            msg['To'] = config.RECIPIENT_EMAIL
            msg['Subject'] = subject
            
            # Add HTML content
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Add CSV attachment if provided
            if csv_file_path and os.path.exists(csv_file_path):
                with open(csv_file_path, 'rb') as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {os.path.basename(csv_file_path)}'
                )
                msg.attach(part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_user, self.email_password)
                server.send_message(msg)
            
            self.logger.info(f"Email sent successfully to {config.RECIPIENT_EMAIL}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send email: {str(e)}")
            return False
    
    def send_scraping_report(self, scraping_result):
        """Send complete scraping report via email"""
        subject = f"Wikipedia Scraping Report - {datetime.now().strftime('%Y-%m-%d')}"
        html_content = self.create_scraping_report(scraping_result)
        
        csv_file = scraping_result.get('csv_file') if scraping_result['success'] else None
        
        return self.send_email(subject, html_content, csv_file)

def main():
    """Test email functionality"""
    email_sender = EmailSender()
    
    # Test email
    test_result = {
        'success': True,
        'articles_count': 3,
        'articles': [
            {
                'title': 'Test Article',
                'url': 'https://en.wikipedia.org/wiki/Test',
                'first_paragraph': 'This is a test article for email functionality.',
                'word_count': 10,
                'categories': ['Test', 'Example']
            }
        ]
    }
    
    success = email_sender.send_scraping_report(test_result)
    print(f"Email test {'successful' if success else 'failed'}")

if __name__ == "__main__":
    main()
