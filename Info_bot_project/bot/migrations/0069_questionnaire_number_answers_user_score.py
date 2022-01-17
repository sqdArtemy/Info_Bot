# Generated by Django 4.0.1 on 2022-01-15 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0068_alter_language_incorrect_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionnaire',
            name='number_answers',
            field=models.PositiveIntegerField(default=5, verbose_name='Number of questions'),
        ),
        migrations.AddField(
            model_name='user',
            name='score',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Overall score for poll'),
        ),
    ]
