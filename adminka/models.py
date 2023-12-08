from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class Forward(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    forward_text = RichTextUploadingField(verbose_name="Описание")
    creation_datetime = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")


    class Meta:
        verbose_name = "Угроза"
        verbose_name_plural = "Угрозы"

    def __str__(self):
        return f"{self.name}"
