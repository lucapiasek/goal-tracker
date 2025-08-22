from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

app_name = 'accounts'

urlpatterns = [
    path('user/new/', views.UserCreateView.as_view(), name='user_create'),
    path('user/login', views.LoginView.as_view(), name='login'),
    path('user/logout', views.LogoutView.as_view(), name='logout'),
    path('<str:username>/', views.UserDetailView.as_view(), name='user_detail')
]