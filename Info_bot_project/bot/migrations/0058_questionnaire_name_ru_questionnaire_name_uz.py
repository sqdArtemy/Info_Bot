# Generated by Django 4.0.1 on 2022-01-15 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0057_alter_answer_text_alter_answer_text_ru_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionnaire',
            name='name_ru',
            field=models.CharField(max_length=256, null=True, unique=True, verbose_name='Name of the questionnaire'),
        ),
        migrations.AddField(
            model_name='questionnaire',
            name='name_uz',
            field=models.CharField(max_length=256, null=True, unique=True, verbose_name='Name of the questionnaire'),
        ),
    ]
