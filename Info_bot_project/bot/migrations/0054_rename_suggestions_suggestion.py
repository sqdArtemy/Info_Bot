# Generated by Django 4.0.1 on 2022-01-15 04:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0053_suggestions_language_suggestion_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Suggestions',
            new_name='Suggestion',
        ),
    ]
