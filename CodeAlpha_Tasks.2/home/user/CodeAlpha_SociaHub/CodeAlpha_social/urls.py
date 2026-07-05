from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("profile/<str:username>/", views.profile_view, name="profile"),
    
    path("post/create/", views.post_create, name="post_create"),
    path("post/<int:post_id>/edit/", views.post_edit, name="post_edit"),
    path("post/<int:post_id>/delete/", views.post_delete, name="post_delete"),

    path("post/<int:post_id>/comment/", views.add_comment, name="add_comment"),
    path("comment/<int:comment_id>/delete/", views.delete_comment, name="delete_comment"),

    path("post/<int:post_id>/like/", views.toggle_like, name="toggle_like"),
    path("follow/<str:username>/", views.toggle_follow, name="toggle_follow"),
]