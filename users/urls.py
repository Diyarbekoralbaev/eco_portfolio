from django.urls import path
from .views import RegisterUserView, UsersListView, RefreshTokenView, UserMeView, UserDetailView, LoginView, \
    TeamListView, TeamAddMemberView, TeamUpdateView, TeamRemoveMemberView, TeamDetailView, TeamDeleteView, \
    TeamCreateView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('me/', UserMeView.as_view(), name='me'),
    path('refresh-token/', RefreshTokenView.as_view(), name='refresh-token'),
    path('users/', UsersListView.as_view(), name='users-list'),
    path('user/<int:user_id>/', UserDetailView.as_view(), name='user-detail'),

    path('teams/', TeamListView.as_view(), name='teams-list'),
    path('teams/create/', TeamCreateView.as_view(), name='teams-create'),
    path('teams/<int:team_id>/', TeamDetailView.as_view(), name='teams-detail'),
    path('teams/update/', TeamUpdateView.as_view(), name='teams-update'),
    path('teams/delete/', TeamDeleteView.as_view(), name='teams-delete'),
    path('teams/add-member/', TeamAddMemberView.as_view(), name='teams-add-member'),
    path('teams/remove-member/', TeamRemoveMemberView.as_view(), name='teams-remove-member'),
]
