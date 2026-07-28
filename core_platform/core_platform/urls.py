from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from quiz_engine import views as quiz_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', quiz_views.LoginView.as_view(), name='login'),
    path('logout/', quiz_views.logout_view, name='logout'),
    path('accounts/profile/', lambda request: redirect('/dashboard/'), name='profile_redirect'),
    path('', include('quiz_engine.urls')),
]