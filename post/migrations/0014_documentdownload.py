# Generated by Django 2.2.1 on 2019-06-06 23:36

import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion
import post.models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0013_remove_document_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentDownload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(storage=django.core.files.storage.FileSystemStorage(location='/home/caesar/django/learning/justdjango/blog/protected_media'), upload_to=post.models.upload_file_loc)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.Document')),
            ],
        ),
    ]