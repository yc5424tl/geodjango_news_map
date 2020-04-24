
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION
    file_overwrite = False

class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION

# from storages.backends.s3boto3 import S3Boto3Storage
#
# class S3MediaStorage(S3Boto3Storage):
#     location = 'mediafiles'
#     file_overwrite = False
#
#
# class S3StaticStorage(S3Boto3Storage):
#     location = "static"
