from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    """ Custom User Manager """
    def create_user(self, username, first_name, last_name, phone_number, password=None, **kwargs):
        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_super_user(self, username, first_name, last_name, phone_number, password, **kwargs):
        user = self.create_user(
            username,
            first_name,
            last_name,
            phone_number,
            password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """ Custom User Model """
    username = models.CharField(max_length=50, verbose_name='Никнейм пользователя')
    first_name = models.CharField(max_length=50, null=False, verbose_name='Имя пользователя')
    last_name = models.CharField(max_length=50, null=False, verbose_name='Фамилия пользователя')
    phone_number = models.CharField(max_length=12, unique=True, verbose_name='Номер телефона')

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    def __str__(self):
        return f"{self.phone_number}: {self.username}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Cafe(models.Model):
    name = models.CharField(max_length=50, null=False, verbose_name='Название заведения')
    photo = models.ImageField(null=False, default='default_cafe_photo.png')
    address = models.CharField(max_length=200, null=False, verbose_name='Адрес заведения')
    is_full = models.BooleanField(null=False, default=False)

    def __str__(self):
        return f"{self.name}: {self.address}"


class CafePhoneNumber(models.Model):
    phone_number = models.CharField(unique=True, max_length=12, null=False, verbose_name='Номер телефона')
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.cafe.name}: {self.phone_number}"


class Cuisine(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название кухни')

    def __str__(self):
        return f"{self.name}"


class CafeCuisine(models.Model):
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, verbose_name='Заведение')
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE, verbose_name='Кухня')

    def __str__(self):
        return f"{self.cafe.name}: {self.cuisine}"


class Place(models.Model):
    # ??? Why do we need this place model?
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, verbose_name='Заведение')
    min_guest_number = models.SmallIntegerField(verbose_name='Минимальное количество посетителей')
    max_guest_number = models.SmallIntegerField(verbose_name='Максимальное количество посетителей')

    def __str__(self):
        return f"{self.cafe.name}: {self.min_guest_number} - {self.max_guest_number}"


class Reserve(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    place = models.ForeignKey(Place, on_delete=models.CASCADE, verbose_name='Место')
    reserve_start_time = models.DateTimeField(verbose_name='Время начала')
    reserve_duration = models.DurationField(verbose_name='Время бронирования')

    def __str__(self):
        return f"{self.place}: {self.reserve_start_time} for {self.reserve_duration}"
