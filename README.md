# Team-up
A Team-up online platform

Steps to setup the project on local:

1. Install Python virtual environment

    $ pip install virtualenv
    
    Cd to a directory in which u want to create a virtalenv eg. Desktop
    
    Then type:
    
    $ virtualenv YourEnvName (eg. virtualenv  myvenv)
    
    Activate virtual environment:
    
    $ source myvenv/bin/activate

2. Install Django

3. Generate a Secret Key for Development Evironment using Django Bash

    $ python manage.py shell

    >>> from django.core.management.utils import get_random_secret_key

    >>> get_random_secret_key()

    Insert the generated key in Team_Up settings.py file as-

    SECRET_KEY = 'YOUR GENERATED SECRET KEY'

4. Run the Project:

    $ python manage.py runserver
    
5. If you do any changes to the model.py (DB) then don't forget to makemigrations and migrate as below:
    
    $ python manage.py makemigrations
    
    $ python manage.py migrate
