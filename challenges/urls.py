from django.urls import path
from . import views

app_name = 'challenges'
urlpatterns = [
    path('<str:username>/challenges/', views.ChallengeListView.as_view(), name='list'),
    path('<str:username>/challenges/<int:pk>/', views.ChallengeDetailView.as_view(), name='detail'),
    path('<str:username>/challenges/new', views.ChallengeCreateView.as_view(), name='create'),
    path('<str:username>/challenges/from-task/<int:task_id>', views.ChallengeCreateFromTaskView.as_view(), name='create_from_task'),
    path('<str:username>/challenges/<int:pk>/delete', views.ChallengeDeleteView.as_view(), name='delete'),
    path('<str:username>/challenges/<int:pk>/confirm', views.ChallengeConfirmView.as_view(), name='confirm'),
]
