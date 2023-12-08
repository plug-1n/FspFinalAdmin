from django.contrib import admin
from .models import Forward, ForwardSrc, Achieve

@admin.register(ForwardSrc)
class ForwardSrcAdmin(admin.ModelAdmin):
    list_display = ("id", "forward_id","url")
@admin.register(Forward)
class ForwardAdmin(admin.ModelAdmin):
    list_display = ("id","name","forward_text","creation_datetime")

@admin.register(Achieve)
class AchieveAdmin(admin.ModelAdmin):
    list_display = ("id","name","description","value")

admin.site.site_header = 'Админка'