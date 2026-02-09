from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import Subscriber, Newsletter, NewsletterLog
from .utils import send_newsletter


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_active', 'subscribed_at']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email', 'first_name', 'last_name']
    readonly_fields = ['subscribed_at', 'unsubscribed_at']
    
    actions = ['activate_subscribers', 'deactivate_subscribers']
    
    def activate_subscribers(self, request, queryset):
        updated = queryset.update(is_active=True, unsubscribed_at=None)
        self.message_user(request, f'{updated} subscriber(s) activated.')
    activate_subscribers.short_description = 'Activate selected subscribers'
    
    def deactivate_subscribers(self, request, queryset):
        updated = queryset.update(is_active=False, unsubscribed_at=timezone.now())
        self.message_user(request, f'{updated} subscriber(s) deactivated.')
    deactivate_subscribers.short_description = 'Deactivate selected subscribers'


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['subject', 'created_at', 'sent_at', 'is_sent', 'send_button']
    list_filter = ['is_sent', 'created_at']
    search_fields = ['subject']
    readonly_fields = ['created_at', 'sent_at', 'is_sent']
    
    fieldsets = (
        ('Newsletter Content', {
            'fields': ('subject', 'html_content')
        }),
        ('Status', {
            'fields': ('is_sent', 'created_at', 'sent_at')
        }),
    )
    
    def send_button(self, obj):
        if obj.is_sent:
            return format_html('<span style="color: green;">✓ Sent</span>')
        else:
            return format_html(
                '<a class="button" href="#" onclick="sendNewsletter({}); return false;">Send Newsletter</a>',
                obj.id
            )
    send_button.short_description = 'Action'
    
    class Media:
        js = ('newsletter/admin_newsletter.js',)


@admin.register(NewsletterLog)
class NewsletterLogAdmin(admin.ModelAdmin):
    list_display = ['newsletter', 'subscriber', 'sent_at', 'success']
    list_filter = ['success', 'sent_at']
    search_fields = ['newsletter__subject', 'subscriber__email']
    readonly_fields = ['newsletter', 'subscriber', 'sent_at', 'success', 'error_message']
    
    def has_add_permission(self, request):
        return False
