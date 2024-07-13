from django.urls import path
from .views import PortfolioView, PortfolioDetailView, CategoryView, CategoryDetailView


urlpatterns = [
    path('', PortfolioView.as_view(), name='portfolio'),
    path('<int:pk>/', PortfolioDetailView.as_view(), name='portfolio-detail'),
    path('categories/', CategoryView.as_view(), name='categories'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
]