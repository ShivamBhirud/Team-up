from django.shortcuts import render, redirect, get_object_or_404
from team_up.models import Teams, RecruitedTeammates
from team_up.serializer import ApplicationStatusSerializer
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.models import Extendeduser
from .models import ApplicationStatus
from django.views.decorators.cache import cache_control
from django.http import HttpResponse
from django.core.paginator import (Paginator,
	EmptyPage, PageNotAnInteger)
import json


def home(request):
	# profile = UserProfile.objects
	return render(request, 'team_up/home.html')

@login_required(login_url="/accounts/login")
def create_t_up(request):
	if request.method == 'POST':
		if (request.POST['category'] and request.POST['short_description'] and
		request.POST['description'] and request.POST['vacancy']):
			# Setup Teams table's fields
			teams = Teams()
			teams.category = request.POST.get('category', False)
			teams.short_description = request.POST['short_description']
			teams.description = request.POST['description']
			teams.vacancy = request.POST['vacancy']
			if request.POST['relevant_url']:
				if (request.POST['relevant_url'].startswith('http://') or 
				request.POST['relevant_url'].startswith('https://')):
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
			return render(request, 'team_up/create_t_up.html', 
			{'error':'All astrisk marked (*) fields are required!'})
	else:
		return render(request, 'team_up/create_t_up.html')

def detail(request, team_up_id):
	#TODO add a page where all his created t-ups are visible to the user
	teamup = get_object_or_404(Teams, pk=team_up_id)
	return render(request, 'team_up/details.html', {'teams':teamup,
	'owner':request.user})

# Functions to handle the functionlity of all the Team-up groups
@login_required(login_url="/accounts/login")
def tup_category(request, category):
	teams = Teams.objects.filter(category=category).order_by('-pub_date')
	page = request.GET.get('page', 1)
	total_page_count = 5
	data = paginate(request, page, teams, total_page_count)
	return render(request, 'team_up/tup_groups.html', {'data': data})

# Show Details of a Teamup Advertisement to the user
def show_teamup_details(request):
	recruiter = request.POST['teamup_details'] 
	adv_card = Teams.objects.filter(id=recruiter)
	counting_teammates = RecruitedTeammates.objects.filter(
		teamup_advertisement_id=adv_card[0].id)
	teammate = {}
	for user in counting_teammates:
		extended_user = Extendeduser.objects.get(user=user.teammates.user_id)
		full_name = str(str(extended_user.first_name) + ' ' + 
		str(extended_user.last_name))
		teammate[user.teammates.user_id] = full_name
	if(adv_card[0].logged_in_user.user == request.user):
		owner = 1
	else:
		owner = 0
	return render(request, 'team_up/details.html', {'teams': adv_card[0],
		'teammates': teammate, 'owner':owner})

  # Add a user to the Teamup
def join_tup(request, recruiter):
	# breakpoint() 
	adv_card = Teams.objects.filter(id=recruiter)
	# New code started for notification----->>>>>>>
	pre_existing_requester = ApplicationStatus.objects.filter(
		logged_in_user=Extendeduser.objects.get(
			user=adv_card[0].logged_in_user.user).user_id,
		requester=request.user.id, teamup_advertisement=adv_card[0].id)
	counting_teammates = RecruitedTeammates.objects.filter(
		teamup_advertisement_id=adv_card[0].id)
	teammates_list = []
	total_teammates_count = 0
	for teammate in counting_teammates:
		teammates_list.append(str(teammate.teammates.user))
		total_teammates_count += 1
		print(teammate.teammates.user)
	# Don't send request if user has pending request, vacancy fulfilled,
	#  or user is already accepted 
	if(pre_existing_requester or total_teammates_count >= adv_card[0].vacancy + 1 or
		str(request.user) in teammates_list):
			pass
	else:
		application_status = ApplicationStatus()
		id = Extendeduser.objects.get(user=adv_card[0].logged_in_user.user)
		application_status.logged_in_user = id.user_id
		id = Extendeduser.objects.get(user=request.user)
		application_status.requester = id.user_id
		application_status.teamup_advertisement = adv_card[0].id
		application_status.status = 'P'
		application_status.date = timezone.datetime.now()
		application_status.save()
	return render(request, 'team_up/join_success.html')

