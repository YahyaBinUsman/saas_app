from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from saas_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('saas_app.urls')),  # Include URLs from the app's URLconf
    path('register/', views.register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),  # Include built-in authentication URLs


]
