# Generated by Django 4.0.1 on 2022-01-14 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0051_alter_keyword_word'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='topic',
            field=models.CharField(max_length=256, verbose_name='Publication`s topic'),
        ),
    ]
