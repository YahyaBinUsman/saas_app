# saas_app/models.py
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
# saas_app/models.py
from django.db import models
class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    points = models.TextField(default='')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    max_words_per_day = models.IntegerField(default=1000)  # Add this field
    words_per_day = models.IntegerField(default=1000)  # Add this field

    def __str__(self):
        return self.name


class UserManagement(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    api_key = models.CharField(max_length=100)  # Assuming API key is a string


class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    subscription_date = models.DateField(auto_now_add=True)
    words_generated_today = models.IntegerField(default=0)  # New field to store words generated today
    

    def __str__(self):
        return f"{self.user.username}'s subscription to {self.plan.name}"

    def __str__(self):
        return f"{self.user.username}'s subscription to {self.plan.name}"
   

    def __str__(self):
        return f"{self.user.username}'s subscription to {self.plan.name}"


class GeneratedArticle(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    content = models.TextField()
    topical = models.CharField(max_length=255)
    tags = models.CharField(max_length=255)
    excerpt = models.CharField(max_length=255)
from django.db import models
from enum import Enum
from typing import Optional
from dataclasses import dataclass

class ArticleType(Enum):
    PUBLISHED = "published"
    DRAFT = "draft"
    PENDING = "pending"

class WPCredentials(models.Model):
    api_url = models.URLField()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

