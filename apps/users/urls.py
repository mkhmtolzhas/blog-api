from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from apps.users.views import UserViewSet

router: DefaultRouter = DefaultRouter(trailing_slash=False)

router.register(
    prefix="auth",
    viewset=UserViewSet,
    basename="auth",
)


urlpatterns = [
    path("", include(router.urls)),
    path("auth/refresh", TokenRefreshView.as_view(), name="token_refresh"),
]
