from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.log_and_reg),
    path('register', views.register),
    path('login', views.login),
    path('index', views.index), 
    path('logout', views.logout),
    path('wall', views.wall),
    path('post_message', views.post_message),
    path('messages/<int:message_id>/post_comment', views.post_comment),
    path('users/<int:user_id>', views.user),
    path('messages/<int:message_id>/like', views.like), 
    path('messages/<int:message_id>/unlike', views.unlike),
    path('messages/<int:message_id>/edit_messsage', views.edit_message),
    path('messages/<int:message_id>/update', views.update),
    path('users/<int:user_id>/update', views.update_user),

]
