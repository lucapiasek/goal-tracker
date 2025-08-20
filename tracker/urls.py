from django.urls import path
from . import views

app_name = 'tracker'
urlpatterns = [
    path('<str:username>/goals/', views.GoalsView.as_view(), name='goal_list'),
    path('<str:username>/goal/<int:pk>/', views.GoalDetailView.as_view(), name='goal'),
    path('<str:username>/goal/new', views.GoalCreateView.as_view(), name='goal-create'),
    path('<str:username>/goal/<int:pk>/update', views.GoalUpdateView.as_view(), name='goal_update'),
    path('pieces/', views.PiecesView.as_view(), name='pieces')
]