from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from .models import Subscriber, Newsletter
from .forms import SubscriberForm
from .utils import send_newsletter


def subscribe(request):
    """Handle newsletter subscription"""
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            first_name = form.cleaned_data.get('first_name', '')
            last_name = form.cleaned_data.get('last_name', '')
            
            # Check if email already exists
            subscriber, created = Subscriber.objects.get_or_create(
                email=email,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'is_active': True
                }
            )
            
            if not created:
                if subscriber.is_active:
                    messages.info(request, 'You are already subscribed!')
                else:
                    # Reactivate subscription
                    subscriber.is_active = True
                    subscriber.unsubscribed_at = None
                    subscriber.save()
                    messages.success(request, 'Welcome back! You have been resubscribed.')
            else:
                messages.success(request, 'Successfully subscribed to our newsletter!')
            
            return redirect('newsletter:subscribe_success')
    else:
        form = SubscriberForm()
    
    return render(request, 'newsletter/subscribe.html', {'form': form})


def subscribe_success(request):
    """Display subscription success page"""
    return render(request, 'newsletter/subscribe_success.html')


def unsubscribe(request, email):
    """Handle newsletter unsubscription"""
    subscriber = get_object_or_404(Subscriber, email=email)
    
    if request.method == 'POST':
        subscriber.unsubscribe()
        messages.success(request, 'You have been unsubscribed from our newsletter.')
        return redirect('newsletter:unsubscribe_success')
    
    return render(request, 'newsletter/unsubscribe.html', {'subscriber': subscriber})


def unsubscribe_success(request):
    """Display unsubscription success page"""
    return render(request, 'newsletter/unsubscribe_success.html')


@require_http_methods(["POST"])
def send_newsletter_view(request, newsletter_id):
    """Send newsletter to all active subscribers (admin only)"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    newsletter = get_object_or_404(Newsletter, id=newsletter_id)
    
    if newsletter.is_sent:
        return JsonResponse({'error': 'Newsletter already sent'}, status=400)
    
    # Send newsletter
    result = send_newsletter(newsletter)
    
    return JsonResponse({
        'success': True,
        'sent_count': result['sent_count'],
        'failed_count': result['failed_count']
    })
