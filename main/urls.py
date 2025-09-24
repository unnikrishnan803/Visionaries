from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.views.decorators.csrf import csrf_exempt
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', csrf_exempt(LogoutView.as_view(next_page='/')), name='logout'),
    path('profile/', views.profile, name='profile'),
]