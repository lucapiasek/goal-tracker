from django.urls import path
from . import views

app_name = 'tasks'
urlpatterns = [
    path('<str:username>/tasks/', views.TaskListView.as_view(), name='list'),
    path('<str:username>/tasks/<int:pk>/', views.TaskDetailView.as_view(), name='detail'),
    path('<str:username>/tasks/new', views.TaskCreateView.as_view(), name='create'),
    path('<str:username>/tasks/<int:pk>/update', views.TaskUpdateView.as_view(), name='update'),
    path('<str:username>/tasks/<int:pk>/delete', views.TaskDeleteView.as_view(), name='delete'),
    path('<str:username>/tasks/<int:pk>/practice', views.PracticeCreateView.as_view(), name='practice_create'),
    path('<str:username>/practice/<int:pk>', views.PracticeUpdateView.as_view(), name='practice_update'),
    path('<str:username>/practice/<int:pk>/delete', views.PracticeDeleteView.as_view(), name='practice_delete'),
]
