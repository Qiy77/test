from django.db import models
from django.utils import timezone


class Subscriber(models.Model):
    """Model to store newsletter subscribers"""
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-subscribed_at']
    
    def __str__(self):
        return self.email
    
    def unsubscribe(self):
        """Mark subscriber as inactive"""
        self.is_active = False
        self.unsubscribed_at = timezone.now()
        self.save()


class Newsletter(models.Model):
    """Model to store newsletter content"""
    subject = models.CharField(max_length=200)
    html_content = models.TextField(help_text="HTML content of the newsletter")
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    is_sent = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.subject} - {'Sent' if self.is_sent else 'Draft'}"


class NewsletterLog(models.Model):
    """Model to track newsletter sends to individual subscribers"""
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE, related_name='logs')
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE, related_name='newsletter_logs')
    sent_at = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=True)
    error_message = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-sent_at']
        unique_together = ['newsletter', 'subscriber']
    
    def __str__(self):
        return f"{self.newsletter.subject} to {self.subscriber.email}"
