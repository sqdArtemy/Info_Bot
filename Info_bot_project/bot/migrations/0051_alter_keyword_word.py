# Generated by Django 4.0.1 on 2022-01-14 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0050_alter_answer_text_alter_answer_text_ru_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyword',
            name='word',
            field=models.CharField(max_length=256, verbose_name='Keyword'),
        ),
    ]
