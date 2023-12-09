from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager

from ckeditor_uploader.fields import RichTextUploadingField


class Role(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")

    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"
    
    def __str__(self):
        return f"{self.name}"

# class UserManager(BaseUserManager):
#     def _create_user(self, email, password, **extra_fields):
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email=None, password=None, **extra_fields):
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_superuser", True)

#         if extra_fields.get("is_staff") is not True:
#             raise ValueError("Superuser must have is_staff=True.")
#         if extra_fields.get("is_superuser") is not True:
#             raise ValueError("Superuser must have is_superuser=True.")

#         return self._create_user(email, password, **extra_fields)

#     def create_user(self, email=None, password=None, **extra_fields):
#         extra_fields.setdefault("is_staff", False)
#         extra_fields.setdefault("is_superuser", False)
#         return self._create_user(email, password, **extra_fields)


# class User(AbstractUser):
#     username = None

#     email = models.EmailField(null=False, unique=True, verbose_name='Почта')


#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []
#     objects = UserManager()

class CustomUser(models.Model):
    email = models.EmailField(max_length=250,verbose_name="Почта")
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name="Роль")
    password_hash = models.CharField(max_length=255,verbose_name="Хэш пароля")
    age = models.IntegerField(verbose_name="Возраст", validators=[
        MinValueValidator(6, "Возраст должнен быть от 6 до 100"),
        MaxValueValidator(100, "Возраст должнен быть от 6 до 100")
    ])
    refresh = models.CharField(max_length=100, verbose_name="Рефреш")
    total_points = models.IntegerField(verbose_name="Общее кол-во очков")
    final_exam_current = models.IntegerField(verbose_name="Текущий бал за тест")
    final_exam_max = models.IntegerField(verbose_name="Лучшее решение теста") 
    expired_at = models.DateTimeField(blank=True, null=True)
    registration_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользовталели"
class Forward(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    forward_text = RichTextUploadingField(verbose_name="Описание")
    creation_datetime = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")


    class Meta:
        verbose_name = "Вид угрозы"
        verbose_name_plural = "Виды угроз"

    def __str__(self):
        return f"{self.name}"

class ForwardSrc(models.Model):
    forward_id = models.ForeignKey(Forward, on_delete=models.CASCADE,verbose_name="Название атаки")
    url = models.CharField(max_length=255, verbose_name="Ссылка")

    class Meta:
        verbose_name = "Угроза -> media"
        verbose_name_plural = "Угроза -> media"
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
    user_id = models.ForeignKey(CustomUser, verbose_name="Пользователь", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Юзер-Достижение"
        verbose_name_plural = "Юзер-Достижение"

    def __str__(self):
        return f"{self.achieve_id}"
    
class Product(models.Model):
    name = models.CharField(max_length=50,verbose_name="Название")
    description = RichTextUploadingField(verbose_name="Описание")
    price = models.IntegerField(verbose_name="Цена",validators=[
        MinValueValidator(0,"Цена не может быть отрицательной")
    ])
    url = models.CharField(max_length=255,verbose_name="S3 картинка")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.name}"

class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = RichTextUploadingField(verbose_name="Описание")
    # course_age у нас в качестве уровня сложности
    course_age = models.IntegerField(verbose_name="Сложность [0;2]", validators=[
        MinValueValidator(0,message="Диапозон должен быть в диапозоне от 0 до 2"),
        MaxValueValidator(2,message="Диапозон должен быть в диапозоне от 0 до 2"),
    ])
    url = models.CharField(max_length=255, verbose_name="S3 картинка")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
    
    def __str__(self):
        return f"{self.name}"

class LessonType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")

    class Meta:
        verbose_name = "Тип урока"
        verbose_name_plural = "Типы уроков"
    
    def __str__(self):
        return f"{self.name}"
    
class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    lesson_type = models.ForeignKey(LessonType,verbose_name="Тип урока",on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, verbose_name="Курс", on_delete=models.CASCADE)
    value = models.IntegerField(verbose_name="Кол-во поинтов за курс", validators=[
        MinValueValidator(0,message="Значение должно быть больше или равно 0")
    ])

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
    
    def __str__(self):
        return f"{self.name}"

class UserLesson(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    lesson_id = models.ForeignKey(Lesson,verbose_name="Урок",on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomUser, verbose_name="Юзер", on_delete=models.CASCADE)
    finish = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Юзер-Урок"
        verbose_name_plural = "Юзер-Урок"
    
    def __str__(self):
        return f"{self.name}"

class LessonMat(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    lesson_id = models.ForeignKey(Lesson,verbose_name="Урок",on_delete=models.CASCADE)
    lesson_text = RichTextUploadingField(null=True, verbose_name="Текст")

    class Meta:
        verbose_name = "Урок -> material"
        verbose_name_plural = "Урок -> material"
    
    def __str__(self):
        return f"{self.name}"

class LessonMatSrc(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    lesson_mat_id = models.ForeignKey(LessonMat,verbose_name="Материал урока",on_delete=models.CASCADE)
    url = models.CharField(max_length=255, verbose_name="S3 картинка")

    class Meta:
        verbose_name = "Урок -> media"
        verbose_name_plural = "Урок -> media"
    
    def __str__(self):
        return f"{self.name}"
    
class LessonTest(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    lesson_id = models.ForeignKey(Lesson,verbose_name="Урок",on_delete=models.CASCADE)
    lesson_text = RichTextUploadingField(null=True, verbose_name="Текст")

    class Meta:
        verbose_name = "Урок -> test"
        verbose_name_plural = "Урок -> test"
    
    def __str__(self):
        return f"{self.name}"

class LessonTestQuestionType(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")

    class Meta:
        verbose_name = "Вид вопроса"
        verbose_name_plural = "Виды вопросов"
    
    def __str__(self):
        return f"{self.name}"

class LessonTestQuestion(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    lesson_id = models.ForeignKey(Lesson,on_delete=models.CASCADE, verbose_name="Задание")
    lesson_test_question_type_id = models.ForeignKey(LessonTestQuestionType, on_delete=models.CASCADE, verbose_name="Тип задания")

    class Meta:
        verbose_name = "Тест -> question"
        verbose_name_plural = "Тест -> question"
    
    def __str__(self):
        return f"{self.name}"

class LessonTestAnswer(models.Model):
    answer_text = RichTextUploadingField(verbose_name="Текст ответа")
    lesson_test_question_id = models.ForeignKey(LessonTestQuestion,on_delete=models.CASCADE, verbose_name="Вопрос")
    right = models.BooleanField()

    class Meta:
        verbose_name = "Тест -> answer"
        verbose_name_plural = "Тест -> answer"
    
    def __str__(self):
        return f"{self.name}"

class LessonTestAnswerSrc(models.Model):
    lesson_test_answer_id = models.ForeignKey(LessonTestAnswer,on_delete=models.CASCADE,verbose_name="Ответ вопроса")
    url = models.CharField(max_length=255, verbose_name="S3 картинка")

    class Meta:
        verbose_name = "Ответ -> media"
        verbose_name_plural = "Ответ -> media"
    
    def __str__(self):
        return f"{self.lesson_test_answer_id}"