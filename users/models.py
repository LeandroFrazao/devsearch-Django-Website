from email.policy import default
from django.db import models
from django.contrib.auth.models import User
import uuid
from uuid import uuid4
from django.conf import settings
import os

# Create your models here.

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/profile/<filename>
    return 'user_{0}/profile/{1}'.format(instance.user.id, filename)

class Profile(models.Model): 

    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.OneToOneField(User, on_delete = models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=500, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    
    short_intro = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField( null=True, blank=True)
    profile_image = models.ImageField(null=True, blank=True,upload_to= user_directory_path,  default="images/user-default.png")
    social_github = models.CharField(max_length=200, null=True, blank=True)
    social_twitter = models.CharField(max_length=200, null=True, blank=True)
    social_linkedin = models.CharField(max_length=200, null=True, blank=True)
    social_youtube = models.CharField(max_length=200, null=True, blank=True)
    social_website = models.CharField(max_length=200, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str( self.username)

    class Meta:
        ordering = ['created']

    
    @property
    def imageURL(self):
        try:
            url = self.profile_image.url
        except:
            if os.getcwd()== '/app' or settings.DEFAULT_FILE_STORAGE=='cloudinary_storage.storage.MediaCloudinaryStorage':
                url = 	"http://res.cloudinary.com/"+settings.CLOUDINARY_STORAGE.get('CLOUD_NAME')+"/images/"+"user-default.png"
            else:        
                url = settings.MEDIA_URL+"user-default.png"
        return url


class Skill(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    #uuid = models.CharField(max_length=200, primary_key=True)
    #uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    owner = models.ForeignKey(Profile, on_delete = models.CASCADE, null = True, blank = True)
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField( null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return str( self.name)


class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null = True, blank=True)
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null = True, blank=True, related_name="messages")
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=500, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField( )
    is_read = models.BooleanField( default=False, null=True)

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str( self.subject)

    class Meta:
        ordering = ['is_read', '-created']
