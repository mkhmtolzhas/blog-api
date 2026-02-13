from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.blogs.models import Category, Comments, Post, Tag
from apps.blogs.serializers import (
    CategorySerializer,
    CommentSerializer,
    PostSerializer,
    TagSerializer,
)


