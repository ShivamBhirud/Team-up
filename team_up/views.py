from django.shortcuts import render, redirect, get_object_or_404
from team_up.models import Teams, Recruited_Teammates
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.models import Extendeduser



def home(request):
  # profile = UserProfile.objects
  return render(request, 'team_up/home.html')

@login_required(login_url="/accounts/login")
def create_t_up(request):
  if request.method == 'POST':
    if request.POST['category'] and request.POST['short_description'] and request.POST['description'] and request.POST['vacancy']:
      # Setup Teams table's fields
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
      teams.logged_in_user = request.user.extendeduser
      teams.save()
      # Setup Recruited_Teammates table's fields
      recruited_teammates = Recruited_Teammates()
      recruited_teammates.teamup_advertisement = Teams.objects.get(id=teams.id)
      recruited_teammates.save()
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


# TODO- limit the teammates according to the provided vacancy
def joined_tups(request):
  recruiter = request.POST['recruiter'] 
  print(recruiter)
  print('\n\n')
  adv_card = Teams.objects.filter(id=recruiter)

  for team in adv_card:
    print(team.logged_in_user) # clicked teamup advertisement card owner
    print('\n\n')
  print("adv_card[0].id = " + str(adv_card[0].id))

  # Adding teammates to a teamup advertisement ---------------->>>>>
  rt = Recruited_Teammates(teamup_advertisement_id=adv_card[0].id)
  # rt = Recruited_Teammates.objects.all()
  print(request.user)
  print('printing ID:\n')
  print(rt.id)
  rt.teammates = Extendeduser(user=request.user)
  print(rt.teammates.user)
  rt.save()
  # ------------- Added------------>>>>>>>>>>>

  # print(rt.teammates)
  # data = Extendeduser.objects.filter(user_id=recruiter)
  # data = get_object_or_404(User, pk=recruiter)
  # data = User.objects.filter(username=request.user)

  # print(request.user) # current user i.e t50 logged in
  
  # return render(request, 'team_up/tup_groups.html', {'teams': data})
  # return render(request, 'accounts/user_profile.html', {'data':data})
  return render(request, 'team_up/coming_up_soon.html')

'''
  #---------------HOW TO FETCH ALL TEAMMATES FOR A SINGLE RECRUITMENT CARD?--------->>>>>>
  rt = Recruited_Teammates.objects.filter(teamup_advertisement_id=adv_card[0].id)
  for i in rt:
    print('printing all temmates:\n')
    print(i.teammates)

  #----------------------------------END--------------------->>>>>>>
'''