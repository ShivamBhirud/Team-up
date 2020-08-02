from django.shortcuts import render, redirect, get_object_or_404
from team_up.models import Teams, RecruitedTeammates
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.models import Extendeduser
from .models import ApplicationStatus
from django.views.decorators.cache import cache_control


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
  return render(request, 'team_up/details.html', {'teams':teamup, 'owner':request.user})

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
  if(adv_card[0].logged_in_user.user == request.user):
    owner = 1
  else:
    owner = 0
  # print(request.user_id)
  print(teammates_list)

  return render(request, 'team_up/details.html', {'teams': adv_card[0], 'teammates': counting_teammates, 'owner':owner})

  # Add a user to the Teamup
def join_tup(request, recruiter):
  # breakpoint() 
  print(recruiter)
  print('\n\n')
  adv_card = Teams.objects.filter(id=recruiter)

  for team in adv_card:
    print(team.logged_in_user.user) # clicked teamup advertisement card owner
    print('\n\n')
  print("adv_card[0].id = " + str(adv_card[0].id))
  print('printing vacancy')
  print(adv_card[0].vacancy)
  print(request.user.id)
  # New code started for notification----->>>>>>>
  pre_existing_requester = ApplicationStatus.objects.filter(logged_in_user=Extendeduser.objects.get(user=adv_card[0].logged_in_user.user).user_id,
  requester=request.user.id, teamup_advertisement=adv_card[0].id)
  # print(pre_existing_requester)
  counting_teammates = RecruitedTeammates.objects.filter(teamup_advertisement_id=adv_card[0].id)
  teammates_list = []
  total_teammates_count = 0
  for teammate in counting_teammates:
    teammates_list.append(str(teammate.teammates.user))
    total_teammates_count += 1
    print(teammate.teammates.user)
    
  # print(request.user_id)
  print(teammates_list)
  print(request.user)
  # Don't send request if user has pending request, vacancy fulfilled, or user is already accepted 
  if(pre_existing_requester or total_teammates_count >= adv_card[0].vacancy + 1 or
   str(request.user) in teammates_list):
    pass
  else:
    application_status = ApplicationStatus()
    print(adv_card[0].logged_in_user.user)
    # application_status.logged_in_user = adv_card[0].logged_in_user.user
    id = Extendeduser.objects.get(user=adv_card[0].logged_in_user.user)
    print(id.user_id)
    application_status.logged_in_user = id.user_id
    # application_status.requester = request.user
    id = Extendeduser.objects.get(user=request.user)
    print(id.user_id)
    application_status.requester = id.user_id
    print("Printing IMP")
    print(application_status.logged_in_user)
    print(application_status.requester)
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

def requests(request):
  id = Extendeduser.objects.get(user=request.user)
  # print(id.user_id)
  application_status = ApplicationStatus.objects.filter(logged_in_user=id.user_id, status='P').order_by('date')
  if(application_status):
    requester = Extendeduser.objects.get(user=application_status[0].requester)
    advertisement = Teams.objects.get(id=application_status[0].teamup_advertisement)
    return render(request, 'team_up/requests.html', {'notifications': application_status,
    'requester':requester.first_name, 'advertisement':advertisement.short_description})
  else:
    return render(request, 'team_up/requests.html', {'notifications': application_status})

# TODO Notification not working as expected.The ower gets notified even if the temmate is removed
def notifications(request):
  id = Extendeduser.objects.get(user=request.user)
  print(id.user.id)
  notification = ApplicationStatus.objects.filter(requester=id.user.id, status='R', signal=1).order_by('date')
  # print(notification[0])
  return render(request, 'team_up/notifications.html', {'notifications': notification})

