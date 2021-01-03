from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect

from News_Post.models import Post, PostViews
from News_Sitesetting.models import SiteSetiing, Notification
from News_Sitesetting.forms import OpinionForm
from News_Account.models import User


def home_page(request):
	# top users
	lookup = Q(status='n') | Q(status='g')
	Goodusers = User.objects.filter(lookup).all()

	return render(request, 'home_page.html', {
		'users': Goodusers,
		'recents': Post.objects.filter(status='m').order_by('-id')[:8],
		'mostviews': Post.objects.filter(status='m').order_by('-views')[:8],
		'hots': Post.objects.filter(status='m').order_by('-comments_count')[:8],
		'pops': Post.objects.filter(status='m').order_by('-like_count')[:8]
	})


def header_partial(request):
	context = {
		'SiteSetiing': SiteSetiing.objects.filter(active=True).first(),
		'notifications': Notification.objects.all().order_by('-id'),
		'noticount': None,
	}
	if request.user.is_authenticated:
		if request.user.status == 's':
			noticount = Notification.objects.filter(is_simple=True).count()
			context['noticount'] = noticount

		elif request.user.status == 'v':
			noticount = Notification.objects.filter(is_specific=True).count()
			context['noticount'] = noticount

		elif request.user.status == 'g':
			noticount = Notification.objects.filter(is_newsTransition=True).count()
			context['noticount'] = noticount

		elif request.user.status == 'n':
			noticount = Notification.objects.filter(is_reporter=True).count()
			context['noticount'] = noticount

	return render(request, 'shared/__header.html', context)


def bottomWriter_partial(request):
	context = {
		'SiteSetiing': SiteSetiing.objects.filter(active=True).first()
	}
	return render(request, 'shared/__bottomwriter.html', context)


def opinion_footer_partial(request):
	opinionform = OpinionForm(request.POST or None)
	context = {
		'opinionform':opinionform
	}
	if opinionform.is_valid():
		opModel = opinionform.save(commit=False)
		opModel.save()
		messages.info(request, 'نظر شما با موفقیت ارسال شد. ممنون از تبادلات شما')

	return render(request, 'shared/__footer.html', context)