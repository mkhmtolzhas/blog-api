from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.blogs.views.category import CategoryViewSet
from apps.blogs.views.tag import TagViewSet

router = DefaultRouter(trailing_slash=False)

router.register(
    prefix="tags",
    viewset=TagViewSet,
    basename="tags",
)

router.register(
    prefix="categories",
    viewset=CategoryViewSet,
    basename="categories",
)


urlpatterns = [
    path("blogs/", include(router.urls)),
]
