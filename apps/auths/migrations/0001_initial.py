# Generated by Django 3.0 on 2022-03-14 14:50

import auths.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('name', models.CharField(max_length=150, verbose_name='Имя')),
                ('surname', models.CharField(max_length=150, verbose_name='Фамилия')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='E-mail/username')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Доступ к админке')),
                ('is_active', models.BooleanField(default=True, verbose_name='Рабочий')),
                ('datetime_joined', models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')),
                ('date_birth', models.DateField(validators=[auths.models.adult_validation], verbose_name='Дата рождения (ГГГГ-ММ-ДД)')),
                ('photo', models.ImageField(blank=True, upload_to='custom_user/photos/%Y/%m/%d/', verbose_name='Фотография')),
                ('datetime_updated', models.DateTimeField(auto_now=True, verbose_name='Время обновления')),
                ('datetime_deleted', models.DateTimeField(blank=True, null=True, verbose_name='Время удаления')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Удален')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Кастомный пользователь',
                'verbose_name_plural': 'Кастомные пользователь',
                'ordering': ('datetime_joined',),
            },
        ),
    ]
