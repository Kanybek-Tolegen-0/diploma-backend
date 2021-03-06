# Generated by Django 4.0.4 on 2022-06-01 19:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=50, unique=True, verbose_name='Никнейм пользователя')),
                ('first_name', models.CharField(max_length=50, verbose_name='Имя пользователя')),
                ('last_name', models.CharField(max_length=50, verbose_name='Фамилия пользователя')),
                ('phone_number', models.CharField(max_length=12, unique=True, verbose_name='Номер телефона')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Cafe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название заведения')),
                ('photo', models.ImageField(default='default_cafe_photo.png', upload_to='')),
                ('address', models.CharField(max_length=200, verbose_name='Адрес заведения')),
            ],
        ),
        migrations.CreateModel(
            name='Cuisine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Название кухни')),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_guest_number', models.SmallIntegerField(verbose_name='Минимальное количество посетителей')),
                ('max_guest_number', models.SmallIntegerField(verbose_name='Максимальное количество посетителей')),
                ('cafe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.cafe', verbose_name='Заведение')),
            ],
        ),
        migrations.CreateModel(
            name='Reserve',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reserve_start_time', models.DateTimeField(verbose_name='Время начала')),
                ('reserve_duration', models.DurationField(verbose_name='Время бронирования')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.place', verbose_name='Место')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
        migrations.CreateModel(
            name='CafePhoneNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=12, unique=True, verbose_name='Номер телефона')),
                ('cafe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.cafe')),
            ],
        ),
        migrations.CreateModel(
            name='CafeCuisine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cafe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.cafe', verbose_name='Заведение')),
                ('cuisine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.cuisine', verbose_name='Кухня')),
            ],
        ),
    ]
