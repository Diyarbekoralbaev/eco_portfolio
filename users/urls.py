from django.urls import path
from .views import RegisterUserView, UsersListView, RefreshTokenView, UserMeView, UserDetailView, LoginView, \
    TeamView, TeamAddMemberView, TeamRemoveMemberView, TeamDetailView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('me/', UserMeView.as_view(), name='me'),
    path('refresh-token/', RefreshTokenView.as_view(), name='refresh-token'),
    path('users/', UsersListView.as_view(), name='users-list'),
    path('user/<int:user_id>/', UserDetailView.as_view(), name='user-detail'),

    path('teams/', TeamView.as_view(), name='teams'),
    path('team/<int:team_id>/', TeamDetailView.as_view(), name='team-detail'),
    path('team/<int:team_id>/add-member/', TeamAddMemberView.as_view(), name='team-add-member'),
    path('team/<int:team_id>/remove-member/', TeamRemoveMemberView.as_view(), name='team-remove-member'),
]
