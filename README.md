# Liquid

A bug tracker web-app that keeps track of reported software bugs or issues in software development projects. <br>Helps teams collaborate and get work done easily and more efficiently. The system has a per-project role-based access control for users. The system allows for 4 types of users; Admin, Project Manager, Developer, and Submitter.

![](/repoImages/Liquid.gif)

### Tech Stack:
* Django 3.1.4
* AWS
* PostgreSQL
* Python 3.8
* Bootstrap 4.5
* Heroku

### How to run locally:

After cloning the app down to your machine, navigate into the root directory of the project. 

1. Install project requirements:
```
    pip install -r requirements.txt
```

2. In the settings.py file:

```Python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
```

3. Migrate and run project:
```
    python manage.py migrate
    python manage.py runserver
```
<br />

### Project Understanding

Types of users/roles:
* Admin
* Project Manager
* Developer
* Submitter

Pages on website:
1. Dashboard page:
    - Purpose: Provide a quick summary of the user's most relevant information in the system.
2. Profile page:
    - Purpose: Provides a detailed view of the user details. Users can also edit their information.
3. Projects page:
    - Purpose: Provide a list of all the projects a user is currently involved in.
    - Sub-pages:
        * Add project page
        * Edit project page
        * Project detail page
4. Project Role-Assignment page:
    - Purpose: Allows admins and project managers to assign user roles in the project.
5. Tickets page:
    - Purpose: Provides a list of all the tickets a user created, or is assigned to. Users can also choose to upload attachments or leave a comment inside a ticket.
    - Sub-pages:
        * Add ticket page
        * Edit ticket page
        * Ticket detail page
6. User Management page:
    - Purpose: For admin users only. Allows admins to grant or change user permissions inside the website.
7. Authentication pages:
    - Purpose: Process user authentication in the website.  
    - Pages:
        * Login page
        * Register page
        * Password Reset page
        * Password Change page

Role-based Permissions:
* Admin
    * Can perform all actions on the site
* Project Manager
    * Can assign roles or edit roles inside project
    * Denied permissions to the User Management page
    * Denied permissions to create new projects
* Developer
    * Can only change the status, priority, and type of ticket
    * Denied permissions to the User Management page
    * Denied permissions to create new projects
    * Denied permissions to assign or edit user roles
    * Denied permissions to create new tickets
    
* Submitter
    * Can create and edit tickets
    * Denied permissions to the User Management page
    * Denied permissions to create new projects
    * Denied permissions to assign or edit user roles inside a project
    


