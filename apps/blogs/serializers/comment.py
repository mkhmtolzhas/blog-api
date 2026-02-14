from rest_framework.serializers import CharField, ModelSerializer, SlugField

from apps.blogs.models import Comments


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
