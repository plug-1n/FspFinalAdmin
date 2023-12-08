from django.contrib import admin
from .models import Forward, ForwardSrc, Achieve, User, UserAchieve, Product, Course, LessonType, Lesson, UserLesson

@admin.register(ForwardSrc)
class ForwardSrcAdmin(admin.ModelAdmin):
    list_display = ("id", "forward_id","url")
@admin.register(Forward)
class ForwardAdmin(admin.ModelAdmin):
    list_display = ("id","name","forward_text","creation_datetime")

@admin.register(Achieve)
class AchieveAdmin(admin.ModelAdmin):
    list_display = ("id","name","description","value")

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id","email", "is_staff")

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
class LessonAdmin(admin.ModelAdmin):
    list_display = ("id","name","lesson_id","user_id","finish")

admin.site.site_header = 'Админка'