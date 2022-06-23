[![Django CI](https://github.com/KNehe/liveup_api/actions/workflows/django.yml/badge.svg?branch=main)](https://github.com/KNehe/liveup_api/actions/workflows/django.yml)

## Liveup_api

- An API that powers the [liveup web application](https://github.com/KNehe/liveup_web) that enables doctors to track patient prescriptions, avoid redundancy and manual processes.

## Demo

- Watch the demo [youtube](https://youtu.be/FrIVVXfFy-M")

## Setting Up

- Clone this repository
- Create .env with the following variables

```
SECRET_KEY=
DJANGO_ALLOWED_HOSTS=<separated by space>
DEBUG=
POSTGRES_NAME=
POSTGRES_USER=
POSTGRES_PASSWORD=
DB_HOST=
DB_PORT=
FROM_EMAIL=
CORS_ALLOWED_ORIGINS=<separated by space>
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
```

### Docker

- Prep `.env` as described below
- Run `docker compose build`
- Run `docker compose up`
- Visit http://127.0.0.1:8000/api/v1/swagger/ or http://127.0.0.1:8000/api/v1/redoc/

### Or

- Run `pip install -R requirements.txt` in your virtual environment
- Run `python manage.py runserver`
- Visit http://127.0.0.1:8000/api/v1/swagger , http://127.0.0.1:8000/api/v1/ or
- Swagger docs- https://nehe-liveup-api.herokuapp.com/api/v1/swagger/
- Redoc - https://nehe-liveup-api.herokuapp.com/api/v1/redoc/
- Each of the links point to the deployed app on heroku, I do not know how long it'll be up

## Features

- Login with email and password.
- App User Regisration (Only admins can register receptionists, doctors, nurses, student clinicians, create wards, and perform other admin related work in the admin panel).
- Receptionist can register patients, view and edit their details
- Receptionist can refer a patient to a clinician. Only for patients
  they have registered.
- A Receptionist can look up past referrals (history) of patient and edit them.
  They can see history of patients registered by other receptionists too but can
  only edit a referral they made.
- App users can change their names and password.
- Forgot password.
- Clinicians(doctors, nurses, student doctors, etc) can view patients referred to them
- Clinicians can view patient details and record prescriptions
- Clinicians can admit a patient to a particular ward
- Clinicians can view a patient's history (past admissions and prescriptions made by them and other clinicians). Can only edit an admission and prescription they made.
- Statistics. Number of patients registered,
  number of referrals made by all receptionists or a particular receptionist including for the current day, number of patients admitted, number of prescriptions recorded,
  number of referrals made, to all doctors or a particular doctor including that for the current day,
- Pagination

## Tools and technologies used

- Python
- Django
- Django Rest Framework
- PostgreSQL
- Django-Heroku
- JWT

## Admin Panel

- Find the admin panel at http://127.0.0.1:8000/admin or https://nehe-liveup-api.herokuapp.com/admin
- Ensure to create a super user to be able to test locally
- Run `python manage.py load db.json` to initialize the database with users, wards, admissions, referrals, patients and prescriptions.
