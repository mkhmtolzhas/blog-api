from typing import Any

from django.db.models import QuerySet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND)
from rest_framework.viewsets import ViewSet

from apps.blogs.models import Tag
from apps.blogs.serializers.tag import TagSerializer


class TagViewSet(ViewSet):
    """ViewSet for managing blog tags."""

    serializer_class = TagSerializer
    queryset = Tag.objects.filter(  # type: ignore
        deleted_at__isnull=True,
    )  # type: ignore

    def get_object(self) -> Tag:
        """Get a tag by its ID."""

        self.queryset.filter(
            id=self.kwargs["pk"],  # type: ignore
        )
        return self.queryset.get(id=self.kwargs["pk"])  # type: ignore

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """List all tags."""

        all_tags: QuerySet[Tag] = self.queryset.all()  # type: ignore

        serializer: TagSerializer = TagSerializer(
            all_tags,
            many=True,
        )  # type: ignore

        return Response(
            data=serializer.data,
            status=HTTP_200_OK,
        )

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Create a new tag."""

        serializer: TagSerializer = TagSerializer(data=request.data)  # type: ignore
        serializer.is_valid(raise_exception=True)

        tag: Tag = serializer.save()  # type: ignore

        return Response(
            status=HTTP_201_CREATED,
            headers={
                "Location": f"/api/blogs/tags/{tag.id}",  # type: ignore
            },
        )

    def partial_update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Partially update a tag."""

        try:
            serializer: TagSerializer = TagSerializer(
                self.get_object(),
                data=request.data,
                partial=True,
            )  # type: ignore

            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(
                data=serializer.data,
                status=HTTP_200_OK,
            )
        except Tag.DoesNotExist:  # type: ignore
            return Response(
                data={"detail": "Tag not found."},
                status=HTTP_404_NOT_FOUND,
            )

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Soft delete a tag."""

        try:
            tag: Tag = self.get_object()  # type: ignore

            tag.delete()

            return Response(status=HTTP_204_NO_CONTENT)
        except Tag.DoesNotExist:  # type: ignore
            return Response(
                data={"detail": "Tag not found."},
                status=HTTP_404_NOT_FOUND,
            )

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Update a tag."""

        try:
            serializer: TagSerializer = TagSerializer(
                self.get_object(),
                data=request.data,
            )  # type: ignore

            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(
                data=serializer.data,
                status=HTTP_200_OK,
            )
        except Tag.DoesNotExist:  # type: ignore
            return Response(
                data={"detail": "Tag not found."},
                status=HTTP_404_NOT_FOUND,
            )

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Retrieve a tag by its ID."""

        try:
            tag: Tag = self.get_object()  # type: ignore

            serializer: TagSerializer = TagSerializer(tag)  # type: ignore

            return Response(
                data=serializer.data,
                status=HTTP_200_OK,
            )
        except Tag.DoesNotExist:  # type: ignore
            return Response(
                data={"detail": "Tag not found."},
                status=HTTP_404_NOT_FOUND,
            )
