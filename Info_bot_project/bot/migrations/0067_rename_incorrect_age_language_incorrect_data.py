# Generated by Django 4.0.1 on 2022-01-15 09:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0066_language_incorrect_age'),
    ]

    operations = [
        migrations.RenameField(
            model_name='language',
            old_name='incorrect_age',
            new_name='incorrect_data',
        ),
    ]
