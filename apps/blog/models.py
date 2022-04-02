"""Module to create own classes (tables in database)."""
from django.db import models
from django.urls import reverse

from abstracts.models import DateTimeCustom


class Category(DateTimeCustom):
    """Category model class."""

    title = models.CharField(
        max_length=255,
        verbose_name='Наименование'
    )
    slug = models.SlugField(
        max_length=255,
        verbose_name='Url',
        unique=True
    )

    class Meta:
        """Class to change the apperance in admin."""

        ordering = ['title']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        """Magic method to return title instead of address."""
        return self.title

    def get_absolute_url(self) -> str:  # noqa
        return reverse("category", kwargs={"slug": self.slug})


class Tag(DateTimeCustom):
    """Tag model class."""

    title = models.CharField(
        max_length=50,
        verbose_name='Наименование'
    )
    slug = models.SlugField(
        max_length=255,
        verbose_name='Url',
        unique=True
    )

    class Meta:
        """Class to change the apperance in admin."""

        ordering = ['title']
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self) -> str:
        """Magic method to return title instead of address."""
        return self.title

    def get_absolute_url(self) -> str:  # noqa
        return reverse("tag_posts", kwargs={"slug": self.slug})


class Post(DateTimeCustom):
    """Tag model class."""

    title = models.CharField(
        max_length=255,
        verbose_name='Наименование'
    )
    slug = models.SlugField(
        max_length=255,
        verbose_name='Url',
        unique=True
    )
    author = models.CharField(
        max_length=100,
        verbose_name='Автор'
    )
    content = models.TextField(
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Опубликовано'
    )
    photo = models.ImageField(
        upload_to='post/photos/%Y/%m/%d/',
        blank=True,
        verbose_name='Миниатюра'
    )
    views = models.IntegerField(
        default=0,
        verbose_name='Количество просмотров'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='posts',
        verbose_name='Категория'
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='posts'
    )

    class Meta:
        """Class to change the apperance in admin."""

        ordering = ['-created_at']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self) -> str:
        """Magic method to return title instead of address."""
        return self.title

    def get_absolute_url(self) -> str:  # noqa
        return reverse("post", kwargs={"slug": self.slug})
