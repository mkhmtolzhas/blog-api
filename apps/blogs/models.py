from django.db.models import (
    CASCADE,
    SET_NULL,
    CharField,
    DateTimeField,
    ForeignKey,
    ManyToManyField,
    SlugField,
    TextChoices,
    TextField,
)

from apps.abstracts.models import AbstractBaseModel


class Category(AbstractBaseModel):
    """Model representing a category for blog posts."""

    NAME_MAX_LENGTH = 100

    name = CharField(max_length=NAME_MAX_LENGTH, unique=True)
    slug = SlugField(unique=True)

    def __str__(self):
        """String representation of the Category model."""
        return f"Name: {self.name}, Slug: {self.slug}"

    def __repr__(self):
        """Official string representation of the Category model."""
        return f"Category(name='{self.name}', slug='{self.slug}')"


class Tag(AbstractBaseModel):
    """Model representing a tag for blog posts."""

    NAME_MAX_LENGTH = 50

    name = CharField(max_length=NAME_MAX_LENGTH, unique=True)
    slug = SlugField(unique=True)

    def __str__(self):
        """String representation of the Tag model."""
        return f"Name: {self.name}, Slug: {self.slug}"

    def __repr__(self):
        """Official string representation of the Tag model."""
        return f"Tag(name='{self.name}', slug='{self.slug}')"


class Post(AbstractBaseModel):
    """Model representing a blog post."""

    TITLE_MAX_LENGTH = 200

    class StatusChoices(TextChoices):
        DRAFT = "draft", "Draft"  # type: ignore
        PUBLISHED = "published", "Published"  # type: ignore

    author = ForeignKey("users.User", on_delete=CASCADE, related_name="posts")
    title = CharField(max_length=TITLE_MAX_LENGTH)
    slug = SlugField(unique=True)
    content = TextField()
    category = ForeignKey(Category, on_delete=SET_NULL, related_name="posts", null=True, blank=True)
    tags = ManyToManyField(Tag, related_name="posts", blank=True, null=True)
    status = CharField(choices=StatusChoices.choices, default=StatusChoices.DRAFT)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)


class Comments(AbstractBaseModel):
    """Model representing a comment on a blog post."""

    post = ForeignKey(Post, on_delete=CASCADE, related_name="comments")
    author = ForeignKey("users.User", on_delete=CASCADE)
    body = TextField()
    created_at = DateTimeField(auto_now_add=True)
