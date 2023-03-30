# Team AYMSKYT Major Group Project
## Minted - A1 Personal Spending Tracker

## Team members

The members of the the team are:

- Amber Leung
- Yu Han Chen
- Maja Szczepanczyk
- Stephanie Lawal
- Kyron Caesar
- Yasamin Divsalar
- Thang Nguyen

## Project structure

The project is called `PersonalSpendingTracker`. It consists of a single app called `minted` where all functionality resides.

## Deployed version of the application:
The deployed version of the application can be found at **[Minted](https://minted-aymskyt.azurewebsites.net/)**.

## Installation instructions:
To setup for development, you must edit `settings.py` inside the *PersonalSpendingTracker* directory to be 
`DEBUG = True` from the existing `DEBUG = False`

To install the software and use it in your local development environment, you must first set up and activate a 
local development environment.  From the root of the project:
```
$ virtualenv venv
$ source venv/bin/activate
```
Install mysqlclient:
*For more info see [here](https://pypi.org/project/mysqlclient/)*
```
# Debian
$ sudo apt-get install python3-dev default-libmysqlclient-dev build-essential

# macOS (Homebrew)
$ brew install mysql
```
Install all required packages:
```
$ pip3 install -r requirements.txt
```
Set up environment variables:
- *Copy `.env.sample` into a new file `.env`  at the root directory and replace with your own variables*

  ```dotenv
  # The following variables are required:
  
  # Notifications
  VAPID_PUBLIC_KEY = YOUR_VAPID_PUBLIC_KEY
  VAPID_PRIVATE_KEY = YOUR_VAPID_PRIVATE_KEY
  VAPID_ADMIN_EMAIL = YOUR_VAPID_ADMIN_EMAIL
  
  # Password resets
  EMAIL_HOST = MAIL_SERVICE_SMTP
  EMAIL_HOST_USER = EMAIL_USER_ID
  EMAIL_HOST_PASSWORD = EMAIL_PASSWORD
  EMAIL_PORT = EMAIL_PORT
  EMAIL_USE_TLS = BOOLEAN_USE_TLS
  
  # OAuth
  CLIENT_ID = YOUR-CLIENT-ID
  SECRET = YOUR-SECRET
  ```

Make migrations:
```
$ python3 manage.py makemigrations
```
Migrate the database:
```
$ python3 manage.py migrate
```
Create social app for oauth
```
$ python3 manage.py create_social_app
```
Create default notification subscriptions:
```
$ python3 manage.py create_subscriptions
```
Collect static files:
```
$ python3 manage.py collectstatic
```
Seed the development database with:
```
$ python3 manage.py seed
```
Run all tests with:
```
$ python3 manage.py test
```
Setup cronjobs:
*Note: Your file path must not include spaces*
```
$ python3 manage.py crontab add
```
To remove cronjobs after development:
```
$ python3 manage.py crontab remove
```

## Sources:

*Packages:*

The packages used by this application are specified in `requirements.txt`
The exact version of each package used by this application can also be found in this same file.

For the implementation of notifications we used this [guide](https://www.digitalocean.com/community/tutorials/how-to-send-web-push-notifications-from-django-applications)
and adapted it to work with our project.

Some code has been taken and adapted from the 5CCS2SEG Clucker project.