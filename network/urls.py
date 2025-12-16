
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("post/create/", views.create_post, name="create_post"),
    path("comment/<int:post_id>", views.create_comment, name="create_comment"),
    path("profile/update/", views.update_profile, name="update_profile"),
    path("profile/photo/delete/", views.delete_profile_photo, name="delete_profile_photo"),
    path("profile/", views.user_profile, name="user_profile"),
    path("profile/<str:username>/", views.profile_view, name="profile"),
    path("profile/<str:username>/toggle-follow/", views.toggle_follow, name="toggle_follow"),
    path("following/", views.following_view, name="following"),
    path("post/<int:post_id>/update/", views.update_post, name="update_post"),
    path("post/<int:post_id>/like/", views.toggle_like, name="toggle_like"),
    path("post/detail/<int:post_id>/", views.post_details, name="post_details"),
    path("post/<int:post_id>/delete/", views.delete_post, name="delete"),
    path("post/search/", views.search, name="search"),
    path("post/<str:category>/", views.category_view, name="category_view"),
    path("comment/<int:comment_id>/like/", views.toggle_comment_like, name="toggle_comment_like"),
    path('post/<int:post_id>/track/', views.track_engagement, name='track_engagement')
]
