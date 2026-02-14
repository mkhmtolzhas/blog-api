from rest_framework.serializers import CharField, ModelSerializer, SlugField

from apps.blogs.models import Category, Comments, Post, Tag


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]


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


class CommentSerializer(ModelSerializer):
    author = CharField(source="author.email", read_only=True)
    post = SlugField(source="post.slug", read_only=True)

    class Meta:
        model = Comments
        fields = [
            "id",
            "content",
            "created_at",
            "updated_at",
            "author",
            "post",
        ]
