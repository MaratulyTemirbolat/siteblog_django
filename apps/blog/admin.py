"""Module to setting and register models in admin."""
from typing import (
    Optional,
)

from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from blog.models import (
    Category,
    Tag,
    Post,
)


class PostAdminForm(forms.ModelForm):
    """CkEditor form to be used in Post for admin."""

    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        """Used to determine for whick model and fields it is used."""

        model = Post
        fields = '__all__'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Class to setting Post in Admin."""

    list_display: tuple = (
        'id', 'title', 'slug',
        'category', 'created_at',
        'get_photo', 'views',
    )
    list_display_links: tuple = ('id', 'title',)
    search_fields: tuple = ('title',)
    list_filter: tuple = ('category', 'tags',)
    readonly_fields: tuple = ('views', 'created_at',
                              'get_photo', 'datetime_created',
                              'datetime_updated', 'datetime_deleted',
                              'is_deleted',)
    fields: tuple = (
        ('title', 'slug'), 'category',
        'tags', 'content', 'created_at',
        ('photo', 'get_photo'), 'views',
        'author',
    )
    prepopulated_fields: dict = {
        "slug": ("title",),
    }
    form = PostAdminForm
    save_as: bool = True
    save_on_top: bool = True
    # Благодря этому появится кнопка "сохранить как новый объект"
    # Из-за этого новый пост будет создан на основе текущего (редактирующего)
    filter_horizontal: tuple = ('tags',)

    def get_photo(self, obj: Optional[Post], width: int = 100) -> str:  # noqa
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="{width}">')

    get_photo.short_description = "Миниатюра"
    get_photo.empty_value_display = "No photo uploaded"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Class to setting Category in Admin."""

    readonly_fields: tuple = ('datetime_created', 'datetime_updated',
                              'datetime_deleted', 'is_deleted')
    prepopulated_fields: dict = {"slug": ("title",)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Class to setting Tag in Admin."""

    readonly_fields: tuple = ('datetime_created', 'datetime_updated',
                              'datetime_deleted', 'is_deleted')
    prepopulated_fields: dict = {"slug": ("title",)}
