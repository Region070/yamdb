from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

CHOICES = (
    ('user', 'authenticated_user'),
    ('moderator', 'moderator'),
    ('admin', 'administrator'),
)


class User(AbstractUser):
    role = models.CharField(
        verbose_name='Роль',
        max_length=20,
        choices=CHOICES,
        default=CHOICES[0][0],
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )

    def is_admin(self):
        return self.role == 'admin'

    def is_moderator(self):
        return self.role == 'moderator'


class Genre(models.Model):
    """Модель жанры"""
    name = models.CharField(max_length=50, unique=True,)
    slug = models.SlugField(max_length=20, unique=True,)

    def __str__(self):
        return self.name


class Category(models.Model):
    """Модель категория"""
    name = models.CharField(max_length=50, unique=True,)
    slug = models.SlugField(max_length=20, unique=True,)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведения"""
    name = models.CharField(max_length=200)
    year = models.PositiveSmallIntegerField()
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True
    )
    genre = models.ManyToManyField(
        Genre, related_name='titles', blank=True
    )
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    """Model for reviews."""
    text = models.TextField()
    author = models.ForeignKey('User', on_delete=models.CASCADE,
                               related_name='reviews')
    title = models.ForeignKey('Title', on_delete=models.CASCADE,
                              related_name='reviews')
    score = models.SmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)])
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_title_author'
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Model for comments."""
    text = models.TextField()
    author = models.ForeignKey('User', on_delete=models.CASCADE,
                               related_name='comments')
    pub_date = models.DateTimeField(auto_now_add=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
