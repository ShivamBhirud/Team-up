from django.shortcuts import render, redirect, get_object_or_404
from team_up.models import Teams, RecruitedTeammates
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.models import Extendeduser
from .models import ApplicationStatus



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
      # Setup RecruitedTeammates table's fields
      recruited_teammates = RecruitedTeammates()
      recruited_teammates.teamup_advertisement = Teams.objects.get(id=teams.id)
      recruited_teammates.teammates = Extendeduser.objects.get(user=request.user)
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
  return render(request, 'team_up/tup_groups.html', {'teams': teams})

@login_required(login_url="/accounts/login")
def other(request):
  teams = Teams.objects.filter(category='Other').order_by('pub_date')
  return render(request, 'team_up/tup_groups.html', {'teams': teams})

@login_required(login_url="/accounts/login")
def sports(request):
  teams = Teams.objects.filter(category='Sports').order_by('pub_date')
  print('Printing sports')
  for team in teams:
    print(team.logged_in_user)
  return render(request, 'team_up/tup_groups.html', {'teams': teams})

@login_required(login_url="/accounts/login")
def gaming(request):
  teams = Teams.objects.filter(category='Gaming').order_by('pub_date')
  return render(request, 'team_up/tup_groups.html', {'teams': teams})

@login_required(login_url="/accounts/login")
def household_chores(request):
  teams = Teams.objects.filter(category='Household Chores').order_by('pub_date')
  return render(request, 'team_up/tup_groups.html', {'teams': teams})

# Show Details of a Teamup Advertisement to the user
def show_teamup_details(request):
  recruiter = request.POST['teamup_details'] 
  print(recruiter)
  print('\n\n')
  adv_card = Teams.objects.filter(id=recruiter)

  for team in adv_card:
    print(team.logged_in_user.user) # clicked teamup advertisement card owner
    print('\n\n')
  print("adv_card[0].id = " + str(adv_card[0].id))
  print('printing vacancy')
  print(adv_card[0].vacancy)

  counting_teammates = RecruitedTeammates.objects.filter(teamup_advertisement_id=adv_card[0].id)
  teammates_list = []
  total_teammates_count = 0
  for teammate in counting_teammates:
    teammates_list.append(str(teammate.teammates.user))
    total_teammates_count += 1
    print(teammate.teammates.user)
    
  # print(request.user_id)
  print(teammates_list)

  return render(request, 'team_up/details.html', {'teams': adv_card[0], 'teammates': counting_teammates})

  # Add a user to the Teamup
def join_tup(request):
  recruiter = request.POST['recruiter'] 
  print(recruiter)
  print('\n\n')
  adv_card = Teams.objects.filter(id=recruiter)

  for team in adv_card:
    print(team.logged_in_user.user) # clicked teamup advertisement card owner
    print('\n\n')
  print("adv_card[0].id = " + str(adv_card[0].id))
  print('printing vacancy')
  print(adv_card[0].vacancy)

  # New code started for notification----->>>>>>>
  pre_existing_requester = ApplicationStatus.objects.filter(logged_in_user=adv_card[0].logged_in_user.user,
  requester=request.user,teamup_advertisement=adv_card[0].id,status='P')
  if pre_existing_requester:
    pass
  else:
    application_status = ApplicationStatus()
    application_status.logged_in_user = adv_card[0].logged_in_user.user
    application_status.requester = request.user
    application_status.teamup_advertisement = adv_card[0].id
    application_status.status = 'P'
    application_status.date = timezone.datetime.now()
    application_status.save()
  # New code end------------>>>>>>>

  print("REQUEST SENT TO THE OWNER!")
  # IMPORTANT CODE TO ADD THE TEMMATE------------>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  # # Adding teammates to a teamup advertisement ---------------->>>>>
  # rt = RecruitedTeammates(teamup_advertisement_id=adv_card[0].id)
  # print('printing teammates')
  # # Counting existing teammates for a teamup advertisement---->>>
  # counting_teammates = RecruitedTeammates.objects.filter(teamup_advertisement_id=adv_card[0].id)
  # teammates_list = []
  # total_teammates_count = 0
  # for teammate in counting_teammates:
  #   teammates_list.append(str(teammate.teammates.user))
  #   total_teammates_count += 1
  #   print(teammate.teammates.user)
    
  # # print(request.user_id)
  # print(teammates_list)
  # if(total_teammates_count <= adv_card[0].vacancy + 1 and str(request.user) not in teammates_list):
  #   print('teammate added')
  #   rt.teammates = Extendeduser(user=request.user)
  #   rt.save()
  # else:
  #   print('teammate already exited!')
  # print(request.user)
  
  # ------------- Added------------>>>>>>>>>>>
  # IMPORTANT CODE TO ADD TEAMMATE ENDS HERE------------------------->>>>>>>>>>>>>>>>>>>>>>>

  
  # return render(request, 'team_up/tup_groups.html', {'teams': data})
  # return render(request, 'accounts/user_profile.html', {'data':data})
  return render(request, 'team_up/coming_up_soon.html')

  # counting_teammates = RecruitedTeammates.objects.filter(teamup_advertisement_id=adv_card[0].id)
  # return render(request, 'team_up/details.html', {'teams': adv_card[0], 'teammates': counting_teammates})

'''
  #---------------HOW TO FETCH ALL TEAMMATES FOR A SINGLE RECRUITMENT CARD?--------->>>>>>
  rt = RecruitedTeammates.objects.filter(teamup_advertisement_id=adv_card[0].id)
  for i in rt:
    print('printing all temmates:\n')
    print(i.teammates)

  #----------------------------------END--------------------->>>>>>>
'''

def notifications(request):
  application_status = ApplicationStatus.objects.filter(logged_in_user=request.user, status='P').order_by('date')
  return render(request, 'team_up/notifications.html', {'notifications': application_status})

