# Generated by Django 4.0.1 on 2022-01-29 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0075_questionnaire_number_answers_user_number_answers'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='number_answers',
            field=models.PositiveIntegerField(blank=True, default=0, verbose_name='Number of question'),
        ),
    ]
