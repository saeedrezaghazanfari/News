from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import change_data, change_Pw, send_ticket, send_post_postdata, send_post_tags, send_post_galleries
from News_Account.models import User
from News_Post.models import FavPost, Post, Comment
from News_Sitesetting.models import Opinion, Contact
from .models import Ticket

@login_required(login_url='/sign-in')
def pannel_home(request):
    return render(request, 'home_pannel.html', {
        'allPosts': Post.objects.filter(status='p').all().order_by('-id'),
        'posts': Post.objects.filter(writer_id=request.user.id).all()
    })

@login_required(login_url='/sign-in')
def pannel_sidebar(request):
    return render(request, 'Administrator/__sidebar.html', {
        'opinionCount': Opinion.objects.count(),
        'contactCount': Contact.objects.count(),
        'reportCount': Comment.objects.filter(pre_report=True).count()
    })

@login_required(login_url='/sign-in')
def pannel_edit(request):
    change_data_form = change_data(request.POST or None, request.FILES or None, initial={
        'first_name':request.user.first_name,
        'last_name':request.user.last_name,
        'avatar':request.user.avatar,
        'phone':request.user.phone,
        'web':request.user.web,
        'bio':request.user.bio,
    })
    context = {
        'change_data_form':change_data_form
    }
    if request.POST or request.FILES:
        if change_data_form.is_valid():
            first_name = change_data_form.cleaned_data.get('first_name')
            last_name = change_data_form.cleaned_data.get('last_name')
            avatar = request.FILES.get('avatar')
            phone = change_data_form.cleaned_data.get('phone')
            web = change_data_form.cleaned_data.get('web')
            bio = change_data_form.cleaned_data.get('bio')

            thisUser = User.objects.get(id=request.user.id)
            if first_name:
                thisUser.first_name = first_name
            if last_name:
                thisUser.last_name = last_name
            if avatar:
                thisUser.avatar = avatar
            if phone:
                thisUser.phone = phone
            if web:
                thisUser.web = web
            if bio:
                thisUser.bio = bio

            thisUser.save()
            messages.info(request, 'تغییرات با موفقیت ثبت شدند.')
            return redirect('/user/dashboard')

    return render(request, 'pannel_edit.html', context)


@login_required(login_url='/sign-in')
def pannel_changePassword(request):
    changepw = change_Pw(request.POST or None)
    thisUser = request.user
    context = {
        'changepw':changepw
    }
    if changepw.is_valid():
        pw1 = changepw.cleaned_data.get('pw1')
        pw2 = changepw.cleaned_data.get('pw2')

        if pw1 == pw2:
            thisUser.set_password(pw2)
            thisUser.save()

            messages.info(request, 'رمز عبور جدید با موفقیت ثبت شد.')
            return redirect('/user/dashboard')

    return render(request, 'change_pw.html', context)


@login_required(login_url='/sign-in')
def pannel_saved(request):
    favs = FavPost.objects.filter(user_id=request.user.id).order_by('-id')
    context = {'favs':favs}
    return render(request, 'pannel_saved.html', context)


@login_required(login_url='/sign-in')
def delete_pannel_saved(request, postID):
    FavPost.objects.get(user_id=request.user.id, post_id=postID).delete()
    messages.info(request, 'خبر مورد نظر با موفقیت ازلیست بایگانی حذف شد.')
    return redirect('/user/dashboard')


@login_required(login_url='/sign-in')
def pannel_send_ticket(request):
    send_ticket_form = send_ticket(request.POST or None)
    context = {'send_ticket_form':send_ticket_form}
    if send_ticket_form.is_valid():
        subject = send_ticket_form.cleaned_data.get('subject')
        ticket = send_ticket_form.cleaned_data.get('ticket')

        Ticket.objects.create(user=request.user.username, subject=subject, ticket=ticket)
        messages.info(request, 'تیکت شما با موفقیت ثبت شد. در اسرع وقت بررسی میشود.')
        return redirect('/user/dashboard')

    return render(request, 'pannel_send_ticket.html', context)


@login_required(login_url='/sign-in')
def pannel_send_post(request):
    if request.user.status == 's' or request.user.status == 'v':
        messages.info(request, 'شما باید عضویت ویژه داشته باشید.')
        return redirect('/user/dashboard')

    sendpost = send_post_postdata(request.POST or None, request.FILES or None)

    context = {
        'sendpost': sendpost,
    }

    image = request.FILES.get('imagePost')

    if sendpost.is_valid():
        save_post: Post = sendpost.save()
        for i in sendpost.cleaned_data.get('categories'):
            save_post.categories.add(i)
        save_post.image = image
        save_post.status = 'p'
        save_post.writer = request.user

        save_post.save()
        messages.info(request, 'با تشکر، پست شما در سایت قرار گرفت ، بزودی مورد بررسی قرار خواهد گرفت.')
        return redirect('pannel:sendposttags')

    return render(request, 'pannel_send_post.html', context)


@login_required(login_url='/sign-in')
def pannel_send_post_tags(request):
    if request.user.status == 's' or request.user.status == 'v':
        messages.info(request, 'شما باید عضویت ویژه داشته باشید.')
        return redirect('/user/dashboard')

    sendposttags = send_post_tags(request.POST or None)
    selectPostuser = request.POST.get('selectPostuser')
    print(selectPostuser)

    if sendposttags.is_valid():
        saveTAG = sendposttags.save(commit=False)
        saveTAG.post = Post.objects.get(id=selectPostuser)
        saveTAG.writer = request.user
        saveTAG.save()
        messages.info(request, 'تگ پست شما با موفقیت افزوده شد. شما میتوانید چندین تگ ایجاد کنید.')
        return redirect('pannel:sendpostgalleries')

    return render(request, 'pannel_send_post_tags.html', {
        'send_post_tags':send_post_tags,
        'posts':Post.objects.filter(writer_id=request.user.id).all()
    })


@login_required(login_url='/sign-in')
def pannel_send_post_galleries(request):
    if request.user.status == 's' or request.user.status == 'v':
        messages.info(request, 'شما باید عضویت ویژه داشته باشید.')
        return redirect('/user/dashboard')

    sendpostgalleries = send_post_galleries(request.POST or request.FILES)
    selectPostuser = request.POST.get('selectPostuser')
    imagePostGall = request.FILES.get('imagePostGall')

    if sendpostgalleries.is_valid():
        saveGall = sendpostgalleries.save(commit=False)
        saveGall.post = Post.objects.get(id=selectPostuser)
        saveGall.image = imagePostGall
        saveGall.writer = request.user
        saveGall.save()
        messages.info(request, 'گالری پست شما با موفقیت ساخته شد. شما میتوانید تصاویر بیشتری به گالری خبر خود بیفزایید.')
        return redirect('pannel:home')

    return render(request, 'pannel_send_post_galleries.html', {
        'sendpostgalleries':sendpostgalleries,
        'posts': Post.objects.filter(writer_id=request.user.id).all()
    })


@login_required(login_url='/sign-in')
def pannel_convert_release(request, postID):
    if not request.user.is_superuser:
        return redirect('/')

    post = Post.objects.filter(id=postID).first()
    post.status = 'm'
    post.save()
    messages.info(request, 'پست با موفقیت منتشر شد.')
    return redirect('pannel:home')