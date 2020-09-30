from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Extendeduser(models.Model):
	user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255, default='')
	gender = models.CharField(max_length=255, blank=True, default='rather_not_say') #TODO CHECK THE ENUMS TO AVOID DUMMY ENTRY
	email = models.EmailField(verbose_name='email', max_length=60, default='')
	about_me = models.TextField(max_length=1000, default="Let's Team-up!")
	portfolio = models.URLField(default='Not Provided')
	linkedin = models.URLField(default='Not Provided')
	facebook = models.URLField(default='Not Provided')
	twitter = models.URLField(default='Not Provided')
	other_url = models.URLField(default='Not Provided')
	city = models.CharField(max_length=255, default='')
	country = models.CharField(max_length=255, default='') # TODO CREATE A DATA STRUCTURE TO SHOW THE IST OF COUNTRIES
	phone = models.CharField(max_length=17, default='0000000000')
	date_joined = models.DateTimeField(verbose_name='date_joined', auto_now=True)
	last_login = models.DateTimeField(verbose_name='last_login', auto_now=True)
	is_admin = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)

    # Signup details accepted
	def validate(
		self, username, first_name, gender, email, city, country,
		password1, password2
	):
		if first_name and gender and email and city and country:
			if password1 == password2:
				try:
					user = User.objects.get(username=username)
					# User already registered
					return 2
				except User.DoesNotExist:
					user = User.objects.create_user(username, password=password1)
					user_details = Extendeduser(first_name = first_name, email = email, gender = gender, city = city, country = country, user=user)
					user_details.save()
					# User registered successfully 
					return user
			else:
				# Passwords didn't match
				return 1
		else:
			# Asterisk fields are mandatory
			return 0

	# Update user details
	#TODO Validate the entries
	def user_details(
		self, first_name, last_name, gender, email, city, country, phone,
		about_me, portfolio, linkedin, facebook, twitter, other_url, user
	):
		data = Extendeduser.objects.get(user=user)
		if phone:
			data.phone = phone		
		if first_name:
			data.first_name = first_name
		if last_name:
			data.last_name = last_name
		if gender:
			data.gender = gender
		if email:
			data.email = email
		if city:
			data.city = city
		if country:
			data.country = country
		if about_me:
			data.about_me = about_me
		if portfolio:
			data.portfolio = portfolio
		if linkedin:
			data.linkedin = linkedin
		if facebook:
			data.facebook = facebook
		if twitter:
			data.twitter = twitter
		if other_url:
			data.other_url = other_url
		data.save(update_fields= ['first_name', 'last_name', 'gender', 'email',
			'city', 'country', 'phone', 'about_me', 'portfolio', 'linkedin',
			'facebook', 'twitter', 'other_url'])
			
		return True


    

  