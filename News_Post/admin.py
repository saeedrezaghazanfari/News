from django.contrib import admin

from News_Post.models import (
    Post, PostCategory, LikePost, FavPost, PostGallery, PostTag, Comment, PostViews
)

admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(LikePost)
admin.site.register(FavPost)
admin.site.register(PostGallery)
admin.site.register(PostTag)
admin.site.register(Comment)
admin.site.register(PostViews)