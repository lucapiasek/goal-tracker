from django.urls import path
from . import views

app_name = 'tracker'
urlpatterns = [
    path('<str:username>/goals/', views.GoalListView.as_view(), name='goal_list'),
    path('<str:username>/goals/<int:pk>/', views.GoalDetailView.as_view(), name='goal_detail'),
    path('<str:username>/goals/new', views.GoalCreateView.as_view(), name='goal_create'),
    path('<str:username>/goals/<int:pk>/update', views.GoalUpdateView.as_view(), name='goal_update'),
    path('<str:username>/goals/<int:pk>/delete', views.GoalDeleteView.as_view(), name='goal_delete'),
    path('<str:username>/pieces/', views.PieceListView.as_view(), name='piece_list'),
    path('<str:username>/pieces/<int:pk>/', views.PieceDetailView.as_view(), name='piece_detail'),
    path('<str:username>/pieces/new', views.PieceCreateView.as_view(), name='piece_create'),
    path('<str:username>/pieces/<int:pk>/update', views.PieceUpdateView.as_view(), name='piece_update'),
    path('<str:username>/pieces/<int:pk>/delete', views.PieceDeleteView.as_view(), name='piece_delete'),
    path('<str:username>/styles/', views.StyleListView.as_view(), name='style_list'),
    path('<str:username>/styles/new', views.StyleCreateView.as_view(), name='style_create'),
    path('<str:username>/styles/<int:pk>/update', views.StyleUpdateView.as_view(), name='style_update'),
    path('<str:username>/styles/<int:pk>/delete', views.StyleDeleteView.as_view(), name='style_delete'),
]