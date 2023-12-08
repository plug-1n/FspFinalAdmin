from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager

from ckeditor_uploader.fields import RichTextUploadingField


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    email = models.EmailField(null=False, unique=True, verbose_name='Почта')
    phone = models.CharField(max_length=20, null=False,
                             unique=True, verbose_name="Номер телефона")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()


class Forward(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    forward_text = RichTextUploadingField(verbose_name="Описание")
    creation_datetime = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")


    class Meta:
        verbose_name = "Угроза"
        verbose_name_plural = "Угрозы"

    def __str__(self):
        return f"{self.name}"

class ForwardSrc(models.Model):
    forward_id = models.ForeignKey(Forward, on_delete=models.CASCADE,verbose_name="Название атаки")
    url = models.CharField(max_length=255, verbose_name="Ссылка")

    class Meta:
        verbose_name = "Угроза->статика"
        verbose_name_plural = "Угроза->статика"
    def __str__(self):
        return f"{self.forward_id}"

class Achieve(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")
    description = RichTextUploadingField(verbose_name="Описание")
    value = models.IntegerField(blank=True,null=True, verbose_name="Очки",validators=[
            MinValueValidator(0, message="Значение должно быть больше нуля или равнятся нулю"),
        ])
    
    class Meta:
        verbose_name = "Достижение"
        verbose_name_plural = "Достижения"
    

    def __str__(self):
        return f"{self.name}"
    
class UserAchieve(models.Model):
    achieve_id = models.ForeignKey(Achieve, verbose_name="Достижение", on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Юзер-Достижение"
        verbose_name_plural = "Юзер-Достижение"

    def __str__(self):
        return f"{self.achieve_id}"