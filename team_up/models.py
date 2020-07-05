from django.db import models
from django.contrib.auth.models import User
from accounts.models import extendeduser
# Create your models here.

class Teams(models.Model):
  category = models.CharField(max_length=100)
  relevant_url = models.URLField(default='Not Provided')
  pub_date = models.DateTimeField(null=True, blank=True)
  # team_id = models.AutoField()
  # votes_total = models.IntegerField(default=1)
  # image = models.ImageField(upload_to='images/')
  # icon = models.ImageField(upload_to='images/')
  short_description = models.TextField(default='Not Provided', max_length=200)
  description = models.TextField(default='Not Provided', max_length=2000)
  teammates = models.IntegerField(default=0)
  vacancy = models.IntegerField(default=1)
  logged_in_user = models.ForeignKey(extendeduser, on_delete=models.CASCADE)

  def __str__(self):
    return self.category

  # def summary(self):
  #   return self.body[:100]

  def pub_date_pretty(self):
    return self.pub_date.strftime('%b %e %Y')


# class Teams(models.Model):
#   teamup_id = models.ForeignKey(Teamup_recruitment_details, related_name='Teamup_recruitment_details', on_delete=models.CASCADE)