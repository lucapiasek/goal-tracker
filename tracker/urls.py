from django.urls import path
from . import views

app_name = 'tracker'
urlpatterns = [
    path('goals/', views.GoalsView.as_view(), name='goals'),
]