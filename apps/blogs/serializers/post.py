from rest_framework.serializers import CharField, ModelSerializer

from apps.blogs.models import Post
from apps.blogs.serializers.category import CategorySerializer
from apps.blogs.serializers.tag import TagSerializer


class PostSerializer(ModelSerializer):
    author = CharField(source="author.email", read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "slug",
            "content",
            "status",
            "created_at",
            "updated_at",
            "author",
            "categories",
            "tags",
        ]
