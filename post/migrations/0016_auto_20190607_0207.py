# Generated by Django 2.2.1 on 2019-06-07 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0015_documentdownload_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
