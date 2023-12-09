from django.contrib import admin
from .models import  Achieve, Product, Course, Role
from .models import LessonType, Lesson, UserLesson, LessonMat, LessonMatSrc, LessonTest
from .models import LessonTestQuestionType, LessonTestQuestion, LessonTestAnswer, LessonTestAnswerSrc
from .models import Forward, ForwardSrc
from .models import CustomUser, UserAchieve



@admin.register(ForwardSrc)
class ForwardSrcAdmin(admin.ModelAdmin):
    list_display = ("id", "forward_id","url")
@admin.register(Forward)
class ForwardAdmin(admin.ModelAdmin):
    list_display = ("id","name","forward_text","creation_datetime")

@admin.register(Achieve)
class AchieveAdmin(admin.ModelAdmin):
    list_display = ("id","name","description","value")

@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id","email", "age","role_id","total_points")

@admin.register(UserAchieve)
class UserAchieveAdmin(admin.ModelAdmin):
    list_display = ("id","user_id","achieve_id")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id","name","price")

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id","name","course_age")


@admin.register(LessonType)
class LessonTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("id","name","lesson_type","course_id","value")

@admin.register(UserLesson)
class UserLessonAdmin(admin.ModelAdmin):
    list_display = ("id","name","lesson_id","user_id","finish")

@admin.register(LessonMat)
class LessonMatAdmin(admin.ModelAdmin):
    list_display = ("id","name","lesson_id")

@admin.register(LessonMatSrc)
class LessonMatAdmin(admin.ModelAdmin):
    list_display = ("id","name","lesson_mat_id")


@admin.register(LessonTest)
class LessonTestAdmin(admin.ModelAdmin):
    list_display = ("id","name","lesson_id")

@admin.register(LessonTestQuestionType)
class LessonTestQuestionTypeAdmin(admin.ModelAdmin):
    list_display = ("id","name")


@admin.register(LessonTestQuestion)
class LessonTestQuestionAdmin(admin.ModelAdmin):
    list_display = ("id","name","lesson_id","lesson_test_question_type_id")

@admin.register(LessonTestAnswer)
class LessonTestAnswerAdmin(admin.ModelAdmin):
    list_display = ("id","lesson_test_question_id","right")

@admin.register(LessonTestAnswerSrc)
class LessonTestAnswerSrcAdmin(admin.ModelAdmin):
    list_display = ("id","lesson_test_answer_id")

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("id","name")

admin.site.site_header = 'Админка'