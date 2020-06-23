from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class extendeduser(models.Model):
  user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
  first_name = models.CharField(max_length=255)
  last_name = models.CharField(max_length=255, default='')
  gender = models.CharField(max_length=255, blank=True, default='rather_not_say')
  email = models.EmailField(verbose_name='email', max_length=60, default='')
  about_me = models.TextField(max_length=1000, default="Let's Team-up!")
  portfolio = models.URLField(default='Not Provided')
  linkedin = models.URLField(default='Not Provided')
  facebook = models.URLField(default='Not Provided')
  twitter = models.URLField(default='Not Provided')
  other_url = models.URLField(default='Not Provided')
  city = models.CharField(max_length=255, default='')
  country = models.CharField(max_length=255, default='')
  phone = models.CharField(max_length=17, default='0000000000')
  date_joined = models.DateTimeField(verbose_name='date_joined', auto_now=True)
  last_login = models.DateTimeField(verbose_name='last_login', auto_now=True)
  is_admin = models.BooleanField(default=False)
  is_superuser = models.BooleanField(default=False)