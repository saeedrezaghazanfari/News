from django.db import models

from Extentions.utils import get_filename_ext_rand

def upload_image_path_logoWeb(instance, filename):
    name, ext, rand = get_filename_ext_rand(filename)
    final_name = f"{name}-{rand}{ext}"
    return f"logoweb/{final_name}"

def upload_image_path_contactImg(instance, filename):
    name, ext, rand = get_filename_ext_rand(filename)
    final_name = f"{name}-{rand}{ext}"
    return f"contactImg/{final_name}"

def upload_image_path_advers(instance, filename):
    name, ext, rand = get_filename_ext_rand(filename)
    final_name = f"{name}-{rand}{ext}"
    return f"advertising/{final_name}"

class SiteSetiing(models.Model):
    app_name = models.CharField(max_length=20)
    logo = models.ImageField(upload_to=upload_image_path_logoWeb)
    about_us = models.TextField()
    about_website = models.TextField()
    place_website = models.TextField()
    telegram_id = models.URLField(blank=True, null=True)
    whatsapp_id = models.URLField(blank=True, null=True)
    instagram_id = models.URLField(blank=True, null=True)
    scale_X = models.FloatField(default=0)
    scale_Y = models.FloatField(default=0)
    active = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        self.logo.delete()
        super().delete(*args, **kwargs)

class Contact(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=50)
    image = models.ImageField(blank=True, null=True, upload_to=upload_image_path_contactImg)
    msg = models.TextField()
    timeStamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)


class Opinion(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=50)
    msg = models.TextField()
    timeStamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)    


class Notification(models.Model):
    title = models.CharField(max_length=50)
    ntf = models.TextField()
    is_simple = models.BooleanField(default=False)
    is_specific = models.BooleanField(default=False)
    is_newsTransition = models.BooleanField(default=False)
    is_reporter = models.BooleanField(default=False)
    timeStamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Advertising(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to=upload_image_path_advers)
    link = models.URLField(default='http://www.')
    timeStamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

class Send_Mail(models.Model):
    subject = models.CharField(max_length=200)
    msg = models.TextField()
    sended = models.BooleanField(default=False)
    timeStamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):return self.subject
