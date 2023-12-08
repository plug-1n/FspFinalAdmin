from django.contrib import admin
from .models import Forward, ForwardSrc, Achieve, User, UserAchieve

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

admin.site.site_header = 'Админка'