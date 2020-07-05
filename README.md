# Team-up
A Team-up online platform

Steps to setup the project:

1. Install Python virtual environment

    pip3 install virtualenv
    
    Cd to a directory in which u want to create a virtalenv eg. Desktop
    
    Then type:
    
    virtualenv YourEnvName (eg. virtualenv  myvenv)
    
    Activate virtual environment:
    
    Type: source myvenv/bin/activate

2. Install Django

3. Run the Project:

    python3 manage.py runserver
    
4. If you do any changes to the model.py (DB) then don't forget to makemigrations and migrate as below:
    
    python3 manage.py makemigrations
    
    python3 manage.py migrate
