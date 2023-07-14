from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'tabi'

urlpatterns = [
    path('',views.TopListView.as_view(),name='top_list'),
    path('mypage/',views.MypageList.as_view(),name='mypage_list'),
    path('detail/<int:pk>/',views.TabiDetail.as_view(),name='tabi_detail'),
    path('create/',views.TabiCreateView.as_view(),name='tabi_create'),
    path('update/<int:pk>/',views.TabiUpdateView.as_view(),name='tabi_update'),
    path('delete/<int:pk>/',views.TabiDelete.as_view(),name='tabi_delete'),
    path('mysave/',views.MysaveList.as_view(),name='mysave_list'),
    path('userdetail<int:pk>',views.UserDetail.as_view(),name='user_detail'),
    path('comment/<int:pk>/',views.CommentCreate.as_view(),name='comment_create'),
    path('sample/',views.sample,name='sample'),
    path('ot/',views.tabi_ot,name='tabi_ot'),
    path('pop/',views.PopListView.as_view(),name='pop_list'),
    path('day/',views.DayListView.as_view(),name='day_list'),
    path('week/',views.WeekListView.as_view(),name='week_list'),
    path('new/',views.NewListView.as_view(),name='new_list'),
    path('fam/',views.FamListView.as_view(),name='fam_list'),
    path('search/',views.SearchView.as_view(),name='search'),
    path('favo/<int:pk>/',views.FavoritePost,name='favo'),
    path('like-home/<int:pk>/',views.LikeHome.as_view(), name='like-home'),
    path('like-detail/<int:pk>/',views.LikeDetail.as_view(), name='like-detail'),
    path('<slug:username>/profile',views.ProfileDetail.as_view(),name='profile'),
    path('<slug:username>/follow', views.follow_view, name='follow'),
    path('<slug:username>/unfollow', views.unfollow_view, name='unfollow'),
    path('follow-home/<int:pk>', views.FollowHome.as_view(), name='follow-home'),
    path('follow-detail/<int:pk>', views.FollowDetail.as_view(), name='follow-detail'),
    path('follow-list/', views.FollowList.as_view(), name='follow-list'),
    path('comment/create/<int:pk>/', views.CommentCreate.as_view(), name='comment_create'),
    path('hokkaido/',views.HokkaidoListView.as_view(),name='hokkaido_list'),
    path('tokyo/',views.TokyoListView.as_view(),name='tokyo_list'),
    path('osaka/',views.OsakaListView.as_view(),name='osaka_list'),
    path('kyoto/',views.KyotoListView.as_view(),name='kyoto_list'),
    path('fukuoka/',views.FukuokaListView.as_view(),name='fukuoka_list'),
    path('okinawa/',views.OkinawaListView.as_view(),name='okinawa_list'),
]