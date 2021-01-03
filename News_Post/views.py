from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import Post, PostCategory, Comment, FavPost, LikePost, PostViews
from News_Sitesetting.models import Advertising
from .forms import SendCommentForm, SendReplyForm

class PostList(ListView):
    template_name = 'post_list.html'
    model = Post
    paginate_by = 4
    def get_context_data(self, ** kwargs):
        context = super().get_context_data(** kwargs)
        context['recents'] = Post.objects.filter(status='m').order_by('-id')[:8]
        context['hots'] = Post.objects.filter(status='m').order_by('-comments_count')[:8]
        context['pops'] = Post.objects.filter(status='m').order_by('-like_count')[:8]
        return context
    queryset = Post.objects.filter(status='m').all()


def post_detail(request, postID, postTITLE):
    # this post
    thispost: Post = Post.objects.get(id=postID)

    # categories Rels Items
    a = thispost.categories.first()
    rel_posts = Post.objects.filter(status='m', categories=a).distinct()

    # comment Post
    sendcomment = SendCommentForm(request.POST or None, initial={'post_id':thispost.id})
    if sendcomment.is_valid():
        cmt = sendcomment.cleaned_data.get('msg')
        post_id = sendcomment.cleaned_data.get('post_id')
        Comment.objects.create(user_id=request.user.id, post_id=post_id, msg=cmt)
        messages.info(request, 'نظر شما با موفقیت در سایت قرار گرفت.')
        return redirect(f'{thispost.get_absolute_url}')

    # post Veiws
    if request.user.is_authenticated:
        exvipo = PostViews.objects.filter(user_id=request.user.id, post_id=thispost.id).first()
        if not exvipo:
            PostViews.objects.create(user_id=request.user.id, post_id=thispost.id)
        thispost.views = PostViews.objects.filter(post_id=thispost.id).count()
        thispost.save()

    # post likes count
    thispost.like_count = LikePost.objects.filter(post_id=thispost.id).count()
    thispost.save()

    # post comments count
    thispost.comments_count = Comment.objects.filter(post_id=thispost.id).count()
    thispost.save()

    # Reply Post
    sendreply = SendReplyForm(request.POST or None, initial={'post_id':thispost.id})
    if sendreply.is_valid():
        rpl = sendreply.cleaned_data.get('rpl')
        post_id = sendreply.cleaned_data.get('post_id')
        comment_id = request.POST.get('comment_id')
        Comment.objects.create(user_id=request.user.id, post_id=post_id, parent=Comment.objects.get(id=comment_id), msg=rpl)
        messages.info(request, 'پاسخ شما با موفقیت در سایت قرار گرفت.')
        return redirect(f'{thispost.get_absolute_url}')

    # Comments
    comments = Comment.objects.filter(post_id=thispost.id, reported=False).all()

    # like Boolean
    if LikePost.objects.filter(user_id=request.user.id, post_id=thispost.id).first():
        likeBool = True
    else:
        likeBool = False
    countLike = LikePost.objects.filter(post_id=thispost.id).count()

    # fav Boolean
    if FavPost.objects.filter(user_id=request.user.id, post_id=thispost.id).first():
        favBool = True
    else:
        favBool = False

    return render(request, 'post_details.html', {
        'post': thispost,
        'rel_posts': rel_posts,
        'sendcomment': sendcomment,
        'sendreply': sendreply,
        'comments': comments,
        'likeBool': likeBool,
        'favBool': favBool,
        'countLike': countLike
    })


def sidebar_list_partial(request):
    context = {
        'categories': PostCategory.objects.all()
    }
    return render(request, 'partials/sidebar_listpost.html', context)


class searchPost(ListView):
    template_name = 'post_list.html'
    model = Post
    paginate_by = 4
    def get_context_data(self, ** kwargs):
        context = super().get_context_data(** kwargs)
        context['recents'] = Post.objects.filter(status='m').order_by('-id')[:8]
        context['hots'] = Post.objects.filter(status='m').order_by('-comments_count')[:8]
        context['pops'] = Post.objects.filter(status='m').order_by('-like_count')[:8]
        return context
    def get_queryset(self):
        request = self.request
        searchq = request.GET.get('post')
        if searchq:
            messages.info(request, 'نتایج جستجوی شما اعلام شد.')
            return Post.objects.searchForm(searchPostinp=searchq)
        messages.info(request, 'لطفا مقداری را برای جستجو انتخاب کنید.')
        return Post.objects.get_m()


