from django.contrib import admin
from .models import Forward
@admin.register(Forward)
class MusicianAdmin(admin.ModelAdmin):
    list_display = ("id","name","forward_text","creation_datetime")

admin.site.site_header = 'Админка'