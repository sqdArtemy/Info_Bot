# Generated by Django 4.0.1 on 2022-01-15 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0063_language_female_language_male_question_user_age_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='user_age',
            field=models.PositiveIntegerField(verbose_name='User`s age'),
        ),
        migrations.AlterField(
            model_name='question',
            name='user_gender',
            field=models.CharField(max_length=256, verbose_name='User`s gender'),
        ),
        migrations.AlterField(
            model_name='question',
            name='user_height',
            field=models.CharField(max_length=256, verbose_name='User`s height'),
        ),
        migrations.AlterField(
            model_name='question',
            name='user_mariage',
            field=models.CharField(max_length=256, verbose_name='User`s marriage status'),
        ),
        migrations.AlterField(
            model_name='question',
            name='user_weight',
            field=models.CharField(max_length=256, verbose_name='User`s weight'),
        ),
    ]
