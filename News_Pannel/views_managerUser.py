from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from News_Account.models import User
from News_Post.models import Post, PostCategory
from .forms import Edit_User, sendMailForm, sendNotificationForm, Edit_Post
from News_Sitesetting.models import Send_Mail, Notification

@login_required(login_url='/sign-in')
def managerUser(request):
    if not request.user.is_superuser:
        return redirect('/')
    return render(request, 'manager_user.html', {
        'users':User.objects.all(),
    })

@login_required(login_url='/sign-in')
def managerPost(request):
    if not request.user.is_superuser:
        return redirect('/')
    return render(request, 'manager_post.html', {
        'posts':Post.objects.all(),
    })

@login_required(login_url='/sign-in')
def managerUser_edit(request, userID):
    if not request.user.is_superuser:
        return redirect('/')

    editUser = Edit_User(request.POST or None, initial={
        'is_active': request.user.is_active,
        'is_staff': request.user.is_staff,
        'is_superuser': request.user.is_superuser,
        'phone': request.user.phone,
        'web': request.user.web,
        'bio': request.user.bio,
        'status': request.user.status,
        'IP': request.user.IP
    })
    if editUser.is_valid():
        thisUser = User.objects.get(id=userID)
        thisUser.is_active = editUser.cleaned_data.get('is_active')
        thisUser.is_staff = editUser.cleaned_data.get('is_staff')
        thisUser.is_superuser = editUser.cleaned_data.get('is_superuser')
        thisUser.phone = editUser.cleaned_data.get('phone')
        thisUser.web = editUser.cleaned_data.get('web')
        thisUser.bio = editUser.cleaned_data.get('bio')
        thisUser.status = editUser.cleaned_data.get('status')
        thisUser.IP = editUser.cleaned_data.get('IP')

        thisUser.save()
        messages.info(request, 'کاربر با موفقیت ویرایش شد.')
        return redirect('pannel:managerUser')

    return render(request, 'edit_user.html', {
        'editUser':editUser,
        'thisUser': User.objects.get(id=userID)
    })

@login_required(login_url='/sign-in')
def managerPost_edit(request, postID):
    if not request.user.is_superuser:
        return redirect('/')

    thispost = Post.objects.get(id=postID)
    editpost = Edit_Post(request.POST or None, request.FILES or None, initial={
        'title': thispost.title,
        'writer': thispost.writer,
        'image': thispost.image,
        'description': thispost.description,
        'short_description': thispost.short_description,
        'time_reading': thispost.time_reading,
        'status': thispost.status,
    })
    if editpost.is_valid():
        thispost.title = editpost.cleaned_data.get('title')
        thispost.writer = editpost.cleaned_data.get('writer')
        if request.FILES.get('image'):
            thispost.image = request.FILES.get('image')
        thispost.description = editpost.cleaned_data.get('description')
        thispost.short_description = editpost.cleaned_data.get('short_description')
        thispost.time_reading = editpost.cleaned_data.get('time_reading')
        thispost.status = editpost.cleaned_data.get('status')

        for i in editpost.cleaned_data.get('categories'):
            thispost.categories.add(i)

        thispost.save()
        messages.info(request, 'خبر با موفقیت ویرایش شد.')
        return redirect('pannel:managerPost')

    return render(request, 'edit_post.html', {
        'editPost':editpost,
        'thisPost': Post.objects.get(id=postID),
    })

@login_required(login_url='/sign-in')
def manageremail(request):
    if not request.user.is_superuser:
        return redirect('/')

    sendmailform = sendMailForm(request.POST or None)
    if sendmailform.is_valid():
        sendmailformData = sendmailform.save(commit=False)
        sendmailformData.save()
        messages.info(request, 'متن ایمیل شما با موفقیت ذخیره شد.')
        return redirect('pannel:manageremailsend')

    return render(request, 'manager_email.html', {
        'sendmailform':sendmailform
    })


@login_required(login_url='/sign-in')
def manageremailSend(request):
    if not request.user.is_superuser:
        return redirect('/')
    return render(request, 'manager_email_send.html', {
        'allMails':Send_Mail.objects.all(),
    })


