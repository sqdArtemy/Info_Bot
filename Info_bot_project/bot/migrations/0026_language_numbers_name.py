# Generated by Django 4.0.1 on 2022-01-12 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0025_rename_links_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='language',
            name='numbers_name',
            field=models.TextField(blank=True, verbose_name='There are numbers in name'),
        ),
    ]
