from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Extendeduser
from django.contrib.auth.decorators import login_required
import datetime


def signup(request):
	if request.method == 'POST':
		user = Extendeduser()
		creds_validation = user.validate(request.POST.get('username'), request.POST.get('first_name'),
		request.POST.get('gender'), request.POST.get('email'), request.POST.get('city'), 
		request.POST.get('country'), request.POST.get('password1'),request.POST.get('password2'))
		# Asterisk fields are mandatory
		if creds_validation == 0:
			return render(request, 'accounts/signup.html',
			{'error': 'All asterisk (*)marked fields are manadatory!'})
		# Passwords didn't match	
		elif creds_validation == 1:
			return render(request, 'accounts/signup.html', {'error': 'Password didn\'t match!'})
		# User already registered
		elif creds_validation == 2:
			return render(request, 'accounts/signup.html', {'error': 'User already exist!'})
		# User registered successfully 
		else:
			auth.login(request, creds_validation)
			data = Extendeduser.objects.filter(user = request.user)
			return render(request, 'user_profile/show.html', {'data':data})
	else:
		return render(request, 'accounts/signup.html')

def login(request):
  if request.method == 'POST':
    user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
    if user is not None:
      auth.login(request, user)
      return redirect('home')
    else:
      return render(request, 'accounts/login.html', {'error': 'Username or password is incorrect'})
  else:
    return render(request, 'accounts/login.html')

def logout(request):
  if request.method == 'POST':
    auth.logout(request)
    return redirect('home')


# Receiving user details after signup
@login_required(login_url="/accounts/login")
def edit_profile(request):
  obj = Extendeduser(user=request.user)
  if request.method == 'POST':
    if request.POST['first_name'] and request.POST['last_name'] and request.POST['gender'] and request.POST['email'] and request.POST['city'] and request.POST['country'] and request.POST['phone'] and request.POST['about_me'] and request.POST['portfolio'] and request.POST['linkedin'] and request.POST['facebook'] and request.POST['twitter'] and request.POST['other_url']:
      obj.first_name = request.POST['first_name']
      obj.last_name = request.POST['last_name']
      obj.gender = request.POST['gender']
      obj.email = request.POST['email']
      obj.city = request.POST['city']
      obj.country = request.POST['country']
      obj.about_me = request.POST['about_me']
      obj.portfolio = request.POST['portfolio']
      obj.linkedin = request.POST['linkedin']
      obj.facebook = request.POST['facebook']
      obj.twitter = request.POST['twitter']
      obj.other_url = request.POST['other_url']
      obj.phone = request.POST['phone']
      obj.save()
      return redirect('user_profile')
    else:
      data = Extendeduser.objects.get(user = request.user)
      if request.POST['phone']:
        obj.phone = request.POST['phone']
      elif data.phone:
        obj.phone = data.phone
              
      if request.POST['first_name']:
        obj.first_name = request.POST['first_name']
      elif data.first_name:
        obj.first_name = data.first_name
      if request.POST['last_name']:
        obj.last_name = request.POST['last_name']
      elif data.last_name:
        obj.last_name = data.last_name
      if request.POST['gender']:
        obj.gender = request.POST['gender']
      elif data.gender:
        obj.gender = data.gender
      if request.POST['email']:
        obj.email = request.POST['email']
      elif data.email:
        obj.email = data.email
      if request.POST['city']:
        obj.city = request.POST['city']
      elif data.city:
        obj.city = data.city
      if request.POST['country']:
        obj.country = request.POST['country']
      elif data.country:
        obj.country = data.country
      if request.POST['about_me']:
        obj.about_me = request.POST['about_me']
      elif data.about_me:
        obj.about_me = data.about_me
      if request.POST['portfolio']:
        obj.portfolio = request.POST['portfolio']
      elif data.portfolio:
        obj.portfolio = data.portfolio
      if request.POST['linkedin']:
        obj.linkedin = request.POST['linkedin']
      elif data.linkedin:
        obj.linkedin = data.linkedin
      if request.POST['facebook']:
        obj.facebook = request.POST['facebook']
      elif data.facebook:
        obj.facebook = data.facebook
      if request.POST['twitter']:
        obj.twitter = request.POST['twitter']
      elif data.twitter:
        obj.twitter = data.twitter
      if request.POST['other_url']:
        obj.other_url = request.POST['other_url']
      elif data.other_url:
        obj.other_url = data.other_url
      obj.save()
      return redirect('user_profile')
  else:
    return redirect('edit_profile')  

# Show User Profile
@login_required(login_url="/accounts/login")
def showuserdata(request):
  data = Extendeduser.objects.filter(user = request.user)
  return render(request, 'user_profile/show.html', {'data':data, 'owner':True})

@login_required(login_url="/accounts/login")
def update_profile(request):
  data = Extendeduser.objects.filter(user = request.user)
  return render(request, 'user_profile/update.html', {'data':data})










