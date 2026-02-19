from django.urls import path
from .views import *

urlpatterns = [
    path('login', login_view, name='login'),
    path('register', register, name='register'),
    path('logout', logout_view, name='logout'),
    path('forgot_password', forgot_password_view, name='forgot_password'),
    path('email_sent', email_sent_view, name='email_sent'),
    path('reset_password/<str:reset_id>', reset_password_view, name='reset_password'),
    path('delete_my_account', delete_my_account, name='delete_my_account'),
    path('profile', profiles, name='profile'),
    path('', home, name='home'),
    path('chat/<str:chatroom_id>', index, name='chatroom'),
    path('privatechat', privatechat, name='privatechat'),
    path('create_group', create_group, name='create_group'),
    path('groups/<str:id>', group_detail, name='group_detail'),
    path('failed', failed, name='failed'),
    path('delete_group/<str:group_id>', delete_group, name='delete_group'),
    path('remove_user_from_group/<str:group_id>/<int:user_id>', remove_user_from_group, name='remove_user_from_group'),
    
]