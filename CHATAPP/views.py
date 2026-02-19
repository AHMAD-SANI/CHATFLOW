from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import profile
from .models import *
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from django.core.mail import EmailMessage
from django.conf import settings
import datetime
from django.template.loader import render_to_string



def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        print('data ost successfully')
        if password == confirm_password:
            print('password and confirm password match')
            if User.objects.filter(email=email).exists():
                messages.error(request, 'the email already taken.')
                print('email unavailable')
            else:
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'the username already taken')
                    print('username unvailable')
                else:
                    print('the email provided is available.')
                    print('username available')
                    password_hash = set
                    obj_user = User.objects.create_user(username=username, email=email, password=password)
                    obj_user.save()
                    print('user is created succefully')
                    login(request, obj_user)
                    
                    profiles = profile.objects.create(user=obj_user, fullname=username)
                    profiles.save
                    print('login the user')
                    
                    # send welcoming email.
                    data = render_to_string('welcome_email.html', {
                        'profile' : profiles
                    })
                    
                    email_obj = EmailMessage(
                        'Welcome Abroad...',
                        data,
                        settings.EMAIL_HOST_USER,
                        [email]
                        
                    )
                    
                    email_obj.fail_silently = True
                    email_obj.content_subtype = 'html'
                    email_obj.send()
                    
                    
                    return redirect('/profile') 
        messages.error(request, "password does'nt match.")
        
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        print(password)
        user = authenticate(request, username=username, password=password)
        print(user)
        if user:
            login(request, user)
            return redirect('/profile')
        messages.error(request, 'Invalid credencails.')
    return render(request, 'login.html')


@login_required(login_url='/login')
def logout_view(request):
    user = request.user
    logout(request)
    return redirect('/login')


@login_required(login_url='/login')
def delete_my_account(request):
    username = request.user.username
    user = User.objects.get(username=username)
    user.delete()
    return redirect('/register')



def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            if user is not None:
                prevous_reset_obj = reset_password.objects.filter(user=user)
                if prevous_reset_obj:
                    prevous_reset_obj.delete()
                forgot_password_obj = reset_password.objects.create(user=user)
                forgot_password_obj.save()
                username = user.username
                reset_link = reverse('reset_password', kwargs={'reset_id':forgot_password_obj.id})
                html_email_file = render_to_string(
                    'email.html',
                    {
                        'name': username,
                        'link' : reset_link
                    }
                )
                        
                email_message = EmailMessage(
                    'Reset your password', # email subject
                    html_email_file,
                    settings.EMAIL_HOST_USER, # email sender
                    [email] # email  receiver 
                )
                email_message.fail_silently = False
                email_message.content_subtype = 'html'
                email_message.send()
                return redirect('/email_sent')
        except:
            messages.error(request, 'Invalid email address.')

    return render(request, 'forgot_password.html')


def email_sent_view(request):
    return render(request, 'email_sent.html')


def reset_password_view(request, reset_id):
    try:
        reset_valid = reset_password.objects.get(id=reset_id)
        if request.method == 'POST':
            password = request.POST['password'] 
            confirmPassword = request.POST['confirmPassword'] 
            user_have_isssue = False
            
            if password != confirmPassword:
                user_have_isssue = True
                messages.error(request, 'Password doesnt macth.')
                return redirect(f'/reset_password/{reset_id}')
            
            session_expired = reset_valid.created + timedelta(minutes=10)
            print(session_expired)
            if timezone.now() > session_expired:
                user_have_isssue = True
                messages.error(request, 'the link has expired create again.')
                return redirect('/forgot_password')
            
            if len(password) < 5:
                user_have_isssue = True
                messages.error(request, 'weak password less than 5 characters.')
                return redirect(f'/reset_password/{reset_id}')
            
            if user_have_isssue == False:
                user = reset_valid.user
                user.set_password(password)
                user.save()
                messages.success(request, 'you have reset your password login now.')
                return redirect('/login')
                
                
        return render(request, 'password_reset.html')
    except:
        messages.error(request, 'you have provide an invalid reset url')
        return redirect('/forgot_password')


@login_required(login_url='/login')
def profiles(request):
    user = request.user
    profile_obj = profile.objects.get(user=user)
    user_groups = chatroom.objects.filter(admin=profile_obj)
    if request.method == 'POST':
        profile_image = request.FILES.get('profile_image')
        username = request.POST['username']
        email = request.POST['email']
        address = request.POST['address']
        bio = request.POST['bio']
        phone = request.POST['phone']
        print(profile_image)
        if profile_image is not None:
            print('saving the image update')
            print(profile_image)
            profile_obj.image = profile_image
            profile_obj.address = address
            profile_obj.bio = bio
            profile_obj.fullname = username
            profile_obj.save()
            
        elif profile_image is None:
            profile_obj.fullname = username
            profile_obj.address = address
            profile_obj.bio = bio
            profile_obj.phone = phone
            print('saving the instance')
            profile_obj.save()
            print('saved successfully')
        
    
    context = {
        'profile': profile_obj,
        'user_groups': user_groups,
    }
    return render(request, 'profile.html', context=context)



