# Generated by Django 4.0.1 on 2022-01-09 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0010_language_language_selection'),
    ]

    operations = [
        migrations.AddField(
            model_name='language',
            name='used_link',
            field=models.TextField(blank=True, verbose_name='Link has been used'),
        ),
    ]
