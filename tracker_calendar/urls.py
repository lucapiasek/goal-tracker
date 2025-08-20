from django.urls import path
from . import views

app_name = 'tracker_calendar'

urlpatterns = [
    path('<str:username>/<int:year>/', views.YearView.as_view(), name='year'),
    path('<str:username>/<int:year>/<int:month>/<int:day>', views.DayView.as_view(), name='day')
]