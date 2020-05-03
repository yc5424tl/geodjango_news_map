from storages.backends.s3boto3 import S3Boto3Storage
#from django.conf import settings

class MediaStorage(S3Boto3Storage):

  #  bucket_name = "mtn-bucket"
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False


class StaticStorage(S3Boto3Storage):

 #   bucket_name = "mtn-assets-resource"
    location = 'static'
    default_acl = 'public-read'

# from storages.backends.s3boto3 import S3Boto3Storage
#
# class S3MediaStorage(S3Boto3Storage):
#     location = 'media'
#     file_overwrite = False
#
#
# class S3StaticStorage(S3Boto3Storage):
#     location = "static"