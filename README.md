# commercial-banking-doument-upload-module-using-django

## BACKEND SETUP: (https://djangoforbeginners.com/initial-setup/)

1. Dowload and install python 3

Download the installer and make sure to click the Add Python to PATH option, which will let use use python directly from the command line.

2. Virtual Env

Pipenv is similar to npm and yarn from the JavaScript/Node ecosystem: it creates a Pipfile containing software dependencies and a Pipfile.lock for ensuring deterministic builds. “Determinism” means that each and every time you download the software in a new virtual environment, you will have exactly the same configuration.
The end result is that we will create a new virtual environment with Pipenv for each new Django Project.
To install Pipenv we can use pip3 which HomeBrew automatically installed for us alongside Python 3.

$ pip3 install pipenv

3. Install Django

$ pipenv install django==2.2.5

If you look within our directory there are now two new files: Pipfile and Pipfile.lock. We have the information we need for a new virtual environment but we have not activated it yet. Let’s do that with pipenv shell.

$ pipenv shell

4. Create a new Django project called commercial-banking with the following command. Don’t forget that period . at the end.

(django-_0NWdoUR) $ django-admin startproject commercial_banking .

5. let’s confirm everything is working by running Django’s local web server.

(django-_0NWdoUR) $ python manage.py runserver
If you visit http://127.0.0.1:8000/ you should see the Django welcome page.

If it throws this error ->  Error: [WinError 10013] An attempt was made to access a socket in a way forbidden by its access permissions, try to run the server in a different port

(django-_0NWdoUR) $ python manage.py runserver 127.0.0.1:7000
Now if you visit http://127.0.0.1:7000/ you should see the Django welcome page.

## DATABASE

#### ORM (Operational Relational Model)
 - Tables
   - Customer Table
    - Cust_id
    - Cust_name
    - Cust_file

Table === Class

Table Row === Class Object

``` CUSTOMER ```

Cust_id     Cust_name   Cust_file
----------------------------------------
cust1_id    |cust1_name |cust1_file    |
----------------------------------------
cust2_id    |cust2_name |cust2_file    |
----------------------------------------
cust3_id    |cust3_name |cust3_file    |
----------------------------------------


class Customer:
cust_id: int
cust_name: str
cust_file: file

cust1 = Customer()
cust2 = Customer()
cust3 = Customer()
 
#### postgresql & pgAdmin 

- posgresSQL 
    - Database name: banking
    - Server password: 1234
    - Port number: 5432

#### psycopg2

This is the connector between the PostgreSQL database and the Python programming language.

- How do we install this ?
    - $pip install psycopg2

#### MODELS

https://docs.djangoproject.com/en/3.0/ref/models/fields/

We have to migrate the models to the database,
- $python manage.py makemigrations
- $python manage.py sqlmigrate frontend 0001
- $python manage.py migrate

#### PUSHING DATA TO THE DATABASE THROUGH DJANGO ADMIN PAGE

1. Create a super user
    - $python manage.py createsuperuser
2. There will be admin.py file, where we will have to register the admin page with the model,
    - admin.site.register(<Class_Name>)

#### ADD AND FETCH DATA FROM DATABASE

1. Next is to create the media folder for which we will have to specify the MEDIA_ROOT & MEDIA_URL in the settings.py file and append the urlpatterns in the url.py file.


## COMMANDS

$pip install psycopg2
// This cmd installs psycopg2 through pip, which is the adapter that connects postgres database with the python code.

$python manage.py makemigrations
// This cmd will create the file 0001_initial.py in your module's(here frontend) migration folder. The file contains the create model(here customer) function(). This will just create the migration file.

$python manage.py sqlmigrate frontend 0001
// This cmd creates the table(here frontend_customer) with the SQL command itself.

$python manage.py migrate
// This cmd will migrate and creates the table in the postgres DB.

To create superuser :
$python manage.py createsuperuser
// This cmd will ask for the name, email and password
// Admin username: sri 
// Email address: connect@sri.com
// Password: 1234

If not sure about any commands, go for help command,
$python manage.py help

## SOFTWARES

 - Framework: python3.8.0,
 - Editor: VScode
 - Database: microsoft visual c++ 2015-2019 redistributable (x86) 14.24.28127,postgresql, pgadmin, psycopg2(It's a postgres database adapter which connects with python).
 
## REFERENCE

 - Backend Setup : https://djangoforbeginners.com/initial-setup/
 - Jinja Template Designer : https://jinja.palletsprojects.com/en/2.10.x/templates/
 - Model Fields : https://docs.djangoproject.com/en/3.0/ref/models/fields/
 - Poppler : http://blog.alivate.com.au/poppler-windows/

