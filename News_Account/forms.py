from django import forms
from .models import User
from django.core import validators
from captcha.fields import CaptchaField
# from django.contrib.auth.forms import UserCreationForm

class SingIn(forms.Form):
    emailOrUn = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder':'ایمیل و یا نام کاربری خود را لاتین وارد کنید:', 'class':'form-control form-control-auth'}
        ),
        label= '<b>ایمیل</b> یا <b>نام کاربری</b>'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder':'رمز عبور خود را لاتین وارد کنید:', 'class':'form-control form-control-auth', 'id':'passlogin'}
        ),
        label= '<b>رمز عبور</b>'
    )
    captcha = CaptchaField()

    def clean_emailOrUn(self):
        emailOrun = self.cleaned_data.get('emailOrUn')

        if not User.objects.filter(email__iexact=emailOrun).first():
            if not User.objects.filter(username__iexact=emailOrun).first():
                  raise forms.ValidationError('نام کاربری / ایمیل وارد شده فاقد اعتبار است.')

        if not User.objects.filter(username__iexact=emailOrun).first():
            if not User.objects.filter(email__iexact=emailOrun).first():
                  raise forms.ValidationError('نام کاربری / ایمیل وارد شده فاقد اعتبار است.')

        if not emailOrun:
            raise forms.ValidationError('فیلد ایمیل / نام کاربری را پر کنید.')
        return emailOrun


class SingUp(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder':'نام کاربری خود را لاتین وارد کنید:', 'class':'form-control form-control-auth'}
        ),
        label= '<b>نام کاربری</b>'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'placeholder':'ایمیل خود را وارد کنید:', 'class':'form-control form-control-auth'}
        ),
        label= '<b>ایمیل</b>'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder':'رمز عبور خود را لاتین وارد کنید:', 'class':'form-control form-control-auth'}
        ),
        label= '<b>رمز عبور</b>',
        validators=[
            validators.MinLengthValidator(5, 'رمز عبور نباید کمتر از 5 کاراکتر باشد.'),
            validators.MaxLengthValidator(25, 'رمز عبور نباید بیشتر از 25 کاراکتر باشد.'),
        ]
    )
    repassword = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder':'رمز عبور خود را دوباره وارد کنید:', 'class':'form-control form-control-auth'}
        ),
        label= '<b>تکرار رمز عبور</b>'
    )
    captcha = CaptchaField()


    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).first():
            raise forms.ValidationError('نام کاربری دیگری انتخاب کنید.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).first():
            raise forms.ValidationError('ایمیل دیگری انتخاب کنید.')
        return email

    def clean_repassword(self):
        p1 = self.cleaned_data.get('password')
        p2 = self.cleaned_data.get('repassword')
        if p1 != p2:
            raise forms.ValidationError('باید دو رمز عبور یکسان باشند.')
        return p2


# class SignupForm(UserCreationForm):
#     email = forms.EmailField(max_length=200, help_text='Required')
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2')