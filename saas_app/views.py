from django.http import HttpResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import SubscriptionPlan, UserSubscription
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail

# views.py

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import login
from django.http import HttpResponse
from .forms import SubscriptionCheckoutForm
from .models import SubscriptionPlan, UserSubscription
from django.conf import settings
# views.py

from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import CustomUserCreationForm
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

# views.py

from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Check if the email already exists
            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                messages.error(request, 'This email is already taken.')
                return redirect('register')

            # Check if passwords match
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            if password1 != password2:
                messages.error(request, 'Passwords do not match.')
                return redirect('register')

            # Save user if everything is valid
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Remaining code for sending activation email
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            activation_link = f"http://{current_site.domain}/activate/{urlsafe_base64_encode(force_bytes(user.pk))}/{default_token_generator.make_token(user)}/"
            message = f"Hi {user.username},\n\nThank you for registering with us. To activate your account, please visit {activation_link}\n\nIf you did not register on our site, please ignore this email.\n\nBest regards,\nYour Site Team"

            send_mail(mail_subject, message, None, [user.email])
            return redirect('account_activation_sent')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
            return redirect('register')
    else:
        form = CustomUserCreationForm()
    return render(request, 'saas_app/register.html', {'form': form})

def account_activation_sent(request):
    return render(request, 'saas_app/account_activation_sent.html')

from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user_model = get_user_model()
        user = user_model.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user_model.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')  # Redirect to home page after activation
    else:
        return render(request, 'saas_app/account_activation_invalid.html')

def about_us(request):
    return render(request, 'saas_app/about_us.html')

from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            message = form.cleaned_data['message']
            subject = 'Contact Form Submission'
            message = f'Name: {name}\nEmail: {email}\nPhone Number: {phone_number}\nMessage: {message}'
            sender_email = settings.EMAIL_HOST_USER
            send_mail(subject, message, sender_email, [sender_email])
            return render(request, 'saas_app/contact_info.html')  # Render a success page after sending the email
    else:
        form = ContactForm()
    return render(request, 'saas_app/contact_info.html', {'form': form})

def help_page(request):
    return render(request, 'saas_app/help.html')

def home(request):
    plans = SubscriptionPlan.objects.all()
    return render(request, 'saas_app/home.html', {'plans': plans})

def subscription_plans(request):
    plans = SubscriptionPlan.objects.all()
    for plan in plans:
        plan.points = plan.points.split('\n')  # Preprocess points data
    return render(request, 'saas_app/services.html', {'plans': plans})

def subscribe(request):
    if request.method == 'POST':
        plan_id = request.POST.get('plan_id')
        plan = SubscriptionPlan.objects.get(pk=plan_id)
        return redirect('checkout', plan_id=plan_id)
    return redirect('services')  # Redirect to services page if accessed via GET

# views.py
from django.shortcuts import render, redirect
from .models import SubscriptionPlan, UserSubscription
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render, redirect
from .models import SubscriptionPlan, UserSubscription
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.utils import timezone

@login_required
def checkout(request, plan_id):
    if request.method == 'GET':
        try:
            plan = SubscriptionPlan.objects.get(pk=plan_id)
            return render(request, 'saas_app/checkout.html', {'selected_plan': plan})
        except SubscriptionPlan.DoesNotExist:
            return HttpResponse("Invalid Subscription Plan")


from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import UserSubscription
from .utils import calculate_words_left_per_day

@login_required
def personal_page(request):
    try:
        user_subscription = UserSubscription.objects.get(user=request.user)
        remaining_days = (user_subscription.subscription_date + timedelta(days=30) - timezone.now().date()).days
        words_left_per_day = calculate_words_left_per_day(user_subscription)
        
        return render(request, 'saas_app/personal_page.html', {
            'remaining_days': remaining_days,
            'subscription_plan': user_subscription.plan.name,
            'words_left_per_day': words_left_per_day  # Pass the words left per day to the template
        })
    except UserSubscription.DoesNotExist:
        messages.warning(request, "You don't have a subscription. Please buy a subscription.")
        return HttpResponseRedirect('/services/')

def send_subscription_end_notification(user):
    subject = 'Your subscription has ended'
    message = 'Dear {}, your subscription has ended. Please renew your subscription to continue accessing our services.'.format(user.username)
    from_email = settings.EMAIL_HOST_USER
    to_email = [user.email]
    send_mail(subject, message, from_email, to_email)


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from .models import UserSubscription, SubscriptionPlan
# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from .models import UserSubscription, SubscriptionPlan
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from .models import UserSubscription, SubscriptionPlan
from django.db.models import Sum

@staff_member_required
def admin_dashboard(request):
    # Calculate total users
    total_users = User.objects.count()

    # Calculate total sales from active subscriptions
    total_sales = UserSubscription.objects.filter(active=True).aggregate(total_sales=Sum('plan__price'))['total_sales'] or 0

    # Count total active subscriptions
    total_subscriptions = UserSubscription.objects.filter(active=True).count()

    # Fetch users with subscriptions along with subscription data
    users_with_subscriptions = User.objects.filter(usersubscription__active=True).order_by('-date_joined')
    user_data_with_subscriptions = []
    for user in users_with_subscriptions:
        user_subscription = UserSubscription.objects.filter(user=user).first()
        user_data_with_subscriptions.append({
            'user': user,
            'subscription_package': user_subscription.plan.name,
            'subscription_price': user_subscription.plan.price
        })

    # Fetch users without subscriptions
    users_without_subscriptions = User.objects.exclude(usersubscription__active=True).order_by('-date_joined')
    users_with_subscriptions = User.objects.filter(usersubscription__active=True).order_by('-date_joined')


    return render(request, 'saas_app/admin_dashboard.html', {
        'total_users': total_users,
        'total_sales': total_sales,
        'total_subscriptions': total_subscriptions,
        'user_data_with_subscriptions': user_data_with_subscriptions,
        'users_without_subscriptions': users_without_subscriptions,
        'users_with_subscriptions': users_with_subscriptions,

    })




from django.shortcuts import render, redirect
from .models import SubscriptionPlan, UserSubscription
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.utils import timezone
import paypalrestsdk
from django.conf import settings

paypalrestsdk.configure({
    'mode': settings.PAYPAL_MODE,
    'client_id': settings.PAYPAL_CLIENT_ID,
    'client_secret': settings.PAYPAL_SECRET,
})

@login_required
def process_payment(request):
    plan_id = request.POST.get('plan_id')
    selected_plan = SubscriptionPlan.objects.get(pk=plan_id)
    payment_amount = selected_plan.price

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": "http://localhost:8000/payment/execute/?plan_id={}&payment_amount={}".format(plan_id, payment_amount),
            "cancel_url": "http://localhost:8000/payment/cancel/"
        },
        "transactions": [{
            "amount": {
                "total": str(payment_amount),
                "currency": "USD"
            },
            "description": "Subscription payment for {}".format(selected_plan.name)
        }]
    })

    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                return redirect(link.href)
    else:
        error_message = payment.error['message']
        return render(request, 'saas_app/payment_error.html', {'error_message': error_message})
@login_required
def execute_payment(request):
    plan_id = request.GET.get('plan_id')
    payment_amount = request.GET.get('payment_amount')
    selected_plan = SubscriptionPlan.objects.get(pk=plan_id)
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')
    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        # Payment successful, update user subscription
        user_subscription = UserSubscription.objects.create(user=request.user, plan=selected_plan)
        return redirect('personal_page')
    else:
        error_message = payment.error['message']
        return render(request, 'saas_app/payment_error.html', {'error_message': error_message})

@login_required
def cancel_payment(request):
    return render(request, 'saas_app/payment_cancel.html')

def team(request):
    return render(request,'saas_app/team.html')


def account_activation_invalid(request):
    return render(request,'saas_app/account_activation_invalid.html')

from .utils import generate_blog

from django.shortcuts import render
# views.py

from django.shortcuts import render, redirect
from .models import UserSubscription
from .utils import calculate_words_left_per_day, generate_blog
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required

@login_required
def generate_blog_view(request):
    if request.method == 'POST':
        # Get user subscription based on logged-in user or any other identifier
        user_subscription = UserSubscription.objects.get(user=request.user)
        
        # Calculate words left per day based on user subscription
        words_left_today = calculate_words_left_per_day(user_subscription)
        
        # Get form inputs
        title = request.POST.get('title')
        description = request.POST.get('description')
        total_words = int(request.POST.get('total_words'))
        
        # Check if the total words requested exceed the words left for today
        if total_words > words_left_today:
            # Redirect with an error message or handle the error appropriately
            return redirect('generate_blog')  # Redirect to the same page
            
        # Pass words_per_day argument to generate_blog function
        words_per_day = user_subscription.plan.words_per_day
        generated_blog_text = generate_blog(description, title, total_words, words_per_day)
        
        # Deduct words from daily limit
        user_subscription.words_generated_today += total_words
        user_subscription.save()
        
        # Display or process the generated blog text as needed
        return render(request, 'saas_app/generated_blog.html', {'blog_text': generated_blog_text})
    
    return render(request, 'saas_app/generate_blog.html')

def generated_blog_view(request):
    # This view will render the generated blog content
    # You can modify it based on your requirements
    generated_content = request.POST.get('generated_content')  # Assuming you pass the generated content as POST data
    return render(request, 'saas_app/generated_blog.html', {'generated_content': generated_content})
