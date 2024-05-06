# saas_app/models.py
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
# saas_app/models.py
from django.db import models

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    points = models.TextField(default='')  # Add this field with a default value
    price = models.DecimalField(max_digits=10, decimal_places=2)
     
    def __str__(self):
        return self.name
    # Add other fields like features, duration, etc. as needed


class UserManagement(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    api_key = models.CharField(max_length=100)  # Assuming API key is a string


class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    subscription_date = models.DateField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.user.username}'s subscription to {self.plan.name}"
