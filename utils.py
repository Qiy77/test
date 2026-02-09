from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
from .models import Subscriber, NewsletterLog


def send_newsletter(newsletter):
    """
    Send newsletter to all active subscribers
    
    Args:
        newsletter: Newsletter instance to send
        
    Returns:
        dict: Results with sent_count and failed_count
    """
    active_subscribers = Subscriber.objects.filter(is_active=True)
    sent_count = 0
    failed_count = 0
    
    for subscriber in active_subscribers:
        success = send_newsletter_email(newsletter, subscriber)
        
        # Log the send attempt
        NewsletterLog.objects.create(
            newsletter=newsletter,
            subscriber=subscriber,
            success=success,
            error_message='' if success else 'Failed to send email'
        )
        
        if success:
            sent_count += 1
        else:
            failed_count += 1
    
    # Mark newsletter as sent
    newsletter.is_sent = True
    newsletter.sent_at = timezone.now()
    newsletter.save()
    
    return {
        'sent_count': sent_count,
        'failed_count': failed_count
    }


def send_newsletter_email(newsletter, subscriber):
    """
    Send newsletter email to a single subscriber
    
    Args:
        newsletter: Newsletter instance
        subscriber: Subscriber instance
        
    Returns:
        bool: True if sent successfully, False otherwise
    """
    try:
        # Prepare email content with personalization
        html_content = newsletter.html_content
        
        # Replace placeholders if they exist
        html_content = html_content.replace('{{first_name}}', subscriber.first_name or '')
        html_content = html_content.replace('{{last_name}}', subscriber.last_name or '')
        html_content = html_content.replace('{{email}}', subscriber.email)
        
        # Add unsubscribe link at the bottom
        unsubscribe_link = f"{settings.SITE_URL}/newsletter/unsubscribe/{subscriber.email}/"
        html_content += f'<br><br><p style="font-size: 12px; color: #666;"><a href="{unsubscribe_link}">Unsubscribe</a></p>'
        
        # Create plain text version (strip HTML tags)
        from django.utils.html import strip_tags
        text_content = strip_tags(html_content)
        
        # Create email
        email = EmailMultiAlternatives(
            subject=newsletter.subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[subscriber.email]
        )
        
        # Attach HTML content
        email.attach_alternative(html_content, "text/html")
        
        # Send email
        email.send()
        
        return True
        
    except Exception as e:
        print(f"Error sending to {subscriber.email}: {str(e)}")
        return False


def send_welcome_email(subscriber):
    """
    Send welcome email to new subscriber
    
    Args:
        subscriber: Subscriber instance
    """
    try:
        subject = "Welcome to Our Newsletter!"
        
        html_content = f"""
        <html>
            <body>
                <h2>Welcome {subscriber.first_name or 'there'}!</h2>
                <p>Thank you for subscribing to our newsletter.</p>
                <p>We're excited to have you on board and will keep you updated with our latest news and updates.</p>
                <p>If you ever want to unsubscribe, you can do so <a href="{settings.SITE_URL}/newsletter/unsubscribe/{subscriber.email}/">here</a>.</p>
                <p>Best regards,<br>The Team</p>
            </body>
        </html>
        """
        
        text_content = strip_tags(html_content)
        
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[subscriber.email]
        )
        
        email.attach_alternative(html_content, "text/html")
        email.send()
        
        return True
        
    except Exception as e:
        print(f"Error sending welcome email to {subscriber.email}: {str(e)}")
        return False
