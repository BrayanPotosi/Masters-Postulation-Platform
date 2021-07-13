# Master's Postulation Platform

### Backend of master's postulation platform.
This service provides all data managment to allow the Authentication, Authorization and persistance of user´s data.

The Máster´s Postulation platform allow to send a postulation for the **Platzi Master** program.
#### Candidate UI
The student is able to complete a profile and send the postulation form.
#### Admin UI
The administration role is able to review the profile and give a score.

### Technologies
- Django: Web framework to develop web apps.
- Django-Rest-Framework: REST API framework
- Pandas: Library to manage data.
- Python: Programming language.
- AWS: EC2 machine, deployment using Traefik, Docker.
- PostgreSQL: Database

# API Documentation
API Documentation using postman:
- https://documenter.getpostman.com/view/14419155/TzeaiQzy

  

# Get started

  

1. Clone the repository:

*  `git clone https://github.com/master-s-postulation-platform/backend.git `

  

2.  `cd backend`

3.  `virtualenv -p=python3.8 .venv`

4.  `source .venv/bin/activate`

5.  `pip install -r requirements.txt`

6.  `cd master_postulation_prj`

7.  `python manage.py migrate`

## Create a new branch

`git checkout -b issue_name`

## Run local server

 `python manage.py runserver`
