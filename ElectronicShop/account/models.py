from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# For Signal--------------------------------------------------
from django.db.models.signals import post_save
from django.dispatch import receiver

# For Email---------------------------------------------------
import uuid
from .utils import send_account_activation_email


# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="users")

    # Login Email Verification --------------------------------------
    email_token = models.CharField(max_length=200, default=0)
    is_email_verified = models.BooleanField(default=False)

    # Forget Password------------------------------------------------
    otp = models.IntegerField(default=0)

    gen = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    )
    pro_pic = models.ImageField(default='default_pic.jpg', upload_to="ProfilePic")
    Cov_pic = models.ImageField(default='default_cover.jpg', upload_to="ProfilePic")
    gender = models.CharField(max_length=20, choices=gen, null=True, blank=True)
    date_of_birth = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(max_length=200, null=True, blank=True)
    otp = models.IntegerField(default=0000, null=True, blank=True)

    def __str__(self):
        return str(self.user)

    # Siglar -----------------------------------------------------------------
    # def create_profile(sender, **kwargs):
    #     if kwargs['created']:
    #         user_profile = Profile.objects.create(user=kwargs['instance'])
    #
    # post_save.connect(create_profile, sender=User)

    @receiver(post_save, sender=User)
    def send_email_token(sender, instance, created, **kwargs):
        try:
            if created:
                email_token = str(uuid.uuid4())
                pro_obj = Profile.objects.create(user=instance, email_token=email_token)
                pro_obj.save()
                email = instance.email
                send_account_activation_email(email, email_token)

        except Exception as e:
            print(e)


class multi_address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    Division = models.CharField(max_length=50, null=True, blank=True)
    Sub_division = models.CharField(max_length=50, null=True, blank=True)
    Zipcode = models.CharField(max_length=50, null=True, blank=True)
    Delivery_Address = models.CharField(max_length=50, null=True, blank=True)
    Phone = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.Delivery_Address + self.Sub_division + self.Division