def application(request):
  # Application Accepted
  if request.method == 'POST':
    if request.POST.get('teammate_status_accept'):
      accepted = request.POST['teammate_status_accept']
      application = ApplicationStatus.objects.filter(id=accepted)
      teamup_adv_id = application[0].teamup_advertisement
      adv_card = Teams.objects.filter(id=teamup_adv_id)
      
      # Adding teammates to a teamup advertisement ---------------->>>>>
      rt = RecruitedTeammates(teamup_advertisement=adv_card[0])
      print('printing teammates')
      # Counting existing teammates for an advertisement to avoid extra teammates accepted by the owner in a team---->>>
      counting_teammates = RecruitedTeammates.objects.filter(teamup_advertisement=adv_card[0])
      teammates_list = []
      total_teammates_count = 0
      for teammate in counting_teammates:
        teammates_list.append(str(teammate.teammates.user))
        total_teammates_count += 1
        print(teammate.teammates.user)
        
      # print(request.user_id)
      print(application[0].requester)
      print(teammates_list)
      print(request.user)
      if(total_teammates_count <= adv_card[0].vacancy + 1 and str(application[0].requester) not in teammates_list):
        id = Extendeduser.objects.get(user=application[0].requester)
        requester = Extendeduser.objects.get(user=id.user_id)
        print(requester.user)
        rt.teammates = Extendeduser(user=requester.user)
        rt.save()
        application_status = ApplicationStatus.objects.get(id=accepted)
        application_status.status = 'A' # Status A means accepted!
        application_status.save()
      else:
        print('Team limit Exceeded!')
      
      counting_teammates = RecruitedTeammates.objects.filter(teamup_advertisement=adv_card[0])
      return render(request, 'team_up/details.html', {'teams': adv_card[0], 'teammates': counting_teammates, 'owner':request.user})
      # ------------- Added------------>>>>>>>>>>>
      # IMPORTANT CODE TO ADD TEAMMATE ENDS HERE------------------------->>>>>>>>>>>>>>>>>>>>>>>
    
    # Application Rejected 
    else:
      rejected = request.POST.get('teammate_status_reject')
      application_status = ApplicationStatus(id=rejected)
      application_status.status = 'R' # status R means application rejected
      application_status.save()
      return notifications(request)

    
    # return render(request, 'team_up/tup_groups.html', {'teams': data})
    # return render(request, 'accounts/user_profile.html', {'data':data})
    # return render(request, 'team_up/coming_up_soon.html')

    

'''
  #---------------HOW TO FETCH ALL TEAMMATES FOR A SINGLE RECRUITMENT CARD?--------->>>>>>
  rt = RecruitedTeammates.objects.filter(teamup_advertisement_id=adv_card[0].id)
  for i in rt:
    print('printing all temmates:\n')
    print(i.teammates)

  #----------------------------------END--------------------->>>>>>>
'''
def user_profile(request, user):
  print(user)
  data = Extendeduser.objects.filter(user = user)
  return render(request, 'accounts/user_profile.html', {'data':data})

def user_teamups(request):
  user_teams = Teams.objects.filter(logged_in_user_id=request.user.id).order_by('pub_date')
  return render(request, 'team_up/tup_groups.html', {'teams': user_teams})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def remove_teammate(request, adv):
  if request.method == 'POST':
    if request.POST.get('teammate'):
      teammate = request.POST.get('teammate')
      print(teammate)
      print(request.user.id)
      print(adv)
      teamup_adv = Teams.objects.filter(id=adv)
      if int(teammate) != int(request.user.id):
        application_status = ApplicationStatus.objects.get(logged_in_user=request.user.id, requester=teammate,
        teamup_advertisement=adv, status='A')
        obj = ApplicationStatus.objects.all()
        for i in obj:
          print(i.logged_in_user)
          print(i.requester)
          print(i.teamup_advertisement)
          print(i.status)
          print('----------------')
        application_status.signal = 1
        application_status.status = 'R'
        application_status.comments = str(teamup_adv[0].logged_in_user.first_name) +', the owner of ' + str(teamup_adv[0].short_description) + ' has removed you from the Team'
        application_status.date = timezone.datetime.now()
        RecruitedTeammates.objects.get(teamup_advertisement=adv, teammates=teammate).delete()
        application_status.save()
  # return show_teamup_details(request)
  return render(request, 'team_up/coming_up_soon.html')