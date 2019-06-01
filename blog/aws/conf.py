#https://django-storages.readthedocs.io/en/latest/

import datetime
import os

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "AKIA573FFIJDUS32WNI3")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "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")
AWS_USERNAME = "landing"
AWS_GROUP_NAME = "landing-group"

AWS_FILE_EXPIRE = 200
AWS_PRELOAD_METADATA = True
AWS_QUERYSTRING_AUTH = False
# AWS_QUERYSTRING_AUTH = True


DEFAULT_FILE_STORAGE = 'blog.aws.utils.MediaRootS3BotoStorage'
STATICFILES_STORAGE = 'blog.aws.utils.StaticRootS3BotoStorage'
AWS_STORAGE_BUCKET_NAME = 'landing-page-bucket01'
S3DIRECT_REGION = 'us-west-2'
S3_URL = '//%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
MEDIA_URL = '//%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME
MEDIA_ROOT = MEDIA_URL
STATIC_URL = S3_URL + 'static/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

two_months = datetime.timedelta(days=61)
date_two_months_later = datetime.date.today() + two_months
expires = date_two_months_later.strftime("%A, %d %B %Y 20:00:00 GMT")

AWS_HEADERS = {
    'Expires': expires,
    'Cache-Control': 'max-age=%d' % (int(two_months.total_seconds()), ),
}
