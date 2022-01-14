# Generated by Django 4.0.1 on 2022-01-12 09:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0028_alter_publication_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='bot.category'),
        ),
        migrations.AlterField(
            model_name='publication',
            name='language',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='bot.language'),
        ),
    ]