from django.urls import path
from . import views

app_name = 'tracker_calendar'

urlpatterns = [
    path('<str:username>/<int:year>/', views.YearView.as_view(), name='create'),
]