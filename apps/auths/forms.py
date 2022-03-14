
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
)

from auths.models import CustomUser


class CustomCreationForm(UserCreationForm):  # noqa

    class Meta:  # noqa
        model = CustomUser
        fields = (
            'email',
        )


class CustomUserChangeForm(UserChangeForm):  # noqa

    class Meta:  # noqa
        model = CustomUser
        fields: tuple = (
            'email',
        )
