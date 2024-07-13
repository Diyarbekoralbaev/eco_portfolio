from rest_framework import serializers
from .models import PortfolioModel, CategoryModel


class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioModel
        fields = ('id', 'name', 'description', 'image', 'link', 'demo_video', 'team', 'category', 'created_at', 'updated_at')
        extra_kwargs = {
            'id': {'read_only': True},
            'name': {'required': True},
            'description': {'required': True},
            'image': {'required': True},
            'link': {'required': True},
            'demo_video': {'required': True},
            'team': {'required': True},
            'category': {'required': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

    def validate_image(self, value):
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError('Image size is too large.')
        return value

    def validate_link(self, value):
        if not value.startswith('http://') and not value.startswith('https://'):
            raise serializers.ValidationError('Invalid link.')
        return value

    def validate_demo_video(self, value):
        if not value.startswith('http://') and not value.startswith('https://'):
            raise serializers.ValidationError('Invalid link.')
        return value

    def validate(self, data):
        data = super().validate(data)
        return data

    def create(self, validated_data):
        portfolio = PortfolioModel.objects.create(**validated_data)
        return portfolio

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.image = validated_data.get('image', instance.image)
        instance.link = validated_data.get('link', instance.link)
        instance.demo_video = validated_data.get('demo_video', instance.demo_video)
        instance.team = validated_data.get('team', instance.team)
        instance.category = validated_data.get('category', instance.category)
        instance.save()
        return instance


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ('id', 'name')
        extra_kwargs = {
            'id': {'read_only': True},
            'name': {'required': True},
        }

    def create(self, validated_data):
        category = CategoryModel.objects.create(**validated_data)
        return category

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance