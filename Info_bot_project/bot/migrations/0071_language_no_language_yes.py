# Generated by Django 4.0.1 on 2022-01-15 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0070_remove_language_no_remove_language_yes_language_no_q_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='language',
            name='no',
            field=models.CharField(blank=True, max_length=256, verbose_name='no'),
        ),
        migrations.AddField(
            model_name='language',
            name='yes',
            field=models.CharField(blank=True, max_length=256, verbose_name='yes'),
        ),
    ]