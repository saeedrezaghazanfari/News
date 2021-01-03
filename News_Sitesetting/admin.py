from django.contrib import admin

from News_Sitesetting.models import SiteSetiing, Contact, Opinion, Notification, Advertising, Send_Mail

admin.site.register(SiteSetiing)
admin.site.register(Contact)
admin.site.register(Opinion)
admin.site.register(Notification)
admin.site.register(Advertising)
admin.site.register(Send_Mail)