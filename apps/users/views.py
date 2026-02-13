from typing import Any

from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import User
from apps.users.serializers import UserLoginSerializer, UserRegisterSerializer


class UserViewSet(ViewSet):
    """ViewSet for User model."""

    permission_classes = (IsAuthenticated,)

    @action(
        methods=["POST"],
        detail=False,
        url_path="login",
        url_name="login",
        permission_classes=[AllowAny],
    )
    def login(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Login user."""

        serializer: UserLoginSerializer = UserLoginSerializer(data=request.data)  # type: ignore
        serializer.is_valid(raise_exception=True)
        user: User = serializer.validated_data.pop("user")  # type: ignore

        refresh_token: RefreshToken = RefreshToken.for_user(user)
        access_token: str = str(refresh_token.access_token)

        return Response(
            data={
                "access_token": access_token,
                "refresh_token": str(refresh_token),
            },
            status=HTTP_200_OK,
        )

    @action(
        methods=["POST"],
        detail=False,
        url_path="register",
        url_name="register",
        permission_classes=[AllowAny],
    )
    def register(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Register user."""

        serializer: UserRegisterSerializer = kwargs["serializer"]
        serializer.is_valid(raise_exception=True)

        user: User = User.objects.create_user(
            email=serializer.validated_data["email"],  # type: ignore
            password=serializer.validated_data["password"],  # type: ignore
        )

        refresh: RefreshToken = RefreshToken.for_user(user)
        access_token: str = str(refresh.access_token)

        return Response(
            data={
                "id": user.id,  # type: ignore
                "email": user.email,
                "access": access_token,
                "refresh": str(refresh),
            },
            status=HTTP_200_OK,
        )

    @action(
        methods=["GET"],
        detail=False,
        url_path="me",
        url_name="me",
        permission_classes=[IsAuthenticated],
    )
    def me(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Get current user."""

        user: User = request.user  # type: ignore

        return Response(
            data={
                "id": user.id,  # type: ignore
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "is_active": user.is_active,
                "date_joined": user.date_joined,
            },
            status=HTTP_200_OK,
        )
