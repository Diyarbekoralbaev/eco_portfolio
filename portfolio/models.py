from django.db import models
from users.models import TeamModel


class PortfolioModel(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(db_index=True)
    image = models.ImageField(upload_to='portfolio/')
    link = models.URLField()
    demo_video = models.URLField()
    team = models.ForeignKey(TeamModel, on_delete=models.CASCADE, related_name='portfolio')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
