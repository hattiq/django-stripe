from django.urls import path

from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    path('subscription/create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('subscription/cancel/', views.cancel_subscription, name='cancel_subscription'),
    path('subscription/resume/', views.resume_subscription, name='resume_subscription'),
]