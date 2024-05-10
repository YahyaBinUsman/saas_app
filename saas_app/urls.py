from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    path('activate-error/<str:uidb64>/<str:token>/', views.account_activation_invalid, name='account_activation_invalid'),
    path('about_us/', views.about_us, name='about_us'),
    path('contact_info/', views.contact, name='contact'),
    path('help/', views.help_page, name='help'),
    path('services/', views.subscription_plans, name='services'),  # New URL for services page
    path('subscribe/', views.subscribe, name='subscribe'),
    path('checkout/<int:plan_id>/', views.checkout, name='checkout'),
    path('personal/', views.personal_page, name='personal_page'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('process_payment/', views.process_payment, name='process_payment'),
    path('execute_payment/', views.execute_payment, name='execute_payment'),
    path('cancel_payment/', views.cancel_payment, name='cancel_payment'),
    path('team/', views.team, name='team'),
    path('generate_blog/', views.generate_blog_view, name='generate_blog'),  # Updated URL for generating blogs
    path('generated_blog/', views.generated_blog_view, name='generated_blog'), ]