@login_required(login_url='/sign-in')
class postSpecific(ListView):
    template_name = 'post_list.html'
    model = Post
    paginate_by = 4
    def get_context_data(self, ** kwargs):
        context = super().get_context_data(** kwargs)
        context['recents'] = Post.objects.filter(status='m').order_by('-id')[:8]
        context['hots'] = Post.objects.filter(status='m').order_by('-comments_count')[:8]
        context['pops'] = Post.objects.filter(status='m').order_by('-like_count')[:8]
        return context
    def get_queryset(self):
        CategoryTitle = self.kwargs.get('CategoryTitle')
        if CategoryTitle:
            messages.info(self.request, 'اخباری متناسب با نام دسته بندی وارد شده پیدا شدند.')
            return Post.objects.filter(categories__title__icontains=CategoryTitle, status='m').all().distinct()
        messages.info(self.request, 'دسته بندی محصول مورد نظر را وارد کنید.')
        return Post.objects.get_m()

    # def get_queryset(self):
    #     request = self.request
    #     if request.user.status == 'v' or request.user.status == 'n':
    #         query = Post.objects.filter(is_specific=True, status='m').all()
    #         messages.info(request, 'نتایج جستجوی شما اعلام شد.')
    #         if query:
    #             return query
    #         messages.info(request, 'هنوز ویژه نامه ای در سایت قرار داده نشده است.')
    #         return redirect('post:list')
    #     messages.info(request, 'برای دیدن ویژه نامه باید مقام خبرنگار یا عضو ویژه داشته باشید.')
    #     return redirect('home')


class searchPostTag(ListView):
    template_name = 'post_list.html'
    model = Post
    paginate_by = 4
    def get_context_data(self, ** kwargs):
        context = super().get_context_data(** kwargs)
        context['recents'] = Post.objects.filter(status='m').order_by('-id')[:8]
        context['hots'] = Post.objects.filter(status='m').order_by('-comments_count')[:8]
        context['pops'] = Post.objects.filter(status='m').order_by('-like_count')[:8]
        return context
    def get_queryset(self):
        tagTitle = self.kwargs.get('tagTitle')
        if tagTitle:
            messages.info(self.request, 'اخباری متناسب با تگ وارد شده پیدا شدند.')
            return Post.objects.filter(tags__title__iexact=tagTitle, status='m').all().distinct()
        messages.info(self.request, 'تگ خبر مورد نظر را وارد کنید.')
        return Post.objects.get_m()

class searchPostCateGory(ListView):
    template_name = 'post_list.html'
    model = Post
    paginate_by = 4
    def get_context_data(self, ** kwargs):
        context = super().get_context_data(** kwargs)
        context['recents'] = Post.objects.filter(status='m').order_by('-id')[:8]
        context['hots'] = Post.objects.filter(status='m').order_by('-comments_count')[:8]
        context['pops'] = Post.objects.filter(status='m').order_by('-like_count')[:8]
        return context
    def get_queryset(self):
        CategoryTitle = self.kwargs.get('CategoryTitle')
        if CategoryTitle:
            messages.info(self.request, 'اخباری متناسب با نام دسته بندی وارد شده پیدا شدند.')
            return Post.objects.filter(categories__title__icontains=CategoryTitle, status='m').all().distinct()
        messages.info(self.request, 'دسته بندی محصول مورد نظر را وارد کنید.')
        return Post.objects.get_m()


class postMany(ListView):
    template_name = 'post_list.html'
    model = Post
    paginate_by = 4
    def get_context_data(self, ** kwargs):
        context = super().get_context_data(** kwargs)
        context['recents'] = Post.objects.filter(status='m').order_by('-id')[:8]
        context['hots'] = Post.objects.filter(status='m').order_by('-comments_count')[:8]
        context['pops'] = Post.objects.filter(status='m').order_by('-like_count')[:8]
        return context
    def get_queryset(self):
        many = self.kwargs.get('Many')
        if many:
            messages.info(self.request, f'<span class="number">{many}</span> خبر اخیر در حال نمایش هستند.')
            return Post.objects.filter(status='m').all()[:many]
        messages.info(self.request, 'تعداد خبر وارد شده معتبر نیست.')
        return Post.objects.get_m()


class postTime(ListView):
    template_name = 'post_list.html'
    model = Post
    paginate_by = 4
    def get_context_data(self, ** kwargs):
        context = super().get_context_data(** kwargs)
        context['recents'] = Post.objects.filter(status='m').order_by('-id')[:8]
        context['hots'] = Post.objects.filter(status='m').order_by('-comments_count')[:8]
        context['pops'] = Post.objects.filter(status='m').order_by('-like_count')[:8]
        return context
    def get_queryset(self):
        postTime = self.kwargs.get('postTime')

        if postTime == 'today':
            timee = datetime.today() - timedelta(hours=24)
            messages.info(self.request, 'اخبار امروز در حال نمایش هستند.')
            return Post.objects.filter(timeStamp__gte=timee, status='m').all()

        if postTime == 'yesterday':
            timee = datetime.now() - timedelta(days=2)
            messages.info(self.request, 'اخبار دیروز در حال نمایش هستند.')
            return Post.objects.filter(timeStamp__gte=timee, timeStamp__lte=datetime.now(), status='m').all()

        if postTime == 'this-week':
            timee = datetime.now() - timedelta(days=7)
            messages.info(self.request, 'اخبار این هفته در حال نمایش هستند.')
            return Post.objects.filter(timeStamp__gte=timee, timeStamp__lte=datetime.now(), status='m').all()

        if postTime == 'this-month':
            timee = datetime.now() - timedelta(days=30)
            messages.info(self.request, 'اخبار این ماه در حال نمایش هستند.')
            return Post.objects.filter(timeStamp__gte=timee, timeStamp__lte=datetime.now(), status='m').all()

        if postTime == '3-month':
            timee = datetime.now() - timedelta(days=90)
            messages.info(self.request, 'اخبار سه ماه اخیر در حال نمایش هستند.')
            return Post.objects.filter(timeStamp__gte=timee, timeStamp__lte=datetime.now() , status='m').all()

        messages.info(self.request, 'فیلتر انتخاب شده معتبر نیست.')
        return Post.objects.get_m()


@login_required(login_url='/sign-in')
def like_post_page(request):
    if request.is_ajax():
        BlogID = request.GET.get('BlogID')
        likee: LikePost = LikePost.objects.filter(user_id=request.user.id, post_id=BlogID).first()
        if not likee:
            LikePost.objects.create(user_id=request.user.id, post_id=BlogID)
            count = LikePost.objects.filter(post_id=BlogID).count()
            return JsonResponse({'like':True, 'count':count})
        else:
            LikePost.objects.filter(user_id=request.user.id, post_id=BlogID).delete()
            count = LikePost.objects.filter(post_id=BlogID).count()
            return JsonResponse({'like':False, 'count':count})


@login_required(login_url='/sign-in')
def fav_post_page(request):
    if request.is_ajax():
        BlogID = request.GET.get('BlogID')
        favee: FavPost = FavPost.objects.filter(user_id=request.user.id, post_id=BlogID).first()
        if not favee:
            FavPost.objects.create(user_id=request.user.id, post_id=BlogID)
            return JsonResponse({'fav':True})
        else:
            FavPost.objects.filter(user_id=request.user.id, post_id=BlogID).delete()
            return JsonResponse({'fav':False})


class postListRecent(ListView):
    template_name = 'post_list.html'
    paginate_by = 4
    model = Post
    def get_context_data(self, ** kwargs):
        context = super().get_context_data(** kwargs)
        context['recents'] = Post.objects.filter(status='m').order_by('-id')[:8]
        context['hots'] = Post.objects.filter(status='m').order_by('-comments_count')[:8]
        context['pops'] = Post.objects.filter(status='m').order_by('-like_count')[:8]
        return context
    queryset = Post.objects.filter(status='m')[:9]

class postListPopular(ListView):
    template_name = 'post_list.html'
    paginate_by = 4
    model = Post
    def get_context_data(self, ** kwargs):
        context = super().get_context_data(** kwargs)
        context['recents'] = Post.objects.filter(status='m').order_by('-id')[:8]
        context['hots'] = Post.objects.filter(status='m').order_by('-comments_count')[:8]
        context['pops'] = Post.objects.filter(status='m').order_by('-like_count')[:8]
        return context
    queryset = Post.objects.filter(status='m').order_by('-like_count')[:9]

class postListMostViews(ListView):
    template_name = 'post_list.html'
    paginate_by = 4
    model = Post
    def get_context_data(self, ** kwargs):
        context = super().get_context_data(** kwargs)
        context['recents'] = Post.objects.filter(status='m').order_by('-id')[:8]
        context['hots'] = Post.objects.filter(status='m').order_by('-comments_count')[:8]
        context['pops'] = Post.objects.filter(status='m').order_by('-like_count')[:8]
        return context
    queryset = Post.objects.filter(status='m').order_by('-views')[:8]


class postListHot(ListView):
    template_name = 'post_list.html'
    paginate_by = 4
    model = Post
    def get_context_data(self, ** kwargs):
        context = super().get_context_data(** kwargs)
        context['recents'] = Post.objects.filter(status='m').order_by('-id')[:8]
        context['hots'] = Post.objects.filter(status='m').order_by('-comments_count')[:8]
        context['pops'] = Post.objects.filter(status='m').order_by('-like_count')[:8]
        return context
    queryset = Post.objects.filter(status='m').order_by('-comments_count')[:8]


def list_sidebar_adver_partial(request):
    advers = Advertising.objects.filter(timeStamp__lt=datetime.now() - timedelta(hours=12)).delete()
    advers = Advertising.objects.all().order_by('-id')[:3]
    context = {
        'advers': advers
    }
    return render(request, 'partials/sidebar_advers_list_post.html', context)

def reportComment(request, commentID, postID):
    post = Post.objects.get(id=postID)
    cmt = Comment.objects.get(id=commentID)
    cmt.pre_report = True
    cmt.save()
    messages.info(request, 'پیام با موفقیت گزارش شد.')
    return redirect(post.get_absolute_url())

def removeComment(request, commentID, postID):
    if not request.user.is_superuser:
        return redirect('/')
    post = Post.objects.get(id=postID)
    Comment.objects.filter(id=commentID).delete()
    messages.info(request, 'متن با موفقیت حذف شد.')
    return redirect(post.get_absolute_url())