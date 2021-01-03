from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from News_Account.models import User
from News_Post.models import Post, Comment
from .forms import settingsSite, addAds
from News_Sitesetting.models import Contact, Opinion, Advertising, SiteSetiing

@login_required(login_url='/sign-in')
def manager_contactus(request):
	if not request.user.is_superuser:
		return redirect('/')

	return render(request, 'manager_contactus.html', {
		'contacts': Contact.objects.all().order_by('-id'),
	})


@login_required(login_url='/sign-in')
def manager_opinions(request):
	if not request.user.is_superuser:
		return redirect('/')

	return render(request, 'manager_opinions.html', {
		'opinions': Opinion.objects.all().order_by('-id'),
	})	


@login_required(login_url='/sign-in')
def manager_advertisings(request):
	if not request.user.is_superuser:
		return redirect('/')

	return render(request, 'manager_advertisings.html', {
		'adss': Advertising.objects.all().order_by('-id'),
	})


@login_required(login_url='/sign-in')
def manager_advertisings_add(request):
	if not request.user.is_superuser:
		return redirect('/')
	addads = addAds(request.POST or None)
	imageads = request.FILES.get('imageads')

	if addads.is_valid():
		saveCommit = addads.save(commit=False)
		saveCommit.image = imageads
		saveCommit.save()
		messages.info(request, 'تبلیغ با موفقیت اضافه شد.')
		return redirect('pannel:managerads')

	return render(request, 'manager_advertisings_add.html', {
		'addads':addads
	})


@login_required(login_url='/sign-in')
def manager_setting(request):
	if not request.user.is_superuser:
		return redirect('/')

	sett = SiteSetiing.objects.filter(active=True).first()
	settingForm = settingsSite(request.POST or None, initial={
		'app_name': sett.app_name,
		'about_us': sett.about_us,
		'about_website': sett.about_website,
		'place_website': sett.place_website,
		'telegram_id': sett.telegram_id,
		'whatsapp_id': sett.whatsapp_id,
		'instagram_id': sett.instagram_id,
		'scale_X': sett.scale_X,
		'scale_Y': sett.scale_Y,
		'active': sett.active,
	})
	logo = request.FILES.get('logopic')
	if settingForm.is_valid():
		app_name = settingForm.cleaned_data.get('app_name')
		about_us = settingForm.cleaned_data.get('about_us')
		about_website = settingForm.cleaned_data.get('about_website')
		place_website = settingForm.cleaned_data.get('place_website')
		telegram_id = settingForm.cleaned_data.get('telegram_id')
		whatsapp_id = settingForm.cleaned_data.get('whatsapp_id')
		instagram_id = settingForm.cleaned_data.get('instagram_id')
		scale_X = settingForm.cleaned_data.get('scale_X')
		scale_Y = settingForm.cleaned_data.get('scale_Y')
		active = settingForm.cleaned_data.get('active')
		
		sett.app_name = app_name
		sett.logo = logo
		sett.about_us = about_us
		sett.about_website = about_website
		sett.place_website = place_website
		sett.telegram_id = telegram_id
		sett.whatsapp_id = whatsapp_id
		sett.instagram_id = instagram_id
		sett.scale_X = scale_X
		sett.scale_Y = scale_Y
		sett.active = active

		sett.save()
		messages.info(request, 'تنظیمات با موفقیت اعمال شد.')
		return redirect('pannel:home')

	return render(request, 'manager_setting.html', {
		'setting': settingForm
	})

@login_required(login_url='/sign-in')
def managerReports_cmt(request):
	if not request.user.is_superuser:
		return redirect('/')
	return render(request, 'manager_reports.html', {'cmts':Comment.objects.filter(pre_report=True).all()})