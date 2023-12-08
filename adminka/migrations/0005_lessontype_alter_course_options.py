# Generated by Django 5.0 on 2023-12-08 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminka', '0004_course'),
    ]

    operations = [
        migrations.CreateModel(
            name='LessonType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Тип урока',
                'verbose_name_plural': 'Тип уроков',
            },
        ),
        migrations.AlterModelOptions(
            name='course',
            options={'verbose_name': 'Курс', 'verbose_name_plural': 'Курсы'},
        ),
    ]