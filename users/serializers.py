from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
import re
from .models import UserModel, TeamModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'phone_number', 'telegram', 'role', 'skills')
        extra_kwargs = {
            'id': {'read_only': True},
            'username': {'required': True},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'email': {'required': True},
            'password': {'write_only': True},
            'phone_number': {'required': False},
            'telegram': {'required': False},
            'role': {'required': False},
            'skills': {'required': False},
        }

    def validate_email(self, value):
        if UserModel.objects.filter(email=value).exists():
            raise serializers.ValidationError('This email is already taken.')
        return value

    def validate_username(self, value):
        if UserModel.objects.filter(username=value).exists():
            raise serializers.ValidationError('This username is already taken.')
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('Password must be at least 8 characters long.')
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError('Password must contain at least one uppercase letter.')
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError('Password must contain at least one lowercase letter.')
        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError('Password must contain at least one digit.')
        if not re.search(r'[.!@#$%^&*()_+=-]', value):
            raise serializers.ValidationError('Password must contain at least one special character.')
        return value

    def validate(self, data):
        data = super().validate(data)
        return data

    def create(self, validated_data):
        user = UserModel.objects.create_user(**validated_data)
        return user


class ResponseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'phone_number', 'telegram', 'role', 'skills')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username:
            raise serializers.ValidationError('Username is required.')
        if not password:
            raise serializers.ValidationError('Password is required.')

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError('Incorrect credentials.')
        if not user.is_active:
            raise serializers.ValidationError('User account is disabled.')

        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'phone_number': user.phone_number,
                'telegram': user.telegram,
                'role': user.role,
                'skills': user.skills,
            }
        }


class ResponseLoginSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
    user = ResponseUserSerializer()


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, data):
        refresh = data.get('refresh')

        try:
            token = RefreshToken(refresh)
            token.verify()
            token.blacklist()
        except Exception as e:
            raise serializers.ValidationError(str(e))

        return {
            'access': str(token.access_token),
        }


class ResponseRefreshTokenSerializer(serializers.Serializer):
    access = serializers.CharField()


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamModel
        fields = ('id', 'name', 'members')
        extra_kwargs = {
            'id': {'read_only': True},
            'name': {'required': True},
            'members': {'required': False},
        }

    def validate_name(self, value):
        if TeamModel.objects.filter(name=value).exists():
            raise serializers.ValidationError('This team name is already taken.')
        return value

    def validate(self, data):
        data = super().validate(data)
        return data

    def create(self, validated_data):
        team = TeamModel.objects.create(**validated_data)
        return team


class ResponseTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamModel
        fields = ('id', 'name', 'members')
        depth = 1


class AddMemberToTeamSerializer(serializers.Serializer):
    team_id = serializers.IntegerField()
    user_id = serializers.IntegerField()

    def validate(self, data):
        team_id = data.get('team_id')
        user_id = data.get('user_id')

        if not TeamModel.objects.filter(id=team_id).exists():
            raise serializers.ValidationError('Team does not exist.')
        if not UserModel.objects.filter(id=user_id).exists():
            raise serializers.ValidationError('User does not exist.')

        return data


class RemoveMemberFromTeamSerializer(serializers.Serializer):
    team_id = serializers.IntegerField()
    user_id = serializers.IntegerField()

    def validate(self, data):
        team_id = data.get('team_id')
        user_id = data.get('user_id')

        if not TeamModel.objects.filter(id=team_id).exists():
            raise serializers.ValidationError('Team does not exist.')
        if not UserModel.objects.filter(id=user_id).exists():
            raise serializers.ValidationError('User does not exist.')

        return data


class UpdateTeamSerializer(serializers.Serializer):
    team_id = serializers.IntegerField()
    name = serializers.CharField()

    def validate(self, data):
        team_id = data.get('team_id')
        name = data.get('name')

        if not TeamModel.objects.filter(id=team_id).exists():
            raise serializers.ValidationError('Team does not exist.')
        if TeamModel.objects.filter(name=name).exists():
            raise serializers.ValidationError('This team name is already taken.')

        return data


class DeleteTeamSerializer(serializers.Serializer):
    team_id = serializers.IntegerField()

    def validate(self, data):
        team_id = data.get('team_id')

        if not TeamModel.objects.filter(id=team_id).exists():
            raise serializers.ValidationError('Team does not exist.')

        return data


