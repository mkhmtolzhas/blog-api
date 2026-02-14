from rest_framework.serializers import ModelSerializer

from apps.blogs.models import Tag


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]
