from rest_framework.serializers import ModelSerializer

from apps.blogs.models import Category


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]
