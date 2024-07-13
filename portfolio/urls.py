from django.urls import path
from .views import PortfolioView, PortfolioDetailView


urlpatterns = [
    path('', PortfolioView.as_view(), name='portfolio'),
    path('<int:pk>/', PortfolioDetailView.as_view(), name='portfolio-detail'),
]