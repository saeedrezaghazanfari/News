from django.urls import path, re_path
from . import views

app_name = 'auth'
urlpatterns = [
    path('sign-in', views.sign_in_page , name='signin'),
    path('sign-out', views.sign_out_page , name='signout'),
    path('sign-up', views.sign_up_page , name='signup'),

    # path('signup/', views.signup.as_view(), name='signup'),
    # re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),

]