@login_required(login_url='/login')
def create_group(request):
    users = User.objects.all()
    if request.method == 'POST':
        group_name = request.POST['group_name']
        group_bio = request.POST['group_bio']
        group_image = request.FILES.get('image')
        group_description = request.POST['description']
        user = request.user
        group_admin = profile.objects.get(user=user)
        
        create_group = chatroom.objects.create(
                                               name=group_name, 
                                               image=group_image, 
                                               about=group_bio, 
                                               discription=group_description, 
                                               admin=group_admin
                                               )
        create_group.members.add(group_admin)
        create_group.save()
        
        context = {
            'users': users,
        }
        return redirect(f'/groups/{create_group.id}', context=context)
    
    
    context = {
        'users': users,
    }
    return render(request, 'create_group.html', context=context)


@login_required(login_url='/login')
def group_detail(request, id):
    try:
        chatroom_obj = chatroom.objects.get(id=id)
        if request.user == chatroom_obj.admin.user:
            members_count= chatroom_obj.members.all().count()
            group_url = reverse('group_detail', kwargs={'id': id})
            print(group_url)
            context = {
                'chatroom': chatroom_obj,
                'members_count' : members_count,
                'group_url': group_url,
            }
            return render(request, 'group_admin.html', context=context)
        else:
            user = request.user
            user_profile = profile.objects.get(user=user)
            if chatroom_obj.members.filter(id=user_profile.id).exists():
                print('the user inthe member list')
                members_count = chatroom_obj.members.all().count()
                group_url = reverse('group_detail', kwargs={'id': id})
                print(group_url)
                context = {
                    'chatroom': chatroom_obj,
                    'members_count' : members_count,
                    'group_url': group_url,
                }
                return render(request, 'group_detail.html', context=context )
            else:
                chatroom_obj.members.add(user_profile)
                return redirect(f'/groups/{id}')
                
            
    except:
        return redirect('/failed')
    


@login_required(login_url='/login')
def failed(request):
    return render(request, 'denied.html')

@login_required(login_url='/login')
def remove_user_from_group(request, group_id, user_id):
    try:
        user_obj = User.objects.get(id=user_id)
        profile_obj = profile.objects.get(user=user_obj)
        group = chatroom.objects.get(id=group_id)
        print(profile_obj)
        print(group)
        user = request.user
        admin_profile = profile.objects.get(user=user)
        print(admin_profile)
        if admin_profile == group.admin:
            group.members.remove(profile_obj)
            return redirect(f'/groups/{group_id}')
        else:
            profile_obj = profile.objects.get(user=request.user)
            group.members.remove(profile_obj)
            return redirect('/')
    except:
        return render(request, 'denied.html')
        
    
    
@login_required(login_url='/login')
def delete_group(request, group_id):
    group_obj = chatroom.objects.get(id=group_id)
    admin_profile = profile.objects.get(user=request.user)
    if admin_profile == group_obj.admin:
        group_obj.delete()
        return redirect('/profile')
    else:
        return redirect('/')



@login_required(login_url='/login')
def index(request, chatroom_id):
    user = request.user
    user_profile = profile.objects.get(user=user)
    my_chatrooms = chatroom.objects.filter(members=user_profile)
    current_group = chatroom.objects.get(id=chatroom_id)
    chat_messages = chat_message.objects.filter(chatroom=current_group)
    if request.method == 'POST':
        message_body = request.POST['message_body']
        chat_message.objects.create(user=user_profile, message=message_body, chatroom=current_group)
        return redirect(f'/chat/{chatroom_id}')
    context = {
        'profile': user_profile,
        'user': request.user.username,
        'chatrooms' : my_chatrooms,
        'room_id' : chatroom_id,
        'current_group': current_group,
        'chat_message' : chat_messages,
    }
    return render(request, 'index.html', context=context)


@login_required(login_url='/login')
def home(request):
    user = request.user
    user_profile = profile.objects.get(user=user)
    my_chatrooms = chatroom.objects.filter(members=user_profile)
    print(my_chatrooms)
    context = {
        'profile': user_profile,
        'chatrooms' : my_chatrooms,
    }
    return render(request, 'home.html', context=context)


@login_required(login_url='/login')
def privatechat(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = request.user
        user_profile = profile.objects.get(user=user)
        try:
            chat_member = User.objects.get(email=email)
            chat_member_profile = profile.objects.get(user=chat_member)
            my_group = chatroom.objects.filter(members=user_profile).filter(members=chat_member_profile).first()
            if my_group is not None:
                return redirect(f'/chat/{my_group.id}')
            else:
                chatroom_obj = chatroom.objects.create(is_private=True)
                chatroom_obj.save()   # must save before ManyToMany
                chatroom_obj.members.add(user_profile, chat_member_profile)

                    
                return redirect(f'/chat/{chatroom_obj.id}')
        except User.DoesNotExist:
            messages.error(request, 'The email user doesnot exist in the database')
            return redirect('/')
            