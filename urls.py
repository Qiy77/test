from django.urls import path
from . import views

app_name = 'newsletter'

urlpatterns = [
    path('subscribe/', views.subscribe, name='subscribe'),
    path('subscribe/success/', views.subscribe_success, name='subscribe_success'),
    path('unsubscribe/<str:email>/', views.unsubscribe, name='unsubscribe'),
    path('unsubscribe/success/', views.unsubscribe_success, name='unsubscribe_success'),
    path('send/<int:newsletter_id>/', views.send_newsletter_view, name='send_newsletter'),
]
