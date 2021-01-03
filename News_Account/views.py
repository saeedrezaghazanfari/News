from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.conf import settings
from .forms import SingIn, SingUp
from .models import User

def sign_in_page(request):
	if request.user.is_authenticated:
		messages.info(request, 'شما در حال حاضر دارای یک حساب کاربری فعال میباشید.')
		return redirect('/')

	signin = SingIn(request.POST or None)
	context = {
		'sigin':signin
	}
	if signin.is_valid():
		usernameOremail = signin.cleaned_data.get('emailOrUn')
		password = signin.cleaned_data.get('password')
		myuser = User.objects.filter(email__iexact=usernameOremail).first()
		if myuser:
			user = authenticate(request, username=myuser.username, password=password)
		elif User.objects.filter(username__iexact=usernameOremail).first():
			user = authenticate(request, username=usernameOremail, password=password)
		else:
			signin.add_error('emailOrUn', 'ایمیل / نام کاربری شما فاقد اعتبار است.')

		if user:
			login(request, user)
			context['sigin'] = signin

			# get IP
			x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
			if x_forwarded_for:
				ip = x_forwarded_for.split(',')[0]
			else:
				ip = request.META.get('REMOTE_ADDR')
			userip = User.objects.get(id=request.user.id)
			userip.IP = ip
			userip.save()

			messages.info(request, 'شما با موفقیت وارد شدید.')
			return redirect('/')
		else:
			signin.add_error('password', 'رمز عبور اشتباه است.')

	return render(request, 'sign_in.html', context)

def sign_up_page(request):
	if request.user.is_authenticated:
		messages.info(request, 'شما در حال حاضر دارای یک حساب کاربری فعال میباشید.')
		return redirect('/')

	signup = SingUp(request.POST or None)
	context = {
		'signup':signup
	}
	if signup.is_valid():
		username = signup.cleaned_data.get('username')
		email = signup.cleaned_data.get('email')
		repassword = signup.cleaned_data.get('repassword')
		User.objects.create_user(username=username, email=email, password=repassword)
		context['signup'] = signup

		# send Mail
		subject = 'به طلانیوز خوش آمدید'
		message = f'<div style="text-align: right; direction: rtl;"><h4 style="font-width: bolder;">با سلام و احترام خدمت شما کاربر با نام کاربری {username}</h4><p>ثبتنام شما با موفقیت در سایت طلانیوز انجام گردید. شما میتوانید از طریق لینک زیر اقدام به ورود به سایت بفرمایید:</p><a style="text-align: center; direction: ltr;" href="http://127.0.0.1:8000/sign-in">ورود به وبسایت خبری طلانیوز</a></div>'
		from_email = settings.EMAIL_HOST_USER
		to_list = [email]
		msg_EMAIL = EmailMessage(subject, message, from_email, to_list)
		msg_EMAIL.content_subtype = "html"
		msg_EMAIL.send()

		messages.info(request, 'ساخت حساب کاربری شما موفقیت آمیز بود.')
		messages.info(request, 'لطفا برای ورود از طریق ایمیل اقدام کنید.')

	return render(request, 'sign_up.html', context)

def sign_out_page(request):
	logout(request)
	messages.info(request, 'شما با موفقیت از حساب کاربری خود خارج شده اید.')
	return redirect('/sign-in')




## todo: this is for email forget code
## problem is in token.py file in import six module

# from django.http import HttpResponse
# from .forms import SignupForm
# from django.contrib.sites.shortcuts import get_current_site
# from django.utils.encoding import force_bytes, force_text
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.template.loader import render_to_string
# from .tokens import account_activation_token
# from django.core.mail import EmailMessage
#
# class signup(CreateView):
# 	form_class = SignupForm
# 	template_name = "registration/register.html"
#
# 	def form_valid(self, form):
# 		user = form.save(commit=False)
# 		user.is_active = False
# 		user.save()
# 		current_site = get_current_site(self.request)
# 		mail_subject = 'فعال سازی اکانت'
# 		message = render_to_string('registration/activate_account.html', {
# 			'user': user,
# 			'domain': current_site.domain,
# 			'uid':urlsafe_base64_encode(force_bytes(user.pk)),
# 			'token':account_activation_token.make_token(user),
# 		})
# 		to_email = form.cleaned_data.get('email')
# 		email = EmailMessage(
# 					mail_subject, message, to=[to_email]
# 		)
# 		email.send()
# 		return HttpResponse('لینک فعال سازی به ایمیل شما ارسال شد. <a href="/login">ورود</a>')
#
# def activate(request, uidb64, token):
#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         return HttpResponse('اکانت شما با موفقیت فعال شد. برای ورود کلیک کنید: <a href="/sign-in">ورود</a>')
#     else:
#         return HttpResponse('لینک فعالسازی منقضی شده است. ثبتان')