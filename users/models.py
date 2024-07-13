from django.db import models
from django.contrib.auth.models import AbstractUser


ROLE_CHOICES = (
    ('superadmin', 'Superadmin'),
    ('pm', 'Project Manager'),
    ('developer', 'Developer'),
    ('not_assigned', 'Not Assigned'),
)


class UserModel(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    telegram = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='not_assigned')
    skills = models.JSONField(default=list, blank=True, null=True)

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'


class TeamModel(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(UserModel, related_name='teams', blank=True, null=True)

    def __str__(self):
        return self.name
