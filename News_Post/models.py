from datetime import datetime
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models import Q
from Extentions.utils import get_filename_ext_rand, jalali_convertor
from django.db import models
from News_Account.models import User


def upload_image_path_post(instance, filename):
    name, ext, rand = get_filename_ext_rand(filename)
    final_name = f"{name}-{rand}{ext}"
    return f"posts/{final_name}"

def upload_image_path_galleryImage(instance, filename):
    name, ext, rand = get_filename_ext_rand(filename)
    final_name = f"{name}-{rand}{ext}"
    return f"gallery_image/{final_name}"


class PostCategory(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class PostManager(models.Manager):
    def searchForm(self, searchPostinp):
        lookup = (
                Q(title__icontains=searchPostinp) |
                Q(writer__username__icontains=searchPostinp) |
                Q(short_description__icontains=searchPostinp) |
                Q(categories__title__icontains=searchPostinp) |
                Q(tags__title__icontains=searchPostinp)
        )
        return Post.objects.filter(lookup, status='m').distinct()

    def get_m(self):
        return Post.objects.get_queryset().filter(status='m').all()


class Post(models.Model):
    CHOISE_STATUS_POST = (
        ('p', 'پیش نویس'),
        ('m', 'منتشر شده'),
    )
    title = models.CharField(max_length=50)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='posts')
    image = models.ImageField(upload_to=upload_image_path_post)
    is_specific = models.BooleanField(default=False)
    short_description = models.TextField(max_length=150, help_text='خلاصه ی خبر نباید بیش از 150 کاراکتر باشد.')
    description = RichTextUploadingField()
    categories = models.ManyToManyField(PostCategory)
    time_reading = models.IntegerField(default=0)
    timeStamp = models.DateTimeField(default=datetime.now())
    views = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    status = models.CharField(choices=CHOISE_STATUS_POST, max_length=1, default='p')

    objects = PostManager()

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

    def JtimeStamp(self):
        return jalali_convertor(self.timeStamp)

    def get_absolute_url(self):
        return f'/post/detail/{self.id}/{self.title.replace(" ","-")}'


class PostViews(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class PostGallery(models.Model):
    title = models.CharField(max_length=30)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='galleries')
    image = models.ImageField(upload_to=upload_image_path_galleryImage)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)


class PostTag(models.Model):
    title = models.CharField(max_length=30)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='tags')
    writer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title


class LikePost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')


class FavPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favs')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='favs')


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    msg = RichTextField()
    timeStamp = models.DateTimeField(auto_now_add=True)
    reported = models.BooleanField(default=False)
    pre_report = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.user} - {self.post}'
