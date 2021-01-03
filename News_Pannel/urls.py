from django.urls import path
from . import views, views_managerUser, views_managerSite

app_name = 'pannel'
urlpatterns = [
    path('user/dashboard', views.pannel_home, name='home'),
    path('user/edit', views.pannel_edit, name='edit'),
    path('user/change-pw', views.pannel_changePassword, name='changepw'),
    path('user/saved', views.pannel_saved, name='saved'),
    path('user/delete/saved/<int:postID>', views.delete_pannel_saved, name='deletepostsave'),
    path('user/send-ticket', views.pannel_send_ticket, name='sendticket'),
    path('user/send/post', views.pannel_send_post, name='sendpost'),
    path('user/send/post/tags', views.pannel_send_post_tags, name='sendposttags'),
    path('user/send/post/galleries', views.pannel_send_post_galleries, name='sendpostgalleries'),
    path('user/release/<int:postID>', views.pannel_convert_release, name='releasepost'),

    # manager User
    path('user/manager/users', views_managerUser.managerUser, name='managerUser'),
    path('user/manager/posts', views_managerUser.managerPost, name='managerPost'),
    path('user/manager/users/edit/<int:userID>', views_managerUser.managerUser_edit, name='managerUseredit'),
    path('user/manager/posts/edit/<int:postID>', views_managerUser.managerPost_edit, name='managerPostedit'),
    path('user/manager/emails', views_managerUser.manageremail, name='manageremail'),
    path('user/manager/emails/send', views_managerUser.manageremailSend, name='manageremailsend'),
    path('user/manager/emails/remove/<int:emailID>', views_managerUser.manageremailSend_remove, name='manageremailremove'),
    path('user/manager/emails/send/<int:emailID>', views_managerUser.manageremailSend_sendmail, name='manageremailsendMail'),
    path('user/manager/charts', views_managerUser.managercharts, name='managercharts'),
    path('user/manager/notifications', views_managerUser.manager_notifications, name='managernotifications'),

    # manager Site
    path('user/manager/site/contact-us', views_managerSite.manager_contactus, name='managercontact'),
    path('user/manager/site/opinions', views_managerSite.manager_opinions, name='manageropinion'),
    path('user/manager/site/advertisings', views_managerSite.manager_advertisings, name='managerads'),
    path('user/manager/site/advertisings/add', views_managerSite.manager_advertisings_add, name='manageradsadd'),
    path('user/manager/site/setting', views_managerSite.manager_setting, name='managersetting'),
    path('user/manager/site/comments/reports', views_managerSite.managerReports_cmt, name='managercmtreport'),
]