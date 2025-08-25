from django.urls import path
from . import views

app_name = 'suggestions'
urlpatterns = [
    path('<str:username>/suggestions/', views.SuggestionsListView.as_view(), name='list'),
]
