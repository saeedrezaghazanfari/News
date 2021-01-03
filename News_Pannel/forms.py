from django import forms
from News_Account.models import User
from django.core import validators
from News_Post.models import Post, PostTag, PostGallery
from django.utils.translation import gettext_lazy as _

from News_Sitesetting.models import Send_Mail, Notification, SiteSetiing, Advertising


class change_data(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "avatar", "phone", "web", "bio"]
        labels = {
            'first_name': _('نام'),
            'last_name': _('نام خانوادگی'),
            'avatar': _('لوگو'),
            'phone': _('شماره تلفن'),
            'web': _('وبسایت'),
            'bio': _('بیوگرافی'),
        }

class change_Pw(forms.Form):
    pw1 = forms.CharField(widget=forms.PasswordInput(), label='رمزعبور <b>جدید</b> را وارد کنید:', validators=[
        validators.MinLengthValidator(5, 'رمز عبور نباید کمتر از 5 کاراکتر باشد.'),
        validators.MaxLengthValidator(25, 'رمز عبور نباید بیشتر از 25 کاراکتر باشد.')
    ], required=True)
    pw2 = forms.CharField(widget=forms.PasswordInput(), label='رمزعبور <b>جدید</b> را <b>دوباره</b> وارد کنید:', required=True)

    def clean_pw2(self):
        pw1 = self.cleaned_data.get('pw1')
        pw2 = self.cleaned_data.get('pw2')
        if pw1 != pw2:
            raise forms.ValidationError('باید مقادیر دو فیلد برابر باشند.')
        return pw2

class send_ticket(forms.Form):
    subject = forms.CharField(widget=forms.TextInput(), required=True, label='عنوان تیکت')
    ticket = forms.CharField(widget=forms.Textarea(), required=True, label='متن تیکت',validators=[
        validators.MinLengthValidator(20, 'متن تیکت نباید کمتر از 20 کاراکتر باشد.')
    ])

class send_post_postdata(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'short_description', 'categories', 'time_reading']
        labels = {
            'title': _('عنوان خبر'),
            'description': _('مشروح خبر'),
            'short_description': _('خلاصه ی خبر'),
            'categories': _('دسته بندی های خبر'),
            'time_reading': _('زمان خواندن')
        }

class send_post_tags(forms.ModelForm):
    class Meta:
        model = PostTag
        fields = ['title']
        labels = {
            'title': _('عنوان تگ'),
        }

class send_post_galleries(forms.ModelForm):
    class Meta:
        model = PostGallery
        fields = ['title']
        labels = {
            'title': _('عنوان عکس'),
        }

class Edit_User(forms.ModelForm):
    class Meta:
        model = User
        fields = ['is_active', 'is_staff', 'is_superuser', 'phone', 'web', 'bio', 'status', 'IP']
        labels = {
            'phone': _('شماره تلفن'),
            'web': _('وبسایت کاربر'),
            'bio': _('بیوگرافی'),
            'status': _('وضعیت خبری'),
            'IP': _('آی پی')
        }

class Edit_Post(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'writer', 'categories', 'image', 'description', 'short_description', 'time_reading', 'status']
        labels = {
            'title': _('عنوان خبر'),
            'writer': _('نویسنده ی خبر'),
            'image': _('تصویر محصول'),
            'description': _('مشروح خبر'),
            'short_description': _('خلاصه ی خبر'),
            'time_reading': _('زمان خواندن'),
            'categories': _('دسته بندی های خبر'),
            'status': _('وضعیت'),
        }

class sendMailForm(forms.ModelForm):
    class Meta:
        model = Send_Mail
        fields = ['subject', 'msg']
        labels = {
            'subject': _('عنوان ایمیل'),
            'msg': _('متن ایمیل'),
        }

class sendNotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['title', 'ntf']
        labels = {
            'title': _('عنوان اعلان'),
            'ntf': _('متن اعلان'),
        }

class settingsSite(forms.ModelForm):
    class Meta:
        model = SiteSetiing
        fields = ['app_name' ,'about_us' ,'about_website' ,'place_website' ,'telegram_id' ,'whatsapp_id' ,'instagram_id' ,'scale_X' ,'scale_Y' ,'active']
        labels = {
            'app_name': _('نام فروشگاه'),
            'about_us': _('درباره ی ما'),
            'about_website': _('درباره ی وبسایت'),
            'place_website': _('آدرس وبسایت'),
            'telegram_id': _('آیدی تلگرام'),
            'whatsapp_id': _('آدرس واتساپ'),
            'instagram_id': _('آیدی اینستاگرام'),
            'scale_X': _('مقیاس ایکس در نقسه'),
            'scale_Y': _('مقیاس ایگرگ در نقشه'),
            'active': _('فعال / غیرفعال'),
        }

class addAds(forms.ModelForm):
    class Meta:
        model = Advertising
        fields = ['title']
        labels = {
            'title': _('عنوان تبلیغ'),
        }