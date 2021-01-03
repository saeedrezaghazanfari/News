from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'home'
urlpatterns = [

	# Introduction Apps
	path('', include('News_Account.urls')),
	path('', include('News_Pannel.urls')),
	path('', include('News_Post.urls')),
	path('', include('News_Sitesetting.urls')),

	# Url Pages
	path('', views.home_page, name='home'),

	# partial Views
	path('', views.header_partial, name='header'),
	path('', views.bottomWriter_partial, name='writer'),
	path('', views.opinion_footer_partial, name='footerpar'),

	path('ckeditor/', include('ckeditor_uploader.urls')),
	path('captcha/', include('captcha.urls')),
	path('admin/', admin.site.urls, name='admin'),
]

if settings.DEBUG:
	urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)