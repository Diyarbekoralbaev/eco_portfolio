from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import PortfolioModel, CategoryModel
from .serializers import PortfolioSerializer, CategorySerializer


class PortfolioView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @swagger_auto_schema(
        request_body=PortfolioSerializer,
        responses={
            201: openapi.Response(
                'Portfolio created successfully.',
                PortfolioSerializer,
            ),
        },
        tags=['portfolio'],
    )
    def post(self, request):
        serializer = PortfolioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                'Portfolio details retrieved successfully.',
                PortfolioSerializer,
            ),
        },
        tags=['portfolio'],
    )
    def get(self, request):
        portfolios = PortfolioModel.objects.all()
        serializer = PortfolioSerializer(portfolios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PortfolioDetailView(APIView):
    # def get_permissions(self):
    #     if self.request.method in ['PUT', 'DELETE']:
    #         return [permissions.IsAuthenticated()]
    #     return [permissions.AllowAny()]

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                'Portfolio details retrieved successfully.',
                PortfolioSerializer,
            ),
        },
        tags=['portfolio'],
    )
    def get(self, request, pk):
        portfolio = PortfolioModel.objects.get(pk=pk)
        serializer = PortfolioSerializer(portfolio)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=PortfolioSerializer,
        responses={
            200: openapi.Response(
                'Portfolio updated successfully.',
                PortfolioSerializer,
            ),
        },
        tags=['portfolio'],
    )
    def put(self, request, pk):
        portfolio = PortfolioModel.objects.get(pk=pk)
        serializer = PortfolioSerializer(portfolio, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={
            204: openapi.Response(
                'Portfolio deleted successfully.',
            ),
        },
        tags=['portfolio'],
    )
    def delete(self, request, pk):
        portfolio = PortfolioModel.objects.get(pk=pk)
        portfolio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @swagger_auto_schema(
        request_body=CategorySerializer,
        responses={
            201: openapi.Response(
                'Category created successfully.',
                CategorySerializer,
            ),
        },
        tags=['category'],
    )
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                'Category details retrieved successfully.',
                CategorySerializer,
            ),
        },
        tags=['category'],
    )
    def get(self, request):
        categories = CategoryModel.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryDetailView(APIView):
    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                'Category details retrieved successfully.',
                CategorySerializer,
            ),
        },
        tags=['category'],
    )
    def get(self, request, pk):
        category = CategoryModel.objects.get(pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=CategorySerializer,
        responses={
            200: openapi.Response(
                'Category updated successfully.',
                CategorySerializer,
            ),
        },
        tags=['category'],
    )
    def put(self, request, pk):
        category = CategoryModel.objects.get(pk=pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={
            204: openapi.Response(
                'Category deleted successfully.',
            ),
        },
        tags=['category'],
    )
    def delete(self, request, pk):
        category = CategoryModel.objects.get(pk=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)