from django.contrib.auth.models import AbstractUser
from django.db import models

from Extentions.utils import get_filename_ext_rand
from News_Sitesetting.models import Notification


def upload_image_path(instance, filename):
    name, ext, rand = get_filename_ext_rand(filename)
    final_name = f"{name}-{instance.username}-{rand}{ext}"
    return f"avatars/{final_name}"

class User(AbstractUser):
    STATUS_CHOISE = (
        ('s','ساده'),
        ('v','ویژه'),
        ('g','خبرگذار'),
        ('n','خبرنگار'),
    )
    IP = models.GenericIPAddressField(blank=True, null=True)
    avatar = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    phone = models.BigIntegerField(blank=True, null=True)
    web = models.URLField(null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=1, default='s', choices=STATUS_CHOISE)

    def delete(self, *args, **kwargs):
        self.avatar.delete()
        super().delete(*args, **kwargs)
