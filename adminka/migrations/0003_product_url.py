# Generated by Django 5.0 on 2023-12-08 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminka', '0002_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='url',
            field=models.CharField(default=1, max_length=255, verbose_name='S3 картинка'),
            preserve_default=False,
        ),
    ]
