from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class extendeduser(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  first_name = models.CharField(max_length=255, default='')
  last_name = models.CharField(max_length=255, default='')
  gender = models.CharField(max_length=255, blank=True, default='rather_not_say')
  email = models.EmailField(verbose_name='email', max_length=60, default='')
  about_me = models.TextField(max_length=1000, default='')
  portfolio = models.URLField(default='')
  linkedin = models.URLField(default='')
  fackebook = models.URLField(default='')
  twitter = models.URLField(default='')
  other_url = models.URLField(default='')
  dob = models.DateField(verbose_name=("Birthday"), null=True)
  city = models.CharField(default='', max_length=255)
  country = models.CharField(default='', max_length=255)
  phone = models.IntegerField(default=0000000000)
  date_joined = models.DateTimeField(verbose_name='date_joined', auto_now=True)
  last_login = models.DateTimeField(verbose_name='last_login', auto_now=True)
  is_admin = models.BooleanField(default=False)
  is_superuser = models.BooleanField(default=False)