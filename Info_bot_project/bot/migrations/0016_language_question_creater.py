# Generated by Django 4.0.1 on 2022-01-10 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0015_language_answer_language_answered_question_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='language',
            name='question_creater',
            field=models.TextField(blank=True, verbose_name='Question was succesfully created'),
        ),
    ]