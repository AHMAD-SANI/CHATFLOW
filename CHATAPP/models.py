from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
import uuid


class reset_password(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Use BigAutoField for numeric primary key to match DB bigint columns
    id = models.BigAutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username


class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = CloudinaryField('profile_images', default='https://res.cloudinary.com/dcgfrztgw/image/upload/v1772501764/5856_olh7ta.jpg')
    fullname = models.CharField(max_length=50)
    phone = models.CharField(max_length=20, default=23480000000000)
    bio = models.TextField(default='Am using ChatFlow...')
    address = models.CharField(max_length=100, default='Address not updated.', null=True)
    
    def __str__(self):
        return self.fullname
    

    
class chatroom(models.Model):
    # Use BigAutoField to match the existing DB column type (bigint).
    # The database currently has `id` as bigint which caused a failure
    # when the model tried to insert a UUID string into that column.
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    image = CloudinaryField('group_avater', blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    description = models.TextField(db_column='dicription', blank=True, null=True)
    is_private = models.BooleanField(default=False)
    admin = models.ForeignKey(profile, on_delete=models.CASCADE, blank=True, null=True)
    members = models.ManyToManyField(profile, related_name='members')
    QR_code = models.FileField(upload_to='QR_codes/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    
class chat_message(models.Model):
    user = models.ForeignKey(profile, on_delete=models.CASCADE, related_name='sender')
    chatroom = models.ForeignKey(chatroom, on_delete=models.CASCADE, related_name='chatroom')
    message = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    