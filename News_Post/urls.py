from django.urls import path
from . import views

app_name = 'post'
urlpatterns = [
    path('post/list/', views.PostList.as_view(), name='list'),
    path('post/detail/<int:postID>/<str:postTITLE>', views.post_detail, name='detail'),
    path('post/search/', views.searchPost.as_view(), name='search'),
    path('post/tag/<str:tagTitle>', views.searchPostTag.as_view(), name='tag'),
    path('post/category/<str:CategoryTitle>', views.searchPostCateGory.as_view(), name='category'),
    # path('post/specific/', views.postSpecific.as_view(), name='postSpecific'),      #asdfasdfasfa
    path('post/many/<int:Many>', views.postMany.as_view(), name='many'),
    path('post/time/<str:postTime>', views.postTime.as_view(), name='time'),
    path('post/comments/report/<int:commentID>/<int:postID>', views.reportComment, name='reportComment'),
    path('post/comments/remove/<int:commentID>/<int:postID>', views.removeComment, name='removeComment'),
    path('post/like', views.like_post_page, name='like'),
    path('post/fav', views.fav_post_page, name='fav'),
    path('post/recent', views.postListRecent.as_view(), name='recent'),
    path('post/most-views', views.postListMostViews.as_view(), name='mostviews'),
    path('post/popular', views.postListPopular.as_view(), name='popular'),
    path('post/hot', views.postListHot.as_view(), name='hot'),

    # Partials
    path('post/list/sidebar/list/partial', views.sidebar_list_partial),
]