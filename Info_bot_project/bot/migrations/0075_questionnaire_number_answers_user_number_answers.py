# Generated by Django 4.0.1 on 2022-01-29 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0074_remove_questionnaire_number_answers'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionnaire',
            name='number_answers',
            field=models.CharField(default=5, max_length=256, verbose_name='Number of answers'),
        ),
    ]