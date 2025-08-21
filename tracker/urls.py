from django.urls import path
from . import views

app_name = 'tracker'
urlpatterns = [
    path('<str:username>/goals/', views.GoalListView.as_view(), name='goal_list'),
    path('<str:username>/goals/<int:pk>/', views.GoalDetailView.as_view(), name='goal_detail'),
    path('<str:username>/goals/new', views.GoalCreateView.as_view(), name='goal_create'),
    path('<str:username>/goals/<int:pk>/update', views.GoalUpdateView.as_view(), name='goal_update'),
    path('<str:username>/goals/<int:pk>/delete', views.GoalDeleteView.as_view(), name='goal_delete'),
    path('pieces/', views.PiecesView.as_view(), name='pieces')
]