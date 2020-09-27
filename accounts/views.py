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
	extendeduser = Extendeduser()
	if request.method == 'POST':
		extendeduser.user_details(request.POST.get('first_name'), request.POST.get('last_name'),
		request.POST.get('gender'), request.POST.get('email'), request.POST.get('city'),
		request.POST.get('country'), request.POST.get('phone'), request.POST.get('about_me'),
		request.POST.get('portfolio'), request.POST.get('linkedin'), request.POST.get('facebook'),
		request.POST.get('twitter'), request.POST.get('other_url'), request.user)
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