def requests(request):
	id = Extendeduser.objects.get(user=request.user)
	application_status = ApplicationStatus.objects.filter(
		logged_in_user=id.user_id, status='P').order_by('date')
	if(application_status):
		requester = Extendeduser.objects.get(user=application_status[0].requester)
		advertisement = Teams.objects.get(
			id=application_status[0].teamup_advertisement)
		return render(request, 'team_up/requests.html',
		{'notifications': application_status,'requester':requester.first_name,
		'advertisement':advertisement.short_description})
	else:
		return render(request, 'team_up/requests.html', 
		{'notifications': application_status})

def notifications(request):
	id = Extendeduser.objects.get(user=request.user)
	comments = []
	notification = ApplicationStatus.objects.filter(requester=id.user.id,
		status='R', signal=1).order_by('-date')
	for note in notification:
		ser = ApplicationStatusSerializer(note)
		comments.append(ser.data)
	return HttpResponse(json.dumps(comments))

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
			# Counting existing teammates for an advertisement to avoid
			# extra teammates accepted by the owner in a team---->>>
			counting_teammates = RecruitedTeammates.objects.filter(
				teamup_advertisement=adv_card[0])
			teammates_list = []
			total_teammates_count = 0
			for teammate in counting_teammates:
				teammates_list.append(str(teammate.teammates.user))
				total_teammates_count += 1

			if(total_teammates_count <= adv_card[0].vacancy + 1 and 
			str(application[0].requester) not in teammates_list):
				id = Extendeduser.objects.get(user=application[0].requester)
				requester = Extendeduser.objects.get(user=id.user_id)
				rt.teammates = Extendeduser(user=requester.user)
				rt.save()
				application_status = ApplicationStatus.objects.get(
					id=accepted)
				application_status.status = 'A' # Status A means accepted!
				application_status.save()
			else:
				pass
			
			counting_teammates = RecruitedTeammates.objects.filter(
				teamup_advertisement=adv_card[0])
			return render(request, 'team_up/details.html', {'teams': adv_card[0],
				'teammates': counting_teammates, 'owner':request.user})

		# Application Rejected 
		else:
			rejected = request.POST.get('teammate_status_reject')
			application_status = ApplicationStatus(id=rejected)
			application_status.status = 'R' # status R means application rejected
			application_status.save()
			return notifications(request)

def user_profile(request, user):
	if(request.user == user):
		data = Extendeduser.objects.filter(user = user)
		return render(request, 'user_profile/show.html', 
		{'data':data, 'owner':True})
	else:
		data = Extendeduser.objects.filter(user = user)
		return render(request, 'user_profile/show.html', 
		{'data':data, 'owner':False})

def user_teamups(request):
	user_teams = Teams.objects.filter(
		logged_in_user_id=request.user.id).order_by('-pub_date')
	page = request.GET.get('page', 1)
	total_page_count = 5
	data = paginate(request, page, user_teams, total_page_count)
	return render(request, 'team_up/tup_groups.html', {'data': data})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def remove_teammate(request, adv):
	if request.method == 'POST':
		if request.POST.get('teammate'):
			teammate = request.POST.get('teammate')
			teamup_adv = Teams.objects.filter(id=adv)
			if int(teammate) != int(request.user.id):
				try:
					application_status = ApplicationStatus.objects.get(
						logged_in_user=request.user.id, requester=teammate,
						teamup_advertisement=adv, status='A')
					application_status.signal = 1
					application_status.status = 'R'
					application_status.comments = str(str(
						teamup_adv[0].logged_in_user.first_name) +
						', the owner of ' + str(teamup_adv[0].short_description) +
						' has removed you from the Team')
					application_status.date = timezone.datetime.now()
					RecruitedTeammates.objects.get(teamup_advertisement=adv,
					teammates=teammate).delete()
					application_status.save()
					msg = 'Successfully removed the user from the team.'
				except:
					msg = 'User not active any more.'
			else:
				msg = 'Cannot remove yourself from your team!'
		else:
				msg = 'No action taken!'
	user_teams = Teams.objects.filter(
		logged_in_user_id=request.user.id).order_by('-pub_date')
	page = request.GET.get('page', 1)
	total_page_count = 5
	data = paginate(request, page, user_teams, total_page_count)
	return render(request, 'team_up/tup_groups.html', {
		'data': data, 'msg':msg})


# Pagination method
def paginate(request, page, teams, total_page_count):
	paginator = Paginator(teams, total_page_count)
	try:
		elements = paginator.page(page)
		return elements
	except PageNotAnInteger:
		elements = paginator.page(1)
		return elements
	except EmptyPage:
		elements = paginator.page(paginator.num_pages)
		return elements