@login_required(login_url='/sign-in')
def manageremailSend_sendmail(request, emailID):
    if not request.user.is_superuser:
        return redirect('/')

    if request.POST:
        if request.POST.get('sends'):
            #todo send mail
            pass
        if request.POST.get('sendv'):
            #todo send mail
            pass
        if request.POST.get('sendg'):
            #todo send mail
            pass
        if request.POST.get('sendn'):
            #todo send mail
            pass
        if request.POST.get('sendsuper'):
            #todo send mail
            pass
        if request.POST.get('sendstaff'):
            #todo send mail
            pass

    return render(request, 'manager_email_send_mailing.html', {
        'email':Send_Mail.objects.get(id=emailID),
        'sendsCount': User.objects.filter(status='s').count(),
        'sendvCount': User.objects.filter(status='v').count(),
        'sendgCount': User.objects.filter(status='g').count(),
        'sendnCount': User.objects.filter(status='n').count(),
        'sendsuperCount': User.objects.filter(is_superuser=True).count(),
        'sendstaffCount': User.objects.filter(is_staff=True).count(),
    })


@login_required(login_url='/sign-in')
def manageremailSend_remove(request, emailID):
    if not request.user.is_superuser:
        return redirect('/')
    Send_Mail.objects.get(id=emailID).delete()
    messages.info(request, 'ایمیل با موفقیت حذف شد.')
    return redirect('pannel:manageremailsend')


@login_required(login_url='/sign-in')
def managercharts(request):
    if not request.user.is_superuser:
        return redirect('/')

    return render(request, 'pannel_charts.html', {
        'times':Send_Mail.objects.all(),
        'prices': Send_Mail.objects.all()
    })


@login_required(login_url='/sign-in')
def chart_code_partial(request):
    if not request.user.is_superuser:
        return redirect('/')

    return render(request, 'chart_partial.html', {
        'users': User.objects.count(),
        'users_s': User.objects.filter(status='s').count(),
        'users_v': User.objects.filter(status='v').count(),
        'users_g': User.objects.filter(status='g').count(),
        'users_n': User.objects.filter(status='n').count(),
        'posts_draft': Post.objects.filter(status='p').count(),
        'posts_release': Post.objects.filter(status='m').count(),

        'today': Post.objects.filter(timeStamp__gte=datetime.now() - timedelta(hours=24), timeStamp__lte=datetime.now()).count(),
        '1day': Post.objects.filter(timeStamp__gte=datetime.now() - timedelta(days=2), timeStamp__lte=datetime.now() - timedelta(hours=24)).count(),
        '2day': Post.objects.filter(timeStamp__gte=datetime.now() - timedelta(days=3), timeStamp__lte=datetime.now() - timedelta(days=2)).count(),
        '3day': Post.objects.filter(timeStamp__gte=datetime.now() - timedelta(days=4), timeStamp__lte=datetime.now() - timedelta(days=3)).count(),
        '4day': Post.objects.filter(timeStamp__gte=datetime.now() - timedelta(days=5), timeStamp__lte=datetime.now() - timedelta(days=4)).count(),
        '5day': Post.objects.filter(timeStamp__gte=datetime.now() - timedelta(days=6), timeStamp__lte=datetime.now() - timedelta(days=5)).count(),
        '6day': Post.objects.filter(timeStamp__gte=datetime.now() - timedelta(days=7), timeStamp__lte=datetime.now() - timedelta(days=6)).count(),
        '7day': Post.objects.filter(timeStamp__gte=datetime.now() - timedelta(days=8), timeStamp__lte=datetime.now() - timedelta(days=7)).count(),
    })


@login_required(login_url='/sign-in')
def manager_notifications(request):
    if not request.user.is_superuser:
        return redirect('/')

    sends = request.POST.get('sends')
    sendv = request.POST.get('sendv')
    sendg = request.POST.get('sendg')
    sendn = request.POST.get('sendn')

    sendNotification = sendNotificationForm(request.POST or None)
    if sendNotification.is_valid():
        saveCommit: Notification = sendNotification.save(commit=False)

        if sends:
            saveCommit.is_simple = True
        if sendv:
            saveCommit.is_specific = True
        if sendg:
            saveCommit.is_newsTransition = True
        if sendn:
            saveCommit.is_reporter = True

        saveCommit.save()
        messages.info(request, 'اعلان ها با موفقیت ارسال شدند.')
        return redirect('pannel:home')

    return render(request, 'manager_notifications.html', {
        'sendNotification':sendNotification
    })