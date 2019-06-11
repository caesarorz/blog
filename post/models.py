from tinymce import HTMLField
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

import os
import random
import string
import datetime
from django.utils.text import slugify
from io import BytesIO
from django.utils import timezone
from django.utils.text import slugify
from django.conf import settings
from django.core.files.storage import FileSystemStorage

User = get_user_model()


def unique_slug_generator(instance, new_slug=None):
	"""

	"""

	if new_slug is not None:
		slug = new_slug
	else:
		slug = slugify(instance.title)

	Klass = instance.__class__
	qs_exists = Klass.objects.filter(slug=slug).exists()
	if qs_exists:
		new_slug = "{slug}-{randstr}".format(
					slug=slug,
					randstr=random_string_generator(size=4)
				)

		return unique_slug_generator(instance, new_slug=new_slug)
	return slug

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField()

    def __str__(self):
        return self.user.username



def random_string_generator(size=10,chars=string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))


def upload_file_loc(instance, filename):
    folder_loc = random_string_generator()
    if instance:
        location = "documents/{}_{}/".format(instance.title, folder_loc)
    return location + filename

def get_filename(path):
    return os.path.basename(path)


class Category(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(blank=True, unique=True)
    content = HTMLField()
    comment_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail = models.ImageField()
    categories = models.ManyToManyField(Category)
    featured = models.BooleanField()
    previous_post = models.ForeignKey(
        'self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey(
        'self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"id": self.id})

    # def get_absolute_url(self):
    #     # return "/products/{pk}/".format(pk=self.pk)
    #     return reverse("products:product_detail", kwargs={"slug": self.slug})

    def get_update_url(self):
        return reverse("post-update")

    def get_delete_url(self):
        return reverse("post-delete", kwargs={"id": self.id})

    @property
    def get_comments(self):
        return self.comments.all().order_by("-timestamp")


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    post = models.ForeignKey(
        Post, related_name="comments", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


from blog.aws.download.utils import AWSDownload
from blog.aws.utils import ProtectedS3Storage

class Document(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(blank=True, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    file = models.FileField(
        upload_to=upload_file_loc, storage= ProtectedS3Storage())
        #FileSystemStorage(location=settings.PROTECTED_ROOT))

    def __str__(self):
        return self.title

    def generate_download_url(self):
        bucket = getattr(settings, "AWS_STORAGE_BUCKET_NAME")
        region = getattr(settings, "S3DIRECT_REGION")
        access_key = getattr(settings, "AWS_ACCESS_KEY_ID")
        secret_key = getattr(settings, "AWS_SECRET_ACCESS_KEY")
        PROTECTED_DIR_NAME = getattr(settings, "PROTECTED_DIR_NAME", "protected")
        path = '{base}/{filepath}'.format(base=PROTECTED_DIR_NAME, filepath=str(self.file))
        print(path)
        aws_dl_object =  AWSDownload(access_key, secret_key, bucket, region)
        file_url = aws_dl_object.generate_url(path)#, new_filename='New awesome file')
        return file_url

    def get_download(self):
        qs = self.documentdownload_set.all()
        print("get_download ", qs)
        return qs    

    def get_download_url(self):
        return reverse("download", kwargs={"id": self.id})

    @property
    def name(self):
        return get_filename(self.file.name)


# class DocumentDownload(models.Model):
#     title = models.CharField(max_length=100)
#     document = models.ForeignKey(Document, on_delete=models.CASCADE)
#     file = models.FileField(
#         upload_to=upload_file_loc, 
#         storage=FileSystemStorage(location=settings.PROTECTED_ROOT))


#     def __str__(self):
#         return str(self.file.name)

#     def get_download_url(self):
#         return reverse("download", kwargs={"id": self.id})

#     @property
#     def name(self):
#         return get_filename(self.file.name)