# saas_app/forms.py

from django import forms
from .models import UserSubscription
from django import forms
from .models import SubscriptionPlan



from django import forms
from .models import UserSubscription, SubscriptionPlan

class SubscriptionCheckoutForm(forms.ModelForm):
    class Meta:
        model = UserSubscription
        fields = ['plan']

# forms.py
# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=20)
    message = forms.CharField(widget=forms.Textarea)
