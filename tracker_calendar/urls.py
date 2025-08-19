from django.urls import path
from . import views

app_name = 'tracker_calendar'

urlpatterns = [
    path('user/create/', views.MonthView.as_view(), name='create'),
]