from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager

from ckeditor_uploader.fields import RichTextUploadingField


class Role(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")

    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"

        managed = False
        db_table = "role"
    
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
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name="Роль", db_column="role_id")
    password_hash = models.CharField(max_length=255,verbose_name="Хэш пароля")
    age = models.IntegerField(verbose_name="Возраст", validators=[
        MinValueValidator(6, "Возраст должнен быть от 6 до 100"),
        MaxValueValidator(100, "Возраст должнен быть от 6 до 100")
    ])
    refresh = models.CharField(max_length=100, verbose_name="Рефреш")
    total_points = models.IntegerField(verbose_name="Общее кол-во очков")
    final_exam_current = models.IntegerField(verbose_name="Текущий бал за тест")
    final_exam_max = models.IntegerField(verbose_name="Лучшее решение теста") 
    expired_at = models.DateTimeField(blank=True, null=True,verbose_name="Срок годности токена")
    registration_datetime = models.DateTimeField(auto_now=True, verbose_name="Дата регистрации")

    class Meta:
        verbose_name = "Юзер"
        verbose_name_plural = "Юзеры"

        managed = False
        db_table = "user"
    
    def __str__(self):
        return f"{self.email}"
class Forward(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    forward_text = RichTextUploadingField(verbose_name="Описание")
    creation_datetime = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")


    class Meta:
        verbose_name = "Вид угрозы"
        verbose_name_plural = "Виды угроз"

        managed = False
        db_table = "forward"

    def __str__(self):
        return f"{self.name}"

class ForwardSrc(models.Model):
    forward_id = models.ForeignKey(Forward, on_delete=models.CASCADE,verbose_name="Название атаки", db_column="forward_id")
    url = models.CharField(max_length=255, verbose_name="Ссылка")

    class Meta:
        verbose_name = "Угроза -> media"
        verbose_name_plural = "Угроза -> media"

        managed = False
        db_table = "forward_src"

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

        managed = False
        db_table = "achive"
    

    def __str__(self):
        return f"{self.name}"
    
class UserAchieve(models.Model):
    achieve_id = models.ForeignKey(Achieve, verbose_name="Достижение", on_delete=models.CASCADE,db_column="achive_id")
    user_id = models.ForeignKey(CustomUser, verbose_name="Пользователь", on_delete=models.CASCADE, db_column="user_id")

    class Meta:
        verbose_name = "Юзер-Достижение"
        verbose_name_plural = "Юзер-Достижение"

        managed = False
        db_table = "user_achive"

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

        managed = False
        db_table = "product"

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

        managed = False
        db_table = "course"
    
    def __str__(self):
        return f"{self.name}"

class LessonType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")

    class Meta:
        verbose_name = "Тип урока"
        verbose_name_plural = "Типы уроков"

        managed = False
        db_table = "lesson_type"
    
    def __str__(self):
        return f"{self.name}"
    
class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    lesson_type = models.ForeignKey(LessonType,verbose_name="Тип урока",on_delete=models.CASCADE, db_column="lesson_type")
    course_id = models.ForeignKey(Course, verbose_name="Курс", on_delete=models.CASCADE, db_column="course_id")
    value = models.IntegerField(verbose_name="Кол-во поинтов за курс", validators=[
        MinValueValidator(0,message="Значение должно быть больше или равно 0")
    ])

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

        managed = False
        db_table = "lesson"
    
    def __str__(self):
        return f"{self.name}"

class UserLesson(models.Model):
    lesson_id = models.ForeignKey(Lesson,verbose_name="Урок",on_delete=models.CASCADE, db_column="lesson_id")
    user_id = models.ForeignKey(CustomUser, verbose_name="Юзер", on_delete=models.CASCADE, db_column="user_id")
    finish = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Юзер-Урок"
        verbose_name_plural = "Юзер-Урок"

        managed = False
        db_table = "user_lesson"
    
    def __str__(self):
        return f"{self.lesson_id} - {self.user_id}"

class LessonMat(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    lesson_id = models.ForeignKey(Lesson,verbose_name="Урок",on_delete=models.CASCADE, db_column="lesson_id")
    lesson_text = RichTextUploadingField(null=True, verbose_name="Текст")

    class Meta:
        verbose_name = "Урок -> material"
        verbose_name_plural = "Урок -> material"

        managed = False
        db_table = "lesson_mat"
    
    def __str__(self):
        return f"{self.name}"

class LessonMatSrc(models.Model):
    lesson_mat_id = models.ForeignKey(LessonMat,verbose_name="Материал урока",on_delete=models.CASCADE, db_column="lesson_mat_id")
    url = models.CharField(max_length=255, verbose_name="S3 картинка")

    class Meta:
        verbose_name = "Урок -> media"
        verbose_name_plural = "Урок -> media"

        managed = False
        db_table = "lesson_mat_src"
    
    def __str__(self):
        return f"{self.lesson_mat_id}"
    
class LessonTest(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    lesson_id = models.ForeignKey(Lesson,verbose_name="Урок",on_delete=models.CASCADE, db_column="lesson_id")
    lesson_text = RichTextUploadingField(null=True, verbose_name="Текст")

    class Meta:
        verbose_name = "Урок -> test"
        verbose_name_plural = "Урок -> test"

        managed = False
        db_table = "lesson_test"
    
    def __str__(self):
        return f"{self.name}"

class LessonTestQuestionType(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")

    class Meta:
        verbose_name = "Вид вопроса"
        verbose_name_plural = "Виды вопросов"

        managed = False
        db_table = "lesson_test_question_type"
    
    def __str__(self):
        return f"{self.name}"

class LessonTestQuestion(models.Model):
    question = models.CharField(max_length=255, verbose_name="Вопрос")
    url = models.CharField(max_length=255, verbose_name="S3 картинка")
    lesson_id = models.ForeignKey(Lesson,on_delete=models.CASCADE, verbose_name="Задание", db_column="lesson_id")
    lesson_test_question_type_id = models.ForeignKey(LessonTestQuestionType, on_delete=models.CASCADE, verbose_name="Тип задания",
    db_column="lesson_test_question_type_id")

    class Meta:
        verbose_name = "Тест -> question"
        verbose_name_plural = "Тест -> question"

        managed = False
        db_table = "lesson_test_question"
    
    def __str__(self):
        return f"{self.question}"

class LessonTestAnswer(models.Model):
    answer_text = RichTextUploadingField(verbose_name="Текст ответа")
    lesson_test_question_id = models.ForeignKey(LessonTestQuestion,on_delete=models.CASCADE, verbose_name="Вопрос",
    db_column="lesson_test_question_id")
    correct = models.BooleanField()

    class Meta:
        verbose_name = "Тест -> answer"
        verbose_name_plural = "Тест -> answer"

        managed = False
        db_table = "lesson_test_answer"
    
    def __str__(self):
        return f"{self.lesson_test_question_id}"

class LessonTestAnswerSrc(models.Model):
    lesson_test_answer_id = models.ForeignKey(LessonTestAnswer,on_delete=models.CASCADE,verbose_name="Ответ вопроса",
    db_column="lesson_test_answer_id")
    url = models.CharField(max_length=255, verbose_name="S3 картинка")

    class Meta:
        verbose_name = "Ответ -> media"
        verbose_name_plural = "Ответ -> media"

        managed = False
        db_table = "lesson_test_answer_src"
    
    def __str__(self):
        return f"{self.lesson_test_answer_id}"

class News(models.Model):
    title = models.CharField(max_length=50,verbose_name="Заголовок")
    news_text = RichTextUploadingField()
    creation_datetime = models.DateTimeField(auto_now=True, verbose_name="Дата создания")
    url_image = models.CharField(max_length=255)
    url_video = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

        managed = False
        db_table = "news"
    
    def __str__(self):
        return f"{self.title}"
    
class FinalTest(models.Model):
    test_description = RichTextUploadingField(verbose_name="Описание")

    class Meta:
        verbose_name = "Финальный тест"
        verbose_name_plural = "Финальный тест"

        managed = False
        db_table = "final_test"

    def __str__(self):
        return f"{self.test_description}"

class UserFinal(models.Model):
    final_test_id = models.ForeignKey(FinalTest, on_delete=models.CASCADE, db_column="final_test_id", verbose_name="Тест")
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, db_column="user_id", verbose_name="Пользователь")
    max_result = models.IntegerField(verbose_name="Максимальный результат", validators=[
        MinValueValidator(0,message="Значение должно быть больше или равно 0")
    ])
    last_result = models.IntegerField(verbose_name="Последний резульатт", validators=[
        MinValueValidator(0,message="Значение должно быть больше или равно 0")
    ])

    class Meta:
        verbose_name = "Юзер -> финал"
        verbose_name_plural = "Юзер -> финал"

        managed = False
        db_table = "user_final"
    
    def __str__(self):
        return f"{self.final_test_id} - {self.user_id}"
    
class FinalTestQuestionDirection(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")

    class Meta:
        verbose_name = "Финал -> direction"
        verbose_name_plural = "Финал -> direction"

        managed = False
        db_table = "final_test_question_direction"
    
    def __str__(self):
        return f"{self.name}"


class FinalTestQuestion(models.Model):
    final_test_question_direction_id = models.ForeignKey(FinalTestQuestionDirection,
                                                        on_delete=models.CASCADE,
                                                        db_column="final_test_question_direction_id",
                                                        verbose_name="Финал -> direction")
    url = models.CharField(max_length=255,verbose_name="S3 картинка")
    question = models.CharField(max_length=255,verbose_name="Вопрос")
    class Meta:
        verbose_name = "Финал -> question"
        verbose_name_plural = "Финал -> question"

        managed = False
        db_table = "final_test_question"
    
    def __str__(self):
        return f"{self.question}"

class FinalTestAnswer(models.Model):
    answer_text = RichTextUploadingField(verbose_name="Текст ответа")
    url = models.CharField(max_length=255,verbose_name="S3 картинка")
    final_test_question_id = models.ForeignKey(FinalTestQuestion,
                                               on_delete=models.CASCADE,
                                               db_column="final_test_question_id",
                                               verbose_name="Финал -> question")   
    class Meta:
        verbose_name = "Финал -> answer"
        verbose_name_plural = "Финал -> answer"
        managed = False
        db_table = "final_test_answer"