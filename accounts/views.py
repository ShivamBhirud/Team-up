from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from .models import extendeduser
from django.contrib.auth.decorators import login_required


# Create your views here.
def signup(request):
  if request.method == 'POST':
    # User has the info and wants the account now
    if request.POST['password1'] == request.POST['password2']:
      try:
        user = User.objects.get(username=request.POST['username'])
        return render(request, 'accounts/signup.html', {'error': 'User already exist!'})
      except User.DoesNotExist:
        user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])

        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        gender = request.POST['gender'],
        # email = request.POST['email'],
        # city = request.POST['city'],
        # country = request.POST['country'],
        # about_me = request.POST['about_me'],
        # portfolio = request.POST['portfolio'],
        # linkedin = request.POST['linkedin'],
        # fackebook = request.POST['fackebook'],
        # twitter = request.POST['twitter'],
        # other_url = request.POST['other_url'],
        # dob = request.POST['dob'],
        # phone = request.POST['phone']

        new_user = extendeduser(first_name = first_name, last_name = last_name, gender = gender, user=user)
        # email = email,
        # city = city, country = country, about_me = about_me, portfolio = portfolio, linkedin = linkedin,
        # fackebook = fackebook, twitter = twitter, dob = dob, other_url = other_url, phone = phone,
        new_user.save()
        auth.login(request, user)
        # return redirect('home')
        return render(request, 'accounts/edit_profile_page.html')
    else:
      return render(request, 'accounts/signup.html', {'error': 'Password didn\'t match!'})
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
@login_required(login_url="/accounts/signup")
def edit_profile(request):
  if request.method == 'POST':
    if request.POST['first_name'] and request.POST['gender'] and request.POST['email'] and request.POST['city'] and request.POST['country']:
      user = request.user
      extendeduser.objects.filter(id = user.id).update(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        gender = request.POST['gender'],
        email = request.POST['email'],
        city = request.POST['city'],
        country = request.POST['country'],
        about_me = request.POST['about_me'],
        portfolio = request.POST['portfolio'],
        linkedin = request.POST['linkedin'],
        fackebook = request.POST['fackebook'],
        twitter = request.POST['twitter'],
        other_url = request.POST['other_url'],
        dob = request.POST['dob'],
        phone = request.POST['phone'] #giving errror if ph is no entered
      )
      return redirect('showdata')
    else:
      user = request.user
      extendeduser.objects.filter(id = user.id).update(
        last_name = request.POST['last_name'],
        about_me = request.POST['about_me'],
        portfolio = request.POST['portfolio'],
        linkedin = request.POST['linkedin'],
        fackebook = request.POST['fackebook'],
        twitter = request.POST['twitter'],
        other_url = request.POST['other_url'],
        dob = request.POST['dob'],
        phone = request.POST['phone']
      )
      return render(request, 'accounts/edit_profile.html', {'error': 'All asterisk (*) marked fields are manadatory!'})
  else:
    return redirect('edit_profile')  

# Show User Profile
#TODO Name everything properly
@login_required(login_url="/accounts/login")
def showuserdata(request):
  data = extendeduser.objects.filter(user = request.user)
  return render(request, 'accounts/showdata.html', {'data':data})












