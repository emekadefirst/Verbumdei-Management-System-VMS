from whitenoise.storage import CompressedManifestStaticFilesStorage
from django.conf import settings
from django.core.files.storage import FileSystemStorage


class MediaStorage(FileSystemStorage):
    location = settings.MEDIA_ROOT
    base_url = settings.MEDIA_URL


class CustomStaticFilesStorage(CompressedManifestStaticFilesStorage):
    pass
