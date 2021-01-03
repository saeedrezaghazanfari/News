from django.urls import path
from . import views

app_name = 'sitesetting'
urlpatterns = [
    path('about-us', views.aboutus_page, name='aboutus'),
    path('contact-us', views.contactus_page, name='contactus'),

]