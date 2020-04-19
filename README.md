# [Django School](https://djangoschools.herokuapp.com/)

[![Python Version](https://img.shields.io/badge/python-3.6-brightgreen.svg)](https://python.org)
[![Django Version](https://img.shields.io/badge/django-3.0-brightgreen.svg)](https://djangoproject.com)
[![CircleCI](https://circleci.com/gh/suhailvs/django-schools.svg?style=svg)](https://circleci.com/gh/suhailvs/django-schools)

## [demo](https://djangoschools.herokuapp.com/)

This is an example project to illustrate an implementation of multiple user types. In this Django app, teachers can create quizzes and students can sign up and take quizzes related to their interests.

![Django School Screenshot](https://simpleisbetterthancomplex.com/media/2018/01/teacher-quiz.png)

Read the blog post [How to Implement Multiple User Types with Django](https://simpleisbetterthancomplex.com/tutorial/2018/01/18/how-to-implement-multiple-user-types-with-django.html).

## Running the Project Locally

First, clone the repository to your local machine:

```bash
git clone https://github.com/suhailvs/django-schools
```

Create Virtual Env and Install the requirements:

```bash
cd django-schools
python3 -m venv env
source ./env/bin/activate
pip install -r requirements.txt
```

Create the database and run the development server:

```bash
cd django_school
python manage.py migrate
python manage.py loaddata datas.json
python manage.py runserver
```

The project will be available at http://127.0.0.1:8000, Login using::

**Teacher**

username: `teacher`
password: `teacher`

**Student**

username: `student`
password: `student`


## License

The source code is released under the [MIT License](https://github.com/sibtc/django-multiple-user-types-example/blob/master/LICENSE).
