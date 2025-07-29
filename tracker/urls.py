from django.urls import path
from . import views

app_name = 'tracker'
urlpatterns = [
    path('goals/', views.GoalsView.as_view(), name='goals'),
    path('goal/<int:pk>', views.GoalDetailView.as_view(), name='goal'),
    path('goal/new', views.GoalCreateView.as_view(), name='goal-create'),
    path('pieces/', views.PiecesView.as_view(), name='pieces')
]