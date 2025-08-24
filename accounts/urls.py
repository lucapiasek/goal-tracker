from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

app_name = 'accounts'

urlpatterns = [
    path('user/new/', views.UserCreateView.as_view(), name='user_create'),
    path('/login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('user/<str:username>/', views.UserDetailView.as_view(), name='user_detail'),
    path('user/update', views.UserUpdateView.as_view(), name='user_update'),
    path('user/invite-teacher', views.StudentInviteView.as_view(), name='invite_teacher'),
    path('user/invite-student', views.TeacherInviteView.as_view(), name='invite_student'),
    path('user/accept-student/<str:username>', views.AcceptStudentInvitationView.as_view(), name='accept_student'),
    path('user/accept-teacher/<str:username>', views.AcceptTeacherInvitationView.as_view(), name='accept_teacher'),
    path('user/invitations', views.InvitationListView.as_view(), name='invitation_list')
]