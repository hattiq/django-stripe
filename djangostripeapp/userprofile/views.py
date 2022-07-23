from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

import stripe

from django.conf import settings
from . import models

stripe.api_key = settings.STRIPE_API_KEY

def profile(request):
    """ Profile Page """
    if request.user.is_authenticated and request.user.username != "admin":
        return render(request, template_name='userprofile/profile.html')
    else:
        return redirect("/accounts/login/")

def subscriptions(request):
    if request.user.is_authenticated and request.user.username != "admin":
        try:
            stripe_info = models.UserPaymentInfo.objects.get(user_id=request.user.id)
            stripe_cus_id = stripe_info.stripe_cus_id
        except ObjectDoesNotExist:
            stripe_cust = stripe.Customer.create(email=request.user.email, name=request.user.username)
            models.UserPaymentInfo.objects.create(user_id=request.user.id, stripe_cus_id=stripe_cust.stripe_id)
            stripe_cus_id = stripe_cust.stripe_id

        context = {}
        customer_info = stripe.Customer.retrieve(stripe_cus_id, expand=['subscriptions'])
        print(customer_info)
        subscription_prices = stripe.Price.list(limit=1)
        subscription_plan = stripe.Product.retrieve(subscription_prices["data"][0].product)
        context['subscription_prices'] = subscription_prices
        context['subscription_plan'] = subscription_plan
        context['customer_info'] = customer_info
        return render(request, template_name='userprofile/subscriptions.html', context=context)
    else:
        return redirect("/accounts/login/")

def cancel_subscription(request):
    """
    Endpoint for canceling subscription.
    """

    # Get subscription id from post data
    subscription_id = request.POST['subscribeID']
    # Set cancel_at_period_end to True for 
    # canceling subscription after period end
    stripe.Subscription.modify(
        subscription_id,
        cancel_at_period_end=True
    )
    # Redirect to subscriptions page after canceling
    return redirect('/profile/subscriptions/')

def resume_subscription(request):
    """
    Endpoint for Resuming subscription.
    """

    # Get subscription id from post data
    subscription_id = request.POST['subscribeID']
    # Set cancel_at_period_end to False for 
    # resuming subscription
    stripe.Subscription.modify(
        subscription_id,
        cancel_at_period_end=False
    )
    # Redirect to subscriptions page after resuming
    return redirect('/profile/subscriptions/')

def create_checkout_session(request):
    """
    Endpoint for creating session to checkout subscription.
    """

    # Get price id from post data
    price_id = request.POST['priceId']
    stripe_info = models.UserPaymentInfo.objects.get(user_id=request.user.id)
    
    # Creating session
    session = stripe.checkout.Session.create(
        success_url='http://127.0.0.1:8000/profile/subscriptions?session_id={CHECKOUT_SESSION_ID}',
        cancel_url='http://127.0.0.1:8000/profile/subscriptions?checkout_canceled=True',
        mode='subscription',
        line_items=[{
            'price': price_id,
            'quantity': 1
        }],
        subscription_data={
            'trial_period_days': 7
        },
        customer=stripe_info.stripe_cus_id
    )
    # Resirecting to session for check out
    return redirect(session.url, code=303)