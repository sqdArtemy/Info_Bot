# Generated by Django 4.0.1 on 2022-01-08 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0004_rename_category_name_category_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='language',
            name='send_contact',
            field=models.TextField(blank=True, verbose_name='"Send contact" button'),
        ),
    ]
