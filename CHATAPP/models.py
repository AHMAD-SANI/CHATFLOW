from django.db import models
from django.contrib.auth.models import User
import uuid
from io import BytesIO
from PIL import Image, ImageDraw
from django.core.files import File
import qrcode


class reset_password(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username


class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to='media/profile_images', default='/default_image/5856.jpg')
    fullname = models.CharField(max_length=50)
    phone = models.CharField(max_length=20, default=23480000000000)
    bio = models.TextField(default='Am using ChatFlow...')
    address = models.CharField(max_length=100, default='Address not updated.', null=True)

    
    def __str__(self):
        return self.fullname
    

    
class chatroom(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=100, blank=True, null=True)
    image = models.FileField(upload_to='group_avater/', blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    discription = models.TextField(blank=True, null=True)
    is_private = models.BooleanField(default=False)
    admin = models.ForeignKey(profile, on_delete=models.CASCADE, blank=True, null=True)
    members = models.ManyToManyField(profile, related_name='members')
    QR_code = models.FileField(upload_to='QR_codes/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    
    
    
def save(self, *args, **kwargs):
    image = qrcode.make(self.name).convert("RGB")

    canvas = Image.new('RGB', (290, 290), 'white')
    # CENTER the QR code
    img_w, img_h = image.size
    canvas_w, canvas_h = canvas.size

    box = (
        (canvas_w - img_w) // 2,
        (canvas_h - img_h) // 2,
        (canvas_w + img_w) // 2,
        (canvas_h + img_h) // 2,
    )

    canvas.paste(image, box)

    fname = f'QR_code-{self.name}.png'
    buffer = BytesIO()
    canvas.save(buffer, 'PNG')

    self.QR_code.save(fname, File(buffer), save=False)
    buffer.close()

    super().save(*args, **kwargs)

    
    
    
    
class chat_message(models.Model):
    user = models.ForeignKey(profile, on_delete=models.CASCADE, related_name='sender')
    chatroom = models.ForeignKey(chatroom, on_delete=models.CASCADE, related_name='chatroom')
    message = models.TextField()
    