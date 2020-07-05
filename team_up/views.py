from django.shortcuts import render, redirect, get_object_or_404
from team_up.models import Teams
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.models import extendeduser


def home(request):
  # profile = UserProfile.objects
  return render(request, 'team_up/home.html')

@login_required(login_url="/accounts/login")
def create_t_up(request):
  if request.method == 'POST':
    if request.POST['category'] and request.POST['short_description'] and request.POST['description'] and request.POST['vacancy']:
      teams = Teams()
      teams.category = request.POST.get('category', False)
      teams.short_description = request.POST['short_description']
      teams.description = request.POST['description']
      teams.vacancy = request.POST['vacancy']
      if request.POST['relevant_url']:
        if request.POST['relevant_url'].startswith('http://') or request.POST['relevant_url'].startswith('https://'):
          teams.relevant_url = request.POST['relevant_url']
        else:
          teams.relevant_url = 'https://' + request.POST['relevant_url']
      else:
        teams.relevant_url = teams.relevant_url
      teams.pub_date = timezone.datetime.now()
      teams.logged_in_user = request.user
      teams.save()
      return redirect('/team_up/' + str(teams.id))
    else:
      return render(request, 'team_up/create_t_up.html', {'error':'All astrisk marked (*) fields are required!'})
  else:
    return render(request, 'team_up/create_t_up.html')

def detail(request, team_up_id):
  #TODO add a page where all his created t-ups are visible to the user
  teamup = get_object_or_404(Teams, pk=team_up_id)
  return render(request, 'team_up/details.html', {'teams':teamup})

# Functions to handle the functionlity of all the Team-up groups
# TODO add other team-up groups as well

@login_required(login_url="/accounts/login")
def technology(request):
  teams = Teams.objects.filter(category='Technology').order_by('pub_date')
  for team in teams:
    print(team.logged_in_user)
  return render(request, 'team_up/tup_groups.html', {'teams': teams})

def joined_tups(request):
  recruiter = request.POST['recruiter'] 
  print(recruiter)
  print('\n\n')
  # data = request.
  # return render(request, 'team_up/home.html')
  data = Teams.objects.filter(logged_in_user=recruiter)
  # for data in data:
  #   print(data)
  # data = request.logged_in_user.get(recruiter)  
  for team in data:
    print(team.vacancy)
  
  # data = extendeduser.objects.filter(user_id=recruiter)
  # data = get_object_or_404(User, pk=recruiter)
  # data = User.objects.filter(username=request.user)
  print(request.user)
  # return render(request, 'team_up/tup_groups.html', {'teams': data})
  # return render(request, 'accounts/user_profile.html', {'data':data})
  return render(request, 'team_up/coming_up_soon.html')

