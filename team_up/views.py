from django.shortcuts import render
# from accounts.models import UserProfile
# Create your views here.
def home(request):
  # profile = UserProfile.objects
  return render(request, 'team_up/home.html')