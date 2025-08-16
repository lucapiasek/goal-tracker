from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'accounts'

urlpatterns = [
    path('user/create/', views.UserCreateView.as_view(), name='create'),
    path('user/login', LoginView.as_view(
        template_name='accounts/create_form.html',
        next_page='tracker:goals',
        extra_context={'page_title': "Zaloguj się"}
    ), name='login'),
]