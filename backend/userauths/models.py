from django.db import models
from django.contrib.auth.models import AbstractUser 
# this is user from django
#from django.contrib.auth.models import User


from django.db.models.signals import post_save

class User(AbstractUser):
    username = models.CharField(unique=True, max_length=100)
    email = models.EmailField(unique=True)
    full_name = models.CharField(unique=True, max_length=100)
    # i included for now but this will be removed later as we dont gonna use this feature in future
    otp = models.CharField(max_length=100, null=True, blank=True)
    USERNAME_FIELD = 'email'  # for logging in
    REQUIRED_FIELDS = ['username'] # for creating the account

    def __str__(self):
        return self.email
    
    #overwrite the default save function
    def save(self, *args, **kwargs):
        email_username, full_name = self.email.split("@") #nihar@test.com     this will split full name to nihar
        if self.full_name == "" or self.full_name == None:
            self.full_name == email_username
        if self.username == "" or self.username == None:
            self.username = email_username
        super(User, self).save(*args, **kwargs)

# understand why we need this, ask vanadana
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to="user_folder", default="default-user.jpg", null=True, blank=True)
    full_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.full_name:
            return str(self.full_name)
        else:
            return str(self.user.full_name)
    
    def save(self, *args, **kwargs):
        if self.full_name == "" or self.full_name == None:
            self.full_name == self.user.username
        super(Profile, self).save(*args, **kwargs)
    



#  this is for creating a profile everytime a new user is created
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)




