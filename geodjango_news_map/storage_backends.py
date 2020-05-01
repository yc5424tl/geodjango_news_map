from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage):

    bucket_name = "mtn-assets-resource"
    location = 'media'
    file_overwrite = False

    def get_accessed_time(self, name):
        pass

    def get_created_time(self, name):
        pass

    def path(self, name):
        pass

class StaticStorage(S3Boto3Storage):

    bucket_name = "mtn-assets-resource"
    location = 'static'

    def path(self, name):
        pass

    def get_accessed_time(self, name):
        pass

    def get_created_time(self, name):
        pass

# from storages.backends.s3boto3 import S3Boto3Storage
#
# class S3MediaStorage(S3Boto3Storage):
#     location = 'media'
#     file_overwrite = False
#
#
# class S3StaticStorage(S3Boto3Storage):
#     location = "static"