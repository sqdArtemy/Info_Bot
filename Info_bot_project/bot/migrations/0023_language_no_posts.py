# Generated by Django 4.0.1 on 2022-01-11 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0022_language_posts_found_language_reference_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='language',
            name='no_posts',
            field=models.TextField(blank=True, verbose_name='There are no posts'),
        ),
    ]
