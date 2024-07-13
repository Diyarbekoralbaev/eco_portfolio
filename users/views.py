from .serializers import UserSerializer, LoginSerializer, ResponseUserSerializer, ResponseLoginSerializer, \
    RefreshTokenSerializer, ResponseRefreshTokenSerializer, TeamSerializer, ResponseTeamSerializer, AddMemberToTeamSerializer, \
    DeleteTeamSerializer, RemoveMemberFromTeamSerializer, UpdateTeamSerializer
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import UserModel, TeamModel


class RegisterUserView(APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={
            201: openapi.Response(
                'User created successfully.',
                ResponseUserSerializer,
            ),
        },
        tags=['users'],
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(
                'User logged in successfully.',
                ResponseLoginSerializer,
            ),
        },
        tags=['users'],
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserMeView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                'User details retrieved successfully.',
                ResponseUserSerializer,
            ),
        },
        tags=['users'],
    )
    def get(self, request):
        serializer = ResponseUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                'User details retrieved successfully.',
                ResponseUserSerializer,
            ),
        },
        tags=['users'],
    )
    def get(self, request, user_id):
        user = UserModel.objects.get(id=user_id)
        serializer = ResponseUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UsersListView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                'Users retrieved successfully.',
                ResponseUserSerializer,
            ),
        },
        tags=['users'],
    )
    def get(self, request):
        users = UserModel.objects.all()
        serializer = ResponseUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RefreshTokenView(APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        request_body=RefreshTokenSerializer,
        responses={
            200: openapi.Response(
                'Token refreshed successfully.',
                ResponseRefreshTokenSerializer,
            ),
        },
        tags=['users'],
    )
    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeamCreateView(APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        request_body=TeamSerializer,
        responses={
            201: openapi.Response(
                'Team created successfully.',
                ResponseTeamSerializer,
            ),
        },
        tags=['teams'],
    )
    def post(self, request):
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeamListView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                'Teams retrieved successfully.',
                ResponseTeamSerializer,
            ),
        },
        tags=['teams'],
    )
    def get(self, request):
        teams = TeamModel.objects.filter(members=request.user)
        serializer = ResponseTeamSerializer(teams, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TeamUpdateView(APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        request_body=UpdateTeamSerializer,
        responses={
            200: openapi.Response(
                'Team updated successfully.',
                ResponseTeamSerializer,
            ),
        },
        tags=['teams'],
    )
    def put(self, request):
        team = TeamModel.objects.get(id=request.data['team_id'])
        serializer = UpdateTeamSerializer(team, data=request.data)
        if serializer.is_valid():
            team = TeamModel.objects.get(id=request.data['team_id'])
            team.name = request.data['name']
            team.save()
            response = ResponseTeamSerializer(team)
            return Response(response.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeamDeleteView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        request_body=DeleteTeamSerializer,
        responses={
            204: openapi.Response(
                'Team deleted successfully.',
            ),
        },
        tags=['teams'],
    )
    def delete(self, request):
        team = TeamModel.objects.get(id=request.data['team_id'])
        team.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TeamAddMemberView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        request_body=AddMemberToTeamSerializer,
        responses={
            200: openapi.Response(
                'Member added to team successfully.',
                ResponseTeamSerializer,
            ),
        },
        tags=['teams'],
    )
    def post(self, request):
        team = TeamModel.objects.get(id=request.data['team_id'])
        user = UserModel.objects.get(id=request.data['user_id'])
        team.members.add(user)
        serializer = ResponseTeamSerializer(team)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TeamRemoveMemberView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        request_body=RemoveMemberFromTeamSerializer,
        responses={
            200: openapi.Response(
                'Member removed from team successfully.',
                ResponseTeamSerializer,
            ),
        },
        tags=['teams'],
    )
    def post(self, request):
        team = TeamModel.objects.get(id=request.data['team_id'])
        user = UserModel.objects.get(id=request.data['user_id'])
        team.members.remove(user)
        serializer = ResponseTeamSerializer(team)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TeamDetailView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                'Team details retrieved successfully.',
                ResponseTeamSerializer,
            ),
        },
        tags=['teams'],
    )
    def get(self, request, team_id):
        team = TeamModel.objects.get(id=team_id)
        serializer = ResponseTeamSerializer(team)
        return Response(serializer.data, status=status.HTTP_200_OK)