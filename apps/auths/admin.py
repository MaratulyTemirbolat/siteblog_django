from typing import Optional

from django.contrib import admin
from django.utils.safestring import mark_safe

from auths.models import (
    CustomUser
)


@admin.register(CustomUser)
class CustomUserModel(admin.ModelAdmin):  # noqa
    list_display: tuple = ('email', 'name',
                           'surname', 'is_superuser',
                           'is_active', 'is_deleted',
                           'get_photo',)
    readonly_fields: tuple = ('get_photo', 'datetime_updated',
                              'is_deleted', 'datetime_deleted',
                              'last_login', 'password', )
    list_filter: tuple = ('is_deleted',)
    save_on_top: bool = True

    def get_photo(self, obj: Optional[CustomUser],
                  width: int = 100) -> str:  # noqa
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="{width}">')

    get_photo.short_description = "Фото"
    get_photo.empty_value_display = "No photo uploaded"
