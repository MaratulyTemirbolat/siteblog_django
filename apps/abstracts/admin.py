from django.contrib import admin


class DateTimeCustomAdmin(admin.ModelAdmin):  # noqa
    readonly_fields: tuple = ('datetime_created',
                              'datetime_updated',
                              'datetime_deleted',
                              'is_deleted')
