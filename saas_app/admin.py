# saas_app/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, UserManagement, SubscriptionPlan, UserSubscription

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email')  # Add 'email' to the list of displayed fields

# Unregister the default UserAdmin
admin.site.unregister(User)

# Register User with the customized UserAdmin
admin.site.register(User, CustomUserAdmin)

admin.site.register(UserProfile)
admin.site.register(UserManagement)
admin.site.register(SubscriptionPlan)
admin.site.register(UserSubscription)
