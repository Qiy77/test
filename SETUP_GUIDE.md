# Django Newsletter System - Setup Instructions

## Installation Steps

### 1. Create the Newsletter App
```bash
python manage.py startapp newsletter
```

### 2. Add to INSTALLED_APPS
In your `settings.py`:
```python
INSTALLED_APPS = [
    # ... other apps
    'newsletter',
]
```

### 3. Configure Email Settings
Add to your `settings.py`:

#### For Development (Console Backend):
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@yoursite.com'
SITE_URL = 'http://localhost:8000'
```

#### For Production (SMTP):
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Your SMTP host
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'noreply@yoursite.com'
SITE_URL = 'https://yourwebsite.com'
```

**Note for Gmail users:** You need to create an app-specific password:
1. Go to Google Account settings
2. Security > 2-Step Verification > App passwords
3. Generate a new app password for "Mail"

### 4. Update Main URLs
In your project's `urls.py`:
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('newsletter/', include('newsletter.urls')),
]
```

### 5. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (if not already created)
```bash
python manage.py createsuperuser
```

## Usage

### Creating and Sending Newsletters

1. **Access Admin Panel**: Go to `http://localhost:8000/admin/`

2. **Add Subscribers**: 
   - Navigate to Newsletter > Subscribers
   - Click "Add Subscriber"
   - Or users can subscribe via the public form at `/newsletter/subscribe/`

3. **Create Newsletter**:
   - Navigate to Newsletter > Newsletters
   - Click "Add Newsletter"
   - Enter subject and HTML content
   - Use placeholders: `{{first_name}}`, `{{last_name}}`, `{{email}}`
   - Save as draft

4. **Send Newsletter**:
   - In the newsletters list, click "Send Newsletter" button
   - Or use the admin action menu

### Public URLs

- Subscribe form: `http://localhost:8000/newsletter/subscribe/`
- Unsubscribe: `http://localhost:8000/newsletter/unsubscribe/<email>/`

## Database Models

### Subscriber
- `email`: Unique email address
- `first_name`: Optional first name
- `last_name`: Optional last name
- `is_active`: Subscription status
- `subscribed_at`: Subscription date
- `unsubscribed_at`: Unsubscription date

### Newsletter
- `subject`: Email subject line
- `html_content`: HTML email body
- `created_at`: Creation timestamp
- `sent_at`: Send timestamp
- `is_sent`: Send status

### NewsletterLog
- Tracks each email sent
- Records success/failure
- Links newsletter to subscriber

## Features

✓ Email subscription management
✓ HTML email support
✓ Subscriber personalization ({{first_name}}, etc.)
✓ Unsubscribe functionality
✓ Send tracking and logging
✓ Bulk email sending
✓ Admin interface
✓ Duplicate prevention
✓ Resubscription support

## Testing

### Test Email Configuration
```bash
python manage.py shell
```

```python
from django.core.mail import send_mail

send_mail(
    'Test Subject',
    'Test message.',
    'from@example.com',
    ['to@example.com'],
    fail_silently=False,
)
```

### Send Test Newsletter
1. Create a subscriber in admin
2. Create a newsletter
3. Click "Send Newsletter"
4. Check console (development) or email inbox (production)

## Customization

### Custom Email Templates
Modify `utils.py` to use Django templates:

```python
from django.template.loader import render_to_string

html_content = render_to_string('newsletter/email_template.html', {
    'first_name': subscriber.first_name,
    'content': newsletter.html_content
})
```

### Add Welcome Emails
In `views.py`, after successful subscription:
```python
from .utils import send_welcome_email

if created:
    send_welcome_email(subscriber)
```

## Production Considerations

1. **Use Celery for Async Sending**: For large subscriber lists, send emails asynchronously
2. **Rate Limiting**: Implement rate limiting to avoid spam flags
3. **Email Service**: Consider using SendGrid, Mailgun, or Amazon SES
4. **GDPR Compliance**: Add consent checkboxes and privacy policy
5. **Double Opt-in**: Require email confirmation before activation
6. **Analytics**: Track open rates and click-throughs

## Troubleshooting

**Emails not sending:**
- Check EMAIL_BACKEND setting
- Verify SMTP credentials
- Check firewall/security settings
- Look for errors in console

**Gmail blocking:**
- Enable "Less secure app access" or use app passwords
- Check Gmail's sending limits

**Unsubscribe links not working:**
- Verify SITE_URL is set correctly
- Check URL patterns are included
