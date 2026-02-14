from typing import Any

from django.db.models import QuerySet
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_401_UNAUTHORIZED
)
from rest_framework.viewsets import ViewSet

from apps.blogs.models import Post
from apps.blogs.serializers.comment import CommentSerializer
from apps.blogs.serializers.post import PostSerializer


class PostViewSet(ViewSet):
    """ViewSet for managing blog posts."""

    serializer_class = PostSerializer
    queryset = Post.objects.filter(  # type: ignore
        deleted_at__isnull=True,
    )  # type: ignore

    def get_permissions(self):
        if self.action in ["create", "partial_update", "destroy"]:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_object(self) -> Post:
        """Get a post by its ID."""

        self.queryset.filter(
            id=self.kwargs["pk"],  # type: ignore
        )
        return self.queryset.get(slug=self.kwargs["pk"])  # type: ignore

    def get_object_by_slug(self) -> Post:
        """Get a post by its slug."""
        return get_object_or_404(
            self.queryset,
            slug=self.kwargs["pk"],
            deleted_at__isnull=True,
        )

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """List all posts."""

        all_posts: QuerySet[Post] = self.queryset.all()  # type: ignore

        serializer: PostSerializer = PostSerializer(
            all_posts,
            many=True,
        )  # type: ignore

        return Response(
            data=serializer.data,
            status=HTTP_200_OK,
        )

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Create a new post."""

        serializer: PostSerializer = PostSerializer(data=request.data)  # type: ignore
        serializer.is_valid(raise_exception=True)

        post: Post = serializer.save(author=request.user)  # type: ignore

        return Response(
            status=HTTP_201_CREATED,
            headers={
                "Location": f"/api/blogs/posts/{post.slug}",  # type: ignore
            },
        )

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Retrieve a post by its ID."""

        try:
            post: Post = self.get_object_by_slug()  # type: ignore

            serializer: PostSerializer = PostSerializer(post)  # type: ignore

            return Response(
                data=serializer.data,
                status=HTTP_200_OK,
            )
        except Post.DoesNotExist:  # type: ignore
            return Response(
                status=HTTP_404_NOT_FOUND,
            )

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Soft delete a post by its ID."""

        try:
            post: Post = self.get_object_by_slug()  # type: ignore

            post.delete()  # type: ignore

            return Response(
                status=HTTP_204_NO_CONTENT,
            )
        except Post.DoesNotExist:  # type: ignore
            return Response(
                status=HTTP_404_NOT_FOUND,
            )

    def partial_update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        try:
            post: Post = self.get_object_by_slug()  # type: ignore

            serializer: PostSerializer = PostSerializer(
                post,
                data=request.data,
                partial=True,
            )  # type: ignore

            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(
                data=serializer.data,
                status=HTTP_200_OK,
            )
        except Post.DoesNotExist:  # type: ignore
            return Response(
                data={"detail": "Post not found."},
                status=HTTP_404_NOT_FOUND,
            )

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        try:
            post: Post = self.get_object_by_slug()  # type: ignore

            serializer: PostSerializer = PostSerializer(
                post,
                data=request.data,
            )  # type: ignore

            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(
                data=serializer.data,
                status=HTTP_200_OK,
            )
        except Post.DoesNotExist:  # type: ignore
            return Response(
                data={"detail": "Post not found."},
                status=HTTP_404_NOT_FOUND,
            )

    @action(
        methods=["GET", "POST"],
        detail=True,
        url_path="comments",
        url_name="post-comments",
        permission_classes=[AllowAny],
    )
    def comments(self, request: Request, *args: Any, **kwargs: Any) -> Response:  # type: ignore
        """List all comments for a post."""
        post: Post = self.get_object_by_slug()  # type: ignore

        if request.method == "GET":
            comments = post.comments.filter(deleted_at__isnull=True)  # type: ignore
            serializer = CommentSerializer(comments, many=True)  # type: ignore
            return Response(
                data=serializer.data,
                status=HTTP_200_OK,
            )
        elif request.method == "POST":
            try:
                self.permission_classes = [IsAuthenticated]
                self.check_permissions(request)
                serializer = CommentSerializer(data=request.data)  # type: ignore
                serializer.is_valid(raise_exception=True)
                serializer.save(author=request.user, post=post)  # type: ignore
                return Response(
                    data=serializer.data,
                    status=HTTP_201_CREATED,
                )
            except ValueError:  # type: ignore
                return Response(
                    data={"detail": "Unauthenticated."},
                    status=HTTP_404_NOT_FOUND,
                )
