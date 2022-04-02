from datetime import (
    datetime,
    date,
)

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError


def adult_validation(age: date) -> None:  # noqa
    ADULT_AGE = 18
    today: date = date.today()
    cur_age: int = today.year - age.year - (
        (today.month, today.day) < (age.month, age.day)
        )
    if cur_age < ADULT_AGE:
        raise ValidationError(
            "Ваш возраст не может быть меньше 18 лет (функция валидатор)",
            code='adult_age_error'
        )


def email_lower_case_validation(email: str) -> None:  # noqa
    if(any(letter.isupper() for letter in email)):
        raise ValidationError(
            "Почта не может иметь ни один символ в верхнем регистре",
            code='lower_case_email_error'
        )


class CustomUserManager(BaseUserManager):  # noqa

    def _create_user(
        self,
        email: str,
        password: str,
        name: str,
        surname: str,
        date_birth: str,
        **extra_fields: dict
    ) -> 'CustomUser':
        if not email:
            raise ValidationError('Email must be filled')

        user: 'CustomUser' = self.model(
            email=self.normalize_email(email),
            password=password,
            name=name,
            surname=surname,
            # date_birth=(datetime.strptime(date_birth, "%Y-%m-%d").date()),
            date_birth=date_birth,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self,
        email: str,
        password: str,
        name: str = '',
        surname: str = '',
        date_birth: str = '2001-01-31',
        **extra_fields: dict
    ) -> 'CustomUser':  # noqa
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, name,
                                 surname, date_birth, **extra_fields)

    def create_superuser(
        self,
        email: str,
        password: str,
        name: str = '',
        surname: str = '',
        date_birth: str = '2001-01-31',
        **extra_fields: dict
    ) -> 'CustomUser':  # noqa
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, name, surname,
                                 date_birth, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):  # noqa
    ADULT_AGE = 18
    name = models.CharField(
        max_length=150,
        verbose_name='Имя'
    )
    surname = models.CharField(
        max_length=150,
        verbose_name='Фамилия'
    )
    email = models.EmailField(
        unique=True,
        verbose_name='E-mail/username',
        validators=[email_lower_case_validation]
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='Доступ к админке'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Рабочий'
    )
    datetime_joined = models.DateTimeField(
        verbose_name='Дата регистрации',
        auto_now_add=True
    )
    date_birth = models.DateField(
        verbose_name='Дата рождения (ГГГГ-ММ-ДД)',
        validators=[adult_validation]
    )
    photo = models.ImageField(
        upload_to='custom_user/photos/%Y/%m/%d/',
        blank=True,
        verbose_name='Фотография'
    )
    datetime_updated = models.DateTimeField(
        verbose_name="Время обновления",
        auto_now=True
    )
    datetime_deleted = models.DateTimeField(
        verbose_name="Время удаления",
        null=True,
        blank=True
    )
    is_deleted = models.BooleanField(
        default=False,
        verbose_name='Удален'
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname', 'date_birth']

    objects = CustomUserManager()

    class Meta:  # noqa
        verbose_name = 'Кастомный пользователь'
        verbose_name_plural = 'Кастомные пользователь'
        ordering = (
            'datetime_joined',
        )

    def __str__(self) -> str:  # noqa
        return 'Кастомный пользователь: {}. Добавлен {}'.format(
            self.email,
            self.datetime_joined
        )

    def save(self, *args, **kwargs) -> None:  # noqa
        def calculate_age(born) -> int:
            today: date = date.today()
            return today.year - born.year - (
                (today.month, today.day) < (born.month, born.day)
                )

        if self.email != self.email.lower():
            raise ValidationError(
                'Ваш email "%(email)s" должен быть в нижнем регистре',
                code='lower_case_email_error',
                params={'email': self.email}
            )
        if calculate_age(self.date_birth) < self.ADULT_AGE:
            raise ValidationError(
                'Ваш возраст должен быть не менее 18 лет (из фун-ии save)',
                code='adult_age_error'
            )
        super().save(*args, **kwargs)

    def delete(self) -> None:  # noqa
        self.datetime_deleted = datetime.now()
        self.is_deleted = True
        self.save(
            update_fields=['datetime_deleted', 'is_deleted']
        )
