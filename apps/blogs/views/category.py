from typing import Any

from django.db.models import QuerySet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND)
from rest_framework.viewsets import ViewSet

from apps.blogs.models import Category
from apps.blogs.serializers.category import CategorySerializer


class CategoryViewSet(ViewSet):
    """ViewSet for managing blog categories."""

    serializer_class = CategorySerializer
    queryset = Category.objects.filter(  # type: ignore
        deleted_at__isnull=True,
    )  # type: ignore

    def get_object(self) -> Category:
        """Get a category by its ID."""

        self.queryset.filter(
            id=self.kwargs["pk"],  # type: ignore
        )
        return self.queryset.get(id=self.kwargs["pk"])  # type: ignore

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """List all categories."""

        all_categories: QuerySet[Category] = self.queryset.all()  # type: ignore

        serializer: CategorySerializer = CategorySerializer(
            all_categories,
            many=True,
        )  # type: ignore

        return Response(
            data=serializer.data,
            status=HTTP_200_OK,
        )

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Create a new category."""

        serializer: CategorySerializer = CategorySerializer(data=request.data)  # type: ignore
        serializer.is_valid(raise_exception=True)

        category: Category = serializer.save()  # type: ignore

        return Response(
            status=HTTP_201_CREATED,
            headers={
                "Location": f"/api/blogs/categories/{category.id}",  # type: ignore
            },
        )

    def partial_update(
        self, request: Request, pk=None, *args: Any, **kwargs: Any
    ) -> Response:
        """Partially update a category."""

        try:
            serializer: CategorySerializer = CategorySerializer(
                self.get_object(),  # type: ignore
                data=request.data,  # type: ignore
                partial=True,
            )  # type: ignore
            serializer.is_valid(raise_exception=True)

            serializer.save()

            return Response(
                data=serializer.data,
                status=HTTP_200_OK,
            )
        except Category.DoesNotExist:  # type: ignore
            return Response(
                data={"detail": "Category not found."},
                status=HTTP_404_NOT_FOUND,
            )

    def update(self, request: Request, pk=None, *args: Any, **kwargs: Any) -> Response:
        """Update a category."""

        try:
            serializer: CategorySerializer = CategorySerializer(
                self.get_object(),  # type: ignore
                data=request.data,  # type: ignore
            )  # type: ignore

            serializer.is_valid(raise_exception=True)

            serializer.save()

            return Response(
                data=serializer.data,
                status=HTTP_200_OK,
            )
        except Category.DoesNotExist:  # type: ignore
            return Response(
                data={"detail": "Category not found."},
                status=HTTP_404_NOT_FOUND,
            )

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Delete a category."""

        try:
            category: Category = self.get_object()

            category.delete()

            return Response(
                status=HTTP_204_NO_CONTENT,
            )
        except Category.DoesNotExist:  # type: ignore
            return Response(
                data={"detail": "Category not found."},
                status=HTTP_404_NOT_FOUND,
            )

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Retrieve a category."""

        try:
            category: Category = self.get_object()

            serializer: CategorySerializer = CategorySerializer(category)  # type: ignore

            return Response(
                data=serializer.data,
                status=HTTP_200_OK,
            )
        except Category.DoesNotExist:  # type: ignore
            return Response(
                data={"detail": "Category not found."},
                status=HTTP_404_NOT_FOUND,
            )
