"""
Email Sender Module
Sends email notifications with job alerts
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils.config import EMAIL, PASSWORD, RECIPIENT_EMAIL, JOBS_PER_EMAIL
from datetime import datetime

class EmailSender:
    def __init__(self):
        self.sender_email = EMAIL
        self.sender_password = PASSWORD
        self.recipient_email = RECIPIENT_EMAIL
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
    
    def send_email(self, jobs, subject="New Job Alerts", batch_size=JOBS_PER_EMAIL):
        """
        Send email with job listings
        
        Args:
            jobs (list): List of job dictionaries
            subject (str): Email subject
            batch_size (int): Max jobs per email
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not jobs or not self.sender_email or not self.sender_password:
            print("⚠ Email configuration incomplete. Skipping email...")
            return False
        
        try:
            # Send in batches if many jobs
            total_batches = (len(jobs) + batch_size - 1) // batch_size
            
            for batch_num in range(total_batches):
                start_idx = batch_num * batch_size
                end_idx = start_idx + batch_size
                batch_jobs = jobs[start_idx:end_idx]
                
                html_body = self._create_html_body(batch_jobs, batch_num + 1, total_batches)
                
                if self._send_smtp_email(html_body, subject, total_batches):
                    print(f"✓ Email {batch_num + 1}/{total_batches} sent successfully")
                else:
                    print(f"✗ Failed to send email {batch_num + 1}/{total_batches}")
                    return False
            
            return True
            
        except Exception as e:
            print(f"✗ Error sending email: {str(e)}")
            return False
    
    def _send_smtp_email(self, html_body, subject, total_batches):
        """Send email via SMTP"""
        try:
            if total_batches > 1:
                subject = f"{subject} (Batch {1}/{total_batches})"
            
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.sender_email
            msg['To'] = self.recipient_email
            
            # Attach HTML content
            msg.attach(MIMEText(html_body, 'html'))
            
            # Connect and send
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            return True
            
        except smtplib.SMTPAuthenticationError:
            print("✗ Email authentication failed. Check credentials and app password.")
            return False
        except Exception as e:
            print(f"✗ SMTP error: {str(e)}")
            return False
    
    def _create_html_body(self, jobs, batch_num=1, total_batches=1):
        """Create formatted HTML email body"""
        html = f"""
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #f5f5f5;">
                <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 8px;">
                    <h1 style="color: #333; border-bottom: 2px solid #0066cc; padding-bottom: 10px;">
                        Job Alerts - {datetime.now().strftime('%B %d, %Y')}
                    </h1>
                    <p style="color: #666; font-size: 14px;">Found {len(jobs)} new job opportunities matching your skills!</p>
        """
        
        for idx, job in enumerate(jobs, 1):
            html += f"""
                    <div style="border-left: 4px solid #0066cc; padding: 15px; margin: 15px 0; background-color: #f9f9f9; border-radius: 4px;">
                        <h2 style="color: #0066cc; margin: 0 0 10px 0;">{job.get('title', 'N/A')}</h2>
                        <p style="margin: 8px 0; color: #333;"><strong>Company:</strong> {job.get('company', 'N/A')}</p>
                        <p style="margin: 8px 0; color: #333;"><strong>Location:</strong> {job.get('location', 'N/A')}</p>
                        <p style="margin: 8px 0; color: #333;"><strong>Salary:</strong> {job.get('salary', 'Not available')}</p>
                        <p style="margin: 8px 0; color: #333;"><strong>Source:</strong> {job.get('source', 'Unknown')}</p>
                        <p style="margin: 15px 0 0 0;">
                            <a href="{job.get('link', '#')}" style="background-color: #0066cc; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px; display: inline-block;">Apply Now</a>
                        </p>
                    </div>
            """
        
        html += f"""
                    <hr style="border: 0; border-top: 1px solid #ddd; margin: 20px 0;">
                    <p style="color: #999; font-size: 12px; text-align: center;">
                        Job Scraper System | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                    </p>
                </div>
            </body>
        </html>
        """
        
        return html

def send_email(jobs):
    """Backward compatible function"""
    sender = EmailSender()
    return sender.send_email(jobs)