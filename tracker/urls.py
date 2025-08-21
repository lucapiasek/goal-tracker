from django.urls import path
from . import views

app_name = 'tracker'
urlpatterns = [
    path('<str:username>/goals/', views.GoalListView.as_view(), name='goal_list'),
    path('<str:username>/goals/<int:pk>/', views.GoalDetailView.as_view(), name='goal_detail'),
    path('<str:username>/goal/new', views.GoalCreateView.as_view(), name='goal-create'),
    path('<str:username>/goal/<int:pk>/update', views.GoalUpdateView.as_view(), name='goal_update'),
    path('<str:username>/goal/<int:pk>/delete', views.GoalDeleteView.as_view(), name='goal_delete'),
    path('pieces/', views.PiecesView.as_view(), name='pieces')
]