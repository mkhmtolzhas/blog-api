from typing import Any, Optional

from rest_framework.exceptions import ValidationError
from rest_framework.serializers import CharField, EmailField, Serializer

from apps.users.models import User


class UserLoginSerializer(Serializer):
    email = EmailField(required=True, max_length=User.EMAIL_MAX_LENGTH)
    password = CharField(required=True, max_length=User.PASSWORD_MAX_LENGTH)

    class Meta:
        fields = ["email", "password"]

    def validate_email(self, value: str) -> str:
        """Validates the email field."""
        return value.lower()

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        """Validates the input data."""
        email: str = attrs["email"]
        password: str = attrs["password"]

        user: Optional[User] = User.objects.filter(email=email).first()

        if not user:
            raise ValidationError(
                detail={"email": [f"User with email '{email}' does not exist."]}
            )

        if not user.check_password(raw_password=password):
            raise ValidationError(detail={"password": ["Incorrect password."]})

        attrs["user"] = user

        return super().validate(attrs)


class UserRegisterSerializer(Serializer):
    email = EmailField(required=True, max_length=User.EMAIL_MAX_LENGTH)
    password = CharField(required=True, max_length=User.PASSWORD_MAX_LENGTH)
    first_name = CharField(required=False, max_length=User.FULL_NAME_MAX_LENGTH)
    last_name = CharField(required=False, max_length=User.FULL_NAME_MAX_LENGTH)

    class Meta:
        fields = ["email", "password", "first_name", "last_name"]

    def validate_password(self, value: str) -> str:
        """Validates the password field."""

        password: str = value.strip()
        if len(password) < 8:
            raise ValidationError(
                detail={"password": ["Password must be at least 8 characters long."]}
            )

        return value

    def validate_email(self, value: str) -> str:
        """Validates the email field."""
        email: str = value.lower()

        if User.objects.filter(email=email).exists():
            raise ValidationError(
                detail={"email": [f"User with email '{email}' already exists."]}
            )

        return email
