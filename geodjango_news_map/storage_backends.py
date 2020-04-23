from abc import ABC

from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage, ABC):
    location = 'static/mediafiles'
    file_overwrite = False

# from storages.backends.s3boto3 import S3Boto3Storage
#
# class S3MediaStorage(S3Boto3Storage):
#     location = 'mediafiles'
#     file_overwrite = False
#
#
# class S3StaticStorage(S3Boto3Storage):
#     location = "static"
