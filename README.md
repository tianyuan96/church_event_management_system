**How to get started with the project**


1. Clone into the repository: $ git clone git@bitbucket.org:samscheding/4920-project.git
2. Make a Python virtual environment: $ python3 -m venv env
3. Activate the virtual environment: $ source env/bin/activate
4. Install Django into the virtual environment: $ pip install -r requirements/requirements.txt
5. Run the project: $ python manage.py runserver
6. Visit the development server at: http://127.0.0.1:8000/


**Notes:**

*To start a new app:*
1. $ python manage.py startapp <app_name>
2. Move the new app into 'apps/'
3. Add the app to the list of installed apps in 'church_booking_system/settings.py'    
  eg:

  INSTALLED_APPS = [
      'apps.<new_app>',
      'apps.main',
      ...